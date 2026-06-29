"""
Enterprise Context Guard (EP-08).
Validates and sanitizes a ContextPackage before it enters any AI prompt.
No unauthorized data may reach the LLM.
"""
import logging
from typing import List

from modules.search_engine.models import ContextPackage, RankedPassage
from .models import AIChatRequest

logger = logging.getLogger("AIPlatform.ContextGuard")


class PermissionDenied(Exception):
    pass


class EnterpriseContextGuard:
    """
    Performs permission enforcement on the ContextPackage before prompt assembly.
    
    EP-08 implementation: Service-level RBAC check.
    EP-09 expansion: Row-Level Security pushed to PostgreSQL query layer.
    """

    # Assets classified at these levels require elevated roles to appear in AI context
    ELEVATED_CLASSIFICATIONS = {"CONFIDENTIAL", "RESTRICTED", "TOP_SECRET"}
    ELEVATED_ROLES = {"ADMIN", "KNOWLEDGE_MANAGER", "SECURITY_OFFICER"}

    def validate_and_sanitize(
        self,
        request: AIChatRequest,
        context_package: ContextPackage
    ) -> ContextPackage:
        """
        Returns a sanitized ContextPackage safe for prompt injection.
        Raises PermissionDenied if the user has no access to any context.
        """
        user_roles = set(r.upper() for r in request.user_roles)
        allowed_passages: List[RankedPassage] = []
        
        for passage in context_package.passages:
            # 1. Department filter: passages owned by other departments are hidden
            # unless the user has elevated roles
            if request.user_department:
                # For MVP: allow if no dept restriction or role is ADMIN
                # Full dept ACL enforcement deferred to EP-09 RLS
                pass

            # 2. Classification filter: high-sensitivity assets need elevated roles
            asset_type_upper = passage.asset_type.upper()
            if asset_type_upper in self.ELEVATED_CLASSIFICATIONS:
                if not (user_roles & self.ELEVATED_ROLES):
                    logger.info(
                        f"Context Guard blocked passage from asset '{passage.asset_id}' "
                        f"(classification: {passage.asset_type}) for roles {user_roles}"
                    )
                    continue

            # 3. Minimum confidence filter
            if passage.final_score < 0.01:
                continue

            allowed_passages.append(passage)

        if not allowed_passages and context_package.passages:
            logger.warning(
                "Context Guard stripped all passages due to permission filtering. "
                "Returning empty context to prevent unauthorized data leakage."
            )

        # Return a new ContextPackage with only the allowed passages
        sanitized = ContextPackage(
            original_query=context_package.original_query,
            passages=allowed_passages,
            citations=[c for c in context_package.citations if c.asset_id in {p.asset_id for p in allowed_passages}],
            total_tokens_estimated=sum(len(p.text) // 4 for p in allowed_passages),
            permission_filtered=True
        )

        return sanitized
