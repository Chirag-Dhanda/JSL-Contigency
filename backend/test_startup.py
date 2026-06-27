from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.testclient import TestClient
from main import app
from exceptions.base import NotFoundException, SystemException
from core.lifecycle import lifecycle
from core.module import BaseModule
from core.di import container
import logging

class DummyService:
    def execute(self):
        return "Success"

class TestModule(BaseModule):
    @property
    def name(self) -> str:
        return "TestModule"
        
    @property
    def version(self) -> str:
        return "1.0.0"
        
    def register_services(self, container):
        container.register_singleton(DummyService, DummyService())
        # Simulate duplicate protection test
        try:
            container.register_singleton(DummyService, DummyService())
        except SystemException as e:
            logging.getLogger("Application").info(f"Duplicate registration safely prevented: {e}")
            
    async def initialize(self):
        logging.getLogger("Application").info("TestModule Initialized!")
        
    async def shutdown(self):
        logging.getLogger("Application").info("TestModule Shutdown Cleanly!")

# Inject module before starting
lifecycle.register_module(TestModule)

test_router = APIRouter()

class TestPayload(BaseModel):
    required_field: str

@test_router.get("/error/not-found")
async def trigger_not_found():
    raise NotFoundException(message="This is a test not found exception.")

@test_router.get("/error/unhandled")
async def trigger_unhandled():
    raise ValueError("This is a raw python exception!")

@test_router.post("/error/validation")
async def trigger_validation(payload: TestPayload):
    return {"message": "Success"}

@test_router.get("/di/test")
async def resolve_di():
    svc = container.resolve(DummyService)
    return {"result": svc.execute()}

from modules.auth.middleware import require_authenticated_user
from fastapi import Depends
from modules.security.jwt import JWTService
from modules.security.hashing import PasswordHasher

@test_router.get("/protected")
async def protected_route(payload: dict = Depends(require_authenticated_user)):
    return {"message": "You are authenticated!", "sub": payload.get("sub")}

app.include_router(test_router, prefix="/api/v1/test", tags=["Test"])

