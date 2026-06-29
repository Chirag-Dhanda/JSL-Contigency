"""
Citation Injection Engine (EP-08).
Injects enterprise citations from the ContextPackage into the final AI response.
"""
import logging
from typing import List, Dict, Any, Optional

from modules.search_engine.models import ContextPackage

logger = logging.getLogger("AIPlatform.Citations")


class CitationInjectionEngine:
    """
    Maps Source labels (e.g. [Source 1]) in the AI response to formal Citation objects.
    Returns a structured list of citations for the client.
    """

    def inject(
        self,
        response_text: str,
        context_package: Optional[ContextPackage]
    ) -> tuple[str, List[Dict[str, Any]]]:
        """
        Returns (annotated_text, citation_list).
        Currently preserves the response as-is and returns structured citations.
        Future: link [Source N] inline markers to clickable enterprise references.
        """
        if not context_package or not context_package.citations:
            return response_text, []

        structured_citations = []
        for i, citation in enumerate(context_package.citations):
            structured_citations.append({
                "source_index": i + 1,
                "citation_id": citation.citation_id,
                "asset_id": citation.asset_id,
                "asset_title": citation.asset_title,
                "chunk_id": citation.chunk_id,
                "relevance_score": round(citation.relevance_score, 4),
                "timestamp": citation.timestamp.isoformat()
            })

        # Append citation list as a structured footer
        if structured_citations:
            footer_lines = ["\n\n---\n**Enterprise Sources:**"]
            for c in structured_citations:
                footer_lines.append(
                    f"[Source {c['source_index']}] {c['asset_title']} "
                    f"(Relevance: {c['relevance_score']})"
                )
            annotated_text = response_text + "\n".join(footer_lines)
        else:
            annotated_text = response_text

        return annotated_text, structured_citations
