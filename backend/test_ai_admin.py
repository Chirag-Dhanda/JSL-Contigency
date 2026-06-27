import logging
from modules.model_management.admin_manager import AdminModelManager
from modules.ai_monitoring.health import HealthMonitor
from modules.ai_monitoring.alerts import AlertSystem
from modules.ai_security.permissions import AIPermissionManager
from modules.ai_admin.audit import AIAuditLogger

logging.basicConfig(level=logging.DEBUG)

def test_ai_admin():
    print("--- Testing AI Administration & Governance ---")
    
    # 1. Test Model Management
    print("\n--- 1. Model Management ---")
    model_mgr = AdminModelManager()
    models = model_mgr.get_all_models()
    print(f"Loaded {len(models)} models.")
    print(f"Default Chat Model: {[m.model_id for m in models if m.is_default_chat][0]}")
    model_mgr.toggle_model("llama3", False)
    print(f"llama3 is_enabled after toggle: {[m.is_enabled for m in models if m.model_id == 'llama3'][0]}")
    
    # 2. Test Monitoring & Alerts
    print("\n--- 2. Monitoring & Alerts ---")
    health = HealthMonitor()
    status = health.check_system_health()
    print(f"System Health Status: {status['status']}")
    
    # Force a failure for testing
    status['components']['ollama_local'] = "Offline"
    status['storage_usage_percent'] = 90.0
    
    alerter = AlertSystem()
    generated_alerts = alerter.generate_alerts(status)
    for alert in generated_alerts:
        print(f"ALERT [{alert['type']}]: {alert['message']}")
        
    # 3. Test Security Permissions
    print("\n--- 3. AI Permission Management ---")
    perms = AIPermissionManager()
    can_engineer_use_mfg = perms.check_access("Engineer", "ManufacturingExpert")
    can_engineer_use_hr = perms.check_access("Engineer", "HRDataAgent")
    print(f"Engineer -> ManufacturingExpert? {can_engineer_use_mfg}")
    print(f"Engineer -> HRDataAgent? {can_engineer_use_hr}")
    
    # 4. Test Audit Logging
    print("\n--- 4. Audit Logging ---")
    auditor = AIAuditLogger()
    auditor.log_request(
        user_id="user-999",
        question="How do I start the EAF?",
        model_used="llama3",
        success=True,
        response_time_ms=840,
        sources=["SOP-EAF-01"]
    )
    print(f"Audit Log Count: {len(auditor.logs)}")
    print(f"Latest Log Entry: {auditor.logs[0]['question']} (Model: {auditor.logs[0]['model_used']})")
    
    print("\nTest Complete!")

if __name__ == "__main__":
    test_ai_admin()
