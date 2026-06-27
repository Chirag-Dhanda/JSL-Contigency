import logging
from modules.prompt_studio.engine import PromptStudioEngine
from modules.prompts.models import PromptStatus
from modules.prompt_testing.tester import PromptTester
from modules.prompts.deployment import PromptDeployer

logging.basicConfig(level=logging.DEBUG)

def test_prompt_studio():
    print("--- Testing Enterprise Prompt Studio ---")
    
    # 1. Create a Draft Prompt
    print("\n--- 1. Creating Draft Prompt ---")
    engine = PromptStudioEngine()
    prompt_data = {
        "prompt_id": "PRMPT-MFG-01",
        "name": "Manufacturing Equipment Query",
        "category": "Manufacturing",
        "description": "Used when an operator asks about machine specs.",
        "system_prompt": "You are an expert AI for {department}. Only answer using {retrieved_knowledge}.",
        "prompt_body": "User {current_user} is asking: {question}",
        "author": "admin-1"
    }
    draft = engine.create_draft(prompt_data)
    
    print(f"Created Prompt: {draft.name} | Status: {draft.status}")
    
    # 2. Test Sandbox (Variable Injection)
    print("\n--- 2. Sandbox Testing ---")
    tester = PromptTester()
    mock_context = {
        "department": "Melting Shop",
        "retrieved_knowledge": "EAF Max Temp is 1600C.",
        "current_user": "John Doe",
        "question": "What is the max temp?"
    }
    
    preview_sys = tester.preview_prompt(draft.system_prompt, mock_context)
    preview_body = tester.preview_prompt(draft.prompt_body, mock_context)
    
    print("PREVIEW SYSTEM PROMPT:")
    print(preview_sys)
    print("PREVIEW PROMPT BODY:")
    print(preview_body)
    
    # 3. Test Lifecycle & Deployment
    print("\n--- 3. Lifecycle & Deployment ---")
    
    # Try deploying a draft (should fail)
    deployer = PromptDeployer()
    success = deployer.deploy_prompt(draft)
    print(f"Deploying Draft... Success: {success}")
    
    # Push through lifecycle
    engine.governance.request_approval(draft)
    print(f"Status after Review Request: {draft.status}")
    
    engine.versioning.transition_state(draft, PromptStatus.APPROVED, reviewer_id="mgr-1")
    engine.versioning.transition_state(draft, PromptStatus.PUBLISHED)
    print(f"Final Status: {draft.status}")
    
    # Deploy again
    success = deployer.deploy_prompt(draft)
    print(f"Deploying Published... Success: {success}")
    print(f"Active Prompt in Deployer: {deployer.get_active_prompt('Manufacturing Equipment Query').prompt_id}")
    
    print("\nTest Complete!")

if __name__ == "__main__":
    test_prompt_studio()
