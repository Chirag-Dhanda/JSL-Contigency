import logging
import uuid
from typing import Dict, Any, List
from modules.metadata_engine.service import MetadataEngineService
from exceptions.base import SystemException

logger = logging.getLogger("MediaLibrary")

class MediaLibraryService:
    """
    Manages physical asset metadata (Images, PDFs, Videos) within the Entity Framework.
    """
    
    def __init__(self, metadata_engine: MetadataEngineService):
        self.metadata_engine = metadata_engine
        # Ensure the media_asset type exists in the registry
        # We assume it is registered during system startup.
        logger.info("Media Library Service Initialized.")

    def upload_asset(self, filename: str, content_type: str, file_size: int, uploaded_by: str, tags: List[str] = None) -> Dict[str, Any]:
        """
        Mocks the physical upload of a file and registers it as an Entity.
        In a real scenario, this would stream to S3/Blob Storage.
        """
        # Validate allowed types
        allowed_types = ["application/pdf", "image/png", "image/jpeg", "video/mp4"]
        if content_type not in allowed_types:
            raise SystemException(message=f"Unsupported media type: {content_type}")
            
        # Mock S3 URL generation
        file_id = str(uuid.uuid4())
        mock_url = f"https://enterprise-storage.internal.jsl/assets/{file_id}_{filename}"
        
        # Register as a dynamic entity
        metadata_payload = {
            "filename": filename,
            "content_type": content_type,
            "size_bytes": file_size,
            "storage_url": mock_url,
            "asset_tags": tags or []
        }
        
        # We use the metadata engine to create the entity, enforcing standard validation
        try:
            entity = self.metadata_engine.create_entity(
                name=f"asset-{file_id[:8]}",
                entity_type="media_asset", # Must be registered in EntityRegistry
                display_name=filename,
                created_by=uploaded_by,
                metadata=metadata_payload
            )
            logger.info(f"Media Asset '{filename}' uploaded and registered as {entity.id}")
            return entity
        except Exception as e:
            logger.error(f"Failed to register media asset: {e}")
            raise SystemException(message="Failed to register media asset entity.")
