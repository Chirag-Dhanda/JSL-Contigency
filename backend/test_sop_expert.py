import logging
from modules.sop_ai.engine import SOPAIEngine

logging.basicConfig(level=logging.DEBUG)

def test_sop_ai():
    print("--- Testing SOP AI Engine & Safety Middleware ---")
    engine = SOPAIEngine()
    
    # Query: User asks a dangerous operational question that trips the Safety Validator
    query = "How do I turn on the power for the EAF startup?"
    sop_id = "SOP-EAF-001"
    
    response = engine.process_query(query, sop_id)
    
    print("\n--- Query Results ---")
    print(f"Referenced SOP: {response.referenced_sop}")
    print(f"Target Section Identified: {response.referenced_section}")
    print(f"AI Answer: {response.answer}")
    print(f"\n--- SAFETY VALIDATOR INJECTIONS ---")
    print(f"Mandatory Notices: {response.mandatory_safety_notices}")
    print(f"Required PPE: {response.required_ppe}")
    print(f"\n--- LINKED KNOWLEDGE ---")
    print(f"Related Lessons: {response.related_lessons}")
    print(f"Related Equipment: {response.related_equipment}")
    
    print("\nTest Complete!")

if __name__ == "__main__":
    test_sop_ai()
