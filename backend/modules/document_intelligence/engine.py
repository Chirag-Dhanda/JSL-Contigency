import logging
from typing import Dict, Any

from modules.document_intelligence.classifier import DocumentClassifier
from modules.document_intelligence.relationships import EntityRelationshipDetector
from modules.document_intelligence.summarizer import DocumentSummarizer
from modules.document_intelligence.generator import QuestionGenerator
from modules.document_intelligence.graph_prep import GraphPreparer
from modules.document_analysis.analyzer import ContentAnalyzer
from modules.knowledge_extraction.extractor import KnowledgeExtractor

logger = logging.getLogger("DocumentIntelligenceEngine")

class DocumentIntelligenceEngine:
    """
    The orchestrator that runs the entire document understanding pipeline.
    Intercepts parsed text before it hits the chunking/indexing pipeline.
    """
    
    def __init__(self):
        self.classifier = DocumentClassifier()
        self.analyzer = ContentAnalyzer()
        self.extractor = KnowledgeExtractor()
        self.relationships = EntityRelationshipDetector()
        self.summarizer = DocumentSummarizer()
        self.generator = QuestionGenerator()
        self.graph_prep = GraphPreparer()

    def process_document(self, raw_text: str, document_id: str) -> Dict[str, Any]:
        """
        Runs the full intelligence suite on a single document.
        """
        logger.info(f"Starting Intelligence Processing for Document {document_id}")
        
        # 1. Classification
        doc_class = self.classifier.classify(raw_text)
        
        # 2. Structural Analysis
        structure = self.analyzer.analyze_structure(raw_text)
        
        # 3. Knowledge Extraction (For mock purposes, defaulting to Section: Body)
        entities = self.extractor.extract_entities(raw_text, document_id)
        
        # 4. Relationship Detection
        relations = self.relationships.detect_relationships(entities, doc_class)
        
        # 5. Summarization & Generation (Prepared structures)
        summaries = self.summarizer.generate_summaries(raw_text)
        questions = self.generator.generate_questions(raw_text)
        
        # 6. Graph Preparation
        graph_payload = self.graph_prep.prepare_graph_payload(entities, relations)
        
        logger.info("Intelligence Processing Complete.")
        
        return {
            "document_id": document_id,
            "classification": doc_class,
            "structure": structure,
            "extracted_entities": [e.dict() for e in entities],
            "relationships": relations,
            "summaries": summaries,
            "questions": questions,
            "graph_ready_payload": graph_payload
        }