with TestClient(app, raise_server_exceptions=False) as client:
    print("\n--- Testing NotFoundException ---")
    response = client.get("/api/v1/test/error/not-found")
    print(f"Status: {response.status_code}")

    print("\n--- Testing Unhandled Exception ---")
    response = client.get("/api/v1/test/error/unhandled")
    print(f"Status: {response.status_code}")

    print("\n--- Testing RequestValidationError ---")
    response = client.post("/api/v1/test/error/validation", json={"wrong_field": "test"})
    print(f"Status: {response.status_code}")

    print("\n--- Testing DI Container Resolution ---")
    response = client.get("/api/v1/test/di/test")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    print("\n--- Testing Authentication & Security Sequences ---")
    
    # 1. Test Lockout (Bad Password)
    response = client.post("/api/v1/auth/login", json={"username": "admin", "password": "wrongpassword"})
    print(f"Bad Password Status: {response.status_code}")
    
    # 2. Test First Login (Force Change)
    response = client.post("/api/v1/auth/login", json={"username": "newguy", "password": "temp123"})
    print(f"First Login Status: {response.status_code} (Should be 403 Forbidden)")
    
    # 3. Test Password Change
    response = client.post("/api/v1/auth/change-password", json={
        "username": "newguy", 
        "current_password": "temp123", 
        "new_password": "newSecret123!"
    })
    print(f"Change Password Status: {response.status_code}")
    
    # 4. Test Successful Login
    response = client.post("/api/v1/auth/login", json={"username": "newguy", "password": "newSecret123!"})
    print(f"Successful Login Status: {response.status_code}")
    access_token = response.json().get("access_token")
    
    # 5. Test Protected Route
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/v1/test/protected", headers=headers)
    print(f"Protected Route Status: {response.status_code}")
    
    # 6. Test Logout
    response = client.post("/api/v1/auth/logout", headers=headers)
    print(f"Logout Status: {response.status_code}")
    
    # 7. Test Protected Route after Logout
    response = client.get("/api/v1/test/protected", headers=headers)
    print(f"Protected Route after Logout Status: {response.status_code} (Should be 401 Unauthorized)")

    print("\n--- Testing Access Governance & Temporary Permissions ---")
    from modules.authorization.service import AuthorizationPipeline
    from modules.authorization.models import ResourceOwnership
    from modules.access_request.service import AccessRequestService
    from modules.access_request.enums import DurationType
    from modules.permissions.service import PermissionEngine
    
    auth_pipeline = container.resolve(AuthorizationPipeline)
    access_req_svc = container.resolve(AccessRequestService)
    
    # Mock Scenario: 
    # User 'u-sales-1' (Dept: 'dept-sales') wants to view resource 'res-finance-db' (Owned by: 'dept-finance')
    actor_id = "u-sales-1"
    actor_dept = "dept-sales"
    req_permission = "database.read"
    resource = ResourceOwnership(resource_id="res-finance-db", owned_by_dept_id="dept-finance", created_by="system")
    
    # Pre-requisite: we must mock the PermissionEngine to allow 'database.read' at the RBAC level, 
    # otherwise DBAC won't even evaluate. Since PermissionEngine is a mock in test_startup right now, 
    # wait, we didn't mock PermissionEngine, it's a real class. It might throw Not Implemented.
    # Let's dynamically patch it for the test.
    import asyncio
    
    async def mock_has_perm(act_id, perm):
        return True # Assume RBAC allows it generally
        
    perm_engine = container.resolve(PermissionEngine)
    perm_engine.has_explicit_permission = mock_has_perm
    
    # 1. Attempt access without temporary grant (Should yield Overview Only)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(auth_pipeline.evaluate_access(actor_id, actor_dept, req_permission, resource))
    print(f"Initial Cross-Dept Access: {result} (Expected: Overview Only)")
    
    # 2. Create and Approve Access Request
    req_id = loop.run_until_complete(access_req_svc.create_request(
        requester_id=actor_id,
        target_resource=resource.resource_id,
        perm=req_permission,
        justification="End of quarter cross-referencing",
        duration=DurationType.TEMPORARY
    ))
    loop.run_until_complete(access_req_svc.approve_request(req_id, approver_id="u-admin-1", active_minutes=60))
    print(f"Temporary Access Request {req_id} Approved.")
    
    # 3. Re-evaluate access
    result2 = loop.run_until_complete(auth_pipeline.evaluate_access(actor_id, actor_dept, req_permission, resource))
    print(f"Elevated Cross-Dept Access: {result2} (Expected: Granted Full)")

    print("\n--- Testing Communication Hub (Events & Notifications) ---")
    from modules.events.bus import EventBus
    from modules.events.models import DomainEvent
    from modules.templates.engine import TemplateEngine
    from modules.templates.models import MessageTemplate
    from modules.notifications.service import NotificationService
    
    event_bus = container.resolve(EventBus)
    template_engine = container.resolve(TemplateEngine)
    notif_svc = container.resolve(NotificationService)
    
    # Pre-requisite: Register a template
    template_engine.register_template(MessageTemplate(
        template_id="USER_WELCOME",
        subject="Welcome to JSL, {{ name }}!",
        body_content="Your account has been created. Role: {{ role }}",
        supported_channels=["IN_APP", "EMAIL"]
    ))
    
    # Pre-requisite: Wire the NotificationService to the EventBus
    async def on_user_registered(event: DomainEvent):
        await notif_svc.send_notification(
            recipient_id=event.payload["user_id"],
            template_id="USER_WELCOME",
            context={"name": event.payload["name"], "role": event.payload["role"]}
        )
    event_bus.subscribe("USER_REGISTERED", on_user_registered)
    
    # Dispatch an Event natively
    new_user_event = DomainEvent.create(
        event_type="USER_REGISTERED",
        source="UsersModule",
        payload={"user_id": "u-test-99", "name": "Alice Developer", "role": "Engineer"}
    )
    
    loop.run_until_complete(event_bus.publish(new_user_event))
    print("Event Published and Notification Dispatched Successfully.")

    print("\n--- Testing Enterprise Security Middleware ---")
    
    # 1. Test Input Sanitization and Security Headers
    # We will hit the health endpoint with a malicious query parameter
    malicious_query = "?search=<script>alert(1)</script>&action=DROP TABLE users"
    response = client.get(f"/api/v1/test/di/test{malicious_query}")
    
    print(f"Sanitization/Headers Status: {response.status_code}")
    print(f"Response Headers (Security CSP): {response.headers.get('Content-Security-Policy')}")
    print(f"Response Headers (X-Frame-Options): {response.headers.get('X-Frame-Options')}")
    
    # Check if the query parameter actually got sanitized in the Starlette scope
    # (Since we didn't echo it in the test endpoint, we just prove it didn't break and headers exist)
    
    # 2. Test Rate Limiting
    print("Testing Rate Limiter (Max 5 requests/10s)...")
    for i in range(1, 7):
        resp = client.get("/api/v1/test/di/test")
        if resp.status_code == 429:
            print(f"Request {i}: Blocked (429 Too Many Requests) - RATE LIMIT ENFORCED")
        else:
            print(f"Request {i}: Allowed ({resp.status_code})")

    print("\n--- Testing Learning Roadmap Engine (DAG) ---")
    from modules.roadmap.models import Roadmap, RoadmapStage, RoadmapNode, RoadmapNodeDependency
    from modules.roadmap.enums import NodeType, NodeStatus, DependencyType
    from modules.roadmap.service import RoadmapService
    
    roadmap_svc = container.resolve(RoadmapService)
    
    # Define nodes
    n1 = RoadmapNode(id="n-welcome", title="Welcome", description="Welcome to JSL", type=NodeType.INFORMATION)
    n2 = RoadmapNode(
        id="n-safety", 
        title="Safety Guidelines", 
        description="Mandatory safety training", 
        type=NodeType.INTERACTIVE_LESSON,
        dependencies=[RoadmapNodeDependency(node_id="n-welcome", dependency_type=DependencyType.MANDATORY)]
    )
    n3 = RoadmapNode(
        id="n-dept", 
        title="Department Overview", 
        description="Your department", 
        type=NodeType.VIDEO,
        dependencies=[RoadmapNodeDependency(node_id="n-safety", dependency_type=DependencyType.MANDATORY)]
    )
    
    stage1 = RoadmapStage(id="stage-1", title="Day 1 Onboarding", order=1, nodes=[n1, n2, n3])
    roadmap = Roadmap(id="rm-onboard", title="JSL Onboarding", description="Default Journey", stages=[stage1])
    
    roadmap_svc.register_roadmap(roadmap)
    
    # 1. Initialize user journey
    user_prog = roadmap_svc.initialize_user_journey("u-test-88", "rm-onboard")
    print(f"Initial Status - Welcome: {user_prog.node_progress['n-welcome'].status.value}") # Should be UNLOCKED
    if "n-safety" in user_prog.node_progress:
        print(f"Initial Status - Safety: {user_prog.node_progress['n-safety'].status.value}")
    else:
        print(f"Initial Status - Safety: LOCKED (Not present in unblocked state)")
        
    # 2. Complete Welcome Node
    user_prog = roadmap_svc.mark_node_completed("u-test-88", "rm-onboard", "n-welcome")
    print(f"After Welcome completion - Safety Status: {user_prog.node_progress['n-safety'].status.value}") # UNLOCKED
    
    # 3. Complete Safety Node
    user_prog = roadmap_svc.mark_node_completed("u-test-88", "rm-onboard", "n-safety")
    print(f"After Safety completion - Dept Status: {user_prog.node_progress['n-dept'].status.value}") # UNLOCKED

    print("\n--- Testing Digital Factory Manufacturing Journey ---")
    from modules.manufacturing.service import ManufacturingService
    
    mfg_svc = container.resolve(ManufacturingService)
    
    # Retrieve the scaffolded default SS Journey
    journey = mfg_svc.get_journey("journey-ss-01")
    print(f"Loaded Manufacturing Journey: {journey.title}")
    for st in journey.stations:
        print(f"Station: {st.name} | SAP WC: {st.sap_work_center_id}")
        print(f"  Inputs: {st.input_materials}")
        print(f"  Outputs: {st.output_materials}")
        
    # Log progress
    prog = mfg_svc.log_station_visit("u-test-88", "st-eaf")
    print(f"User u-test-88 visited EAF Station: {prog.visited}")

    print("\n--- Testing Enterprise Knowledge Engine ---")
    from modules.knowledge.service import KnowledgeService
    from modules.knowledge.models import KnowledgeObject
    from modules.knowledge.enums import ContentType, ContentStatus, DifficultyLevel
    from datetime import datetime, timezone
    
    knowledge_svc = container.resolve(KnowledgeService)
    
    ko = KnowledgeObject(
        id="ko-safety-01",
        title="Arc Furnace Safety Protocols",
        description="Core safety protocols for operating the EAF.",
        content_type=ContentType.INTERACTIVE_LESSON,
        category="Safety",
        department="Melting",
        difficulty=DifficultyLevel.INTERMEDIATE,
        tags=["safety", "eaf", "high-voltage"],
        author_id="u-admin-1",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    # 1. Author Content (Draft)
    knowledge_svc.create_knowledge_object(ko)
    print(f"Authored KO: {ko.title} (Status: {ko.status.value})")
    
    # 2. Search while in Draft (Should yield 0 results)
    results = knowledge_svc.search_knowledge(tags=["safety"])
    print(f"Search results for 'safety' (Draft state): {len(results)}")
    
    # 3. Publish Content
    knowledge_svc.transition_status("ko-safety-01", ContentStatus.PUBLISHED, "u-admin-1")
    
    # 4. Search while Published (Should yield 1 result)
    results = knowledge_svc.search_knowledge(tags=["safety"])
    print(f"Search results for 'safety' (Published state): {len(results)}")
    if results:
        print(f"Found Published Content: {results[0].title} | Difficulty: {results[0].difficulty.value}")

print("\nAll Tests Complete.")
