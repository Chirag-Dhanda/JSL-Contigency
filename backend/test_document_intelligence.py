import logging
import json
from modules.document_intelligence.engine import DocumentIntelligenceEngine

logging.basicConfig(level=logging.DEBUG)

def test_intelligence_engine():
    print("--- Testing Document Intelligence Engine ---")
    engine = DocumentIntelligenceEngine()
    
    mock_document_text = """
    Standard Operating Procedure: Electric Arc Furnace
    
    Table 1: Hazards
    Ensure all safety equipment is worn when operating the furnace.
    """
    
    payload = engine.process_document(mock_document_text, "doc-eaf-001")
    
    print("\n--- Intelligence Payload Output ---")
    print(f"Classification: {payload['classification']}")
    print(f"Structure Detected (Has Tables): {payload['structure']['has_tables']}")
    print(f"Entities Extracted: {len(payload['extracted_entities'])}")
    if len(payload['extracted_entities']) > 0:
        print(f"  -> First Entity: {payload['extracted_entities'][0]['entity_value']} (Type: {payload['extracted_entities'][0]['entity_type']})")
        print(f"  -> Confidence: {payload['extracted_entities'][0]['confidence_score']}")
        
    print(f"Relationships Mapped: {len(payload['relationships'])}")
    if len(payload['relationships']) > 0:
        print(f"  -> First Relationship: {payload['relationships'][0]}")
        
    print(f"Graph Nodes Ready: {len(payload['graph_ready_payload']['nodes'])}")
    print(f"Graph Edges Ready: {len(payload['graph_ready_payload']['edges'])}")
    
    print("\nTest Complete!")

if __name__ == "__main__":
    test_intelligence_engine()
