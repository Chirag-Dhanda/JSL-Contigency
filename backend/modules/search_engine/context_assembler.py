"""
Context Assembly Engine (EP-06).
Deduplicates, compresses, and generates Citations for the final Context Package.
"""
import logging
from typing import List
from .models import RankedPassage, Citation, ContextPackage, SearchRequest

logger = logging.getLogger("SearchEngine.ContextAssembler")


class ContextAssemblyEngine:
    def __init__(self, chars_per_token_estimate: float = 4.0):
        self.chars_per_token = chars_per_token_estimate

    def assemble(self, request: SearchRequest, passages: List[RankedPassage], max_tokens: int = 4000) -> ContextPackage:
        # 1. Deduplicate (by chunk id)
        seen_chunks = set()
        unique_passages: List[RankedPassage] = []
        for p in passages:
            if p.id not in seen_chunks:
                unique_passages.append(p)
                seen_chunks.add(p.id)

        # 2. Compress (Token Estimation & Truncation)
        current_tokens = 0
        final_passages: List[RankedPassage] = []
        citations: List[Citation] = []

        for p in unique_passages:
            estimated_tokens = len(p.text) / self.chars_per_token
            if current_tokens + estimated_tokens > max_tokens:
                logger.info(f"Context window full. Truncating at {len(final_passages)} passages.")
                break
            
            current_tokens += estimated_tokens
            final_passages.append(p)
            
            # Generate Citation
            citations.append(Citation(
                asset_id=p.asset_id,
                asset_title=p.asset_title,
                chunk_id=p.id,
                relevance_score=p.final_score
            ))

        # 3. Assemble Package
        pkg = ContextPackage(
            original_query=request.query,
            passages=final_passages,
            citations=citations,
            total_tokens_estimated=int(current_tokens),
            permission_filtered=True # assumed applied before this stage
        )

        logger.info(f"[{pkg.package_id}] Assembled Context Package with {len(final_passages)} passages "
                    f"(~{int(current_tokens)} tokens).")
        return pkg
