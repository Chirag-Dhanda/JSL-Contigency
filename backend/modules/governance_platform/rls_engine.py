"""
Row-Level Security Engine (EP-09).
Python-level predicate injection before SQLAlchemy queries.
Future: push to PostgreSQL-native RLS via session variables.
"""
import logging
from typing import List, Optional, Any
from sqlalchemy import and_, or_, Column

from .models import RLSContext, RLSFilter, ClassificationLevel, CLASSIFICATION_RANK

logger = logging.getLogger("Governance.RLSEngine")


class RowLevelSecurityEngine:
    """
    Generates filter predicates based on user context.
    Applied by services before executing queries — never bypassed.
    
    EP-09 implementation: Python-level filter injection (SQLAlchemy where-clauses).
    Future EP: Migrate to PostgreSQL-native RLS policies.
    """

    def build_filters(self, context: RLSContext) -> List[RLSFilter]:
        """
        Builds the set of RLS filter predicates for the given user context.
        """
        filters: List[RLSFilter] = []

        # 1. Classification ceiling — only return assets at or below user's clearance
        max_rank = CLASSIFICATION_RANK.get(context.max_classification, 1)
        filters.append(RLSFilter(
            filter_type="CLASSIFICATION_MAX",
            column="classification",
            operator="rank_lte",
            value=max_rank
        ))

        # 2. Department isolation — by default, restrict to own department
        # unless user has ADMIN or CROSS_DEPT roles
        admin_roles = {"ADMIN", "SYSTEM", "SECURITY_OFFICER", "KNOWLEDGE_MANAGER"}
        user_roles_upper = {r.upper() for r in context.roles}
        if context.department_id and not (user_roles_upper & admin_roles):
            filters.append(RLSFilter(
                filter_type="DEPT_MATCH",
                column="department_id",
                operator="eq",
                value=context.department_id
            ))

        return filters

    def apply_to_knowledge(self, filters: List[RLSFilter], base_query: Any) -> Any:
        """
        Applies RLS filters to a knowledge asset SQLAlchemy query.
        
        Usage:
            filtered_q = rls_engine.apply_to_knowledge(filters, db.query(DbKnowledgeAsset))
        
        For EP-09, returns the query with Python-evaluated conditions.
        The actual SQLAlchemy model columns must be passed from the calling service.
        """
        logger.debug(f"Applying {len(filters)} RLS filters to knowledge query.")
        # Filters are applied by service layer by inspecting filter.filter_type and filter.column
        # This engine exposes the filters as metadata; services apply them via .where() clauses
        return base_query, filters

    def should_allow_cross_dept(self, user_roles: List[str]) -> bool:
        """Returns True if the user's roles permit cross-department data access."""
        admin_roles = {"ADMIN", "SYSTEM", "SECURITY_OFFICER", "KNOWLEDGE_MANAGER"}
        return bool(admin_roles & {r.upper() for r in user_roles})

    def resolve_user_clearance(self, user_roles: List[str]) -> ClassificationLevel:
        """Returns the maximum ClassificationLevel the user is permitted to access."""
        ROLE_CLEARANCE = {
            "ADMIN": ClassificationLevel.EXPORT_CONTROLLED,
            "SECURITY_OFFICER": ClassificationLevel.EXPORT_CONTROLLED,
            "KNOWLEDGE_MANAGER": ClassificationLevel.HIGHLY_CONFIDENTIAL,
            "MANAGER": ClassificationLevel.CONFIDENTIAL,
            "SUPERVISOR": ClassificationLevel.RESTRICTED,
            "USER": ClassificationLevel.INTERNAL,
            "VIEWER": ClassificationLevel.PUBLIC,
        }
        user_roles_upper = {r.upper() for r in user_roles}
        best = ClassificationLevel.PUBLIC
        best_rank = 0
        for role in user_roles_upper:
            level = ROLE_CLEARANCE.get(role, ClassificationLevel.INTERNAL)
            rank = CLASSIFICATION_RANK.get(level, 0)
            if rank > best_rank:
                best = level
                best_rank = rank
        return best
