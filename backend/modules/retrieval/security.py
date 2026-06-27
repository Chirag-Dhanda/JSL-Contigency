import logging
from typing import List, Dict, Any
from modules.knowledge_index.metadata import DocumentMetadata

logger = logging.getLogger("RetrievalSecurity")

class RetrievalSecurity:
    """Enforces role and security-level constraints on retrieved knowledge."""
    
    def filter_authorized_results(self, 
                                  raw_results: List[Dict[str, Any]], 
                                  user_department: str, 
                                  user_roles: List[str], 
                                  user_clearance_level: int) -> List[Dict[str, Any]]:
        """
        Iterates over vector search results and drops documents the user isn't allowed to see.
        """
        authorized = []
        for result in raw_results:
            meta_dict = result.get("metadata", {})
            
            try:
                # Simulate parsing into our strict metadata model
                meta = DocumentMetadata(**meta_dict)
                
                # 1. Security Level Check
                if meta.security_level > user_clearance_level:
                    logger.debug(f"Dropped doc {meta.document_source} due to security level.")
                    continue
                    
                # 2. Department Check (if restricted)
                if meta.department != "global" and meta.department != user_department:
                    logger.debug(f"Dropped doc {meta.document_source} due to department mismatch.")
                    continue
                    
                # 3. Role Check (if restricted)
                if meta.role_access and "all" not in [r.lower() for r in meta.role_access]:
                    has_role = any(role in meta.role_access for role in user_roles)
                    if not has_role:
                        logger.debug(f"Dropped doc {meta.document_source} due to role mismatch.")
                        continue
                        
                authorized.append(result)
            except Exception as e:
                logger.error(f"Failed to parse metadata for authorization check: {e}")
                # Fail closed
                continue
                
        return authorized
