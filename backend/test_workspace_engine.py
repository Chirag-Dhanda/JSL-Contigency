import logging
import json
from modules.workspace.service import WorkspaceEngineService
from modules.personalization.service import PersonalizationEngineService

logging.basicConfig(level=logging.ERROR)

def main():
    print("=========================================================")
    print("STARTING STAGE 5.9 VALIDATION: EXPERIENCE PLATFORM")
    print("=========================================================")
    
    workspace_engine = WorkspaceEngineService()
    personalization_engine = PersonalizationEngineService()
    
    roles_to_test = ["ENGINEER", "MASTER_EDITOR", "OPERATOR"]
    
    for role in roles_to_test:
        print(f"\n--- Generating Workspace for Role: {role} ---")
        
        # 1. Generate layout from templates
        profile = workspace_engine.get_workspace_for_user(f"u-{role.lower()}", role)
        
        # 2. Add AI Personalization
        profile = personalization_engine.personalize_workspace(profile)
        
        print(f"User ID: {profile.user_id}")
        print(f"Layout Name: {profile.layout.name}")
        print(f"Widget Count: {len(profile.layout.widgets)}")
        print(f"AI Recommendations: {len(profile.ai_recommendations)}")
        
        print("\nWidgets Assigned:")
        for w in profile.layout.widgets:
            print(f"  - [{w.type}] {w.title} ({w.grid_area})")
            
        print("\nAI Copilot Highlights:")
        for r in profile.ai_recommendations:
            print(f"  - {r['title']} ({r['type']})")
            
        assert len(profile.layout.widgets) > 0, "Expected widgets to be assigned"

    print("\n=========================================================")
    print("VALIDATION SUCCESSFUL: EXPERIENCE PLATFORM IS OPERATIONAL")
    print("=========================================================")

if __name__ == "__main__":
    main()
