import logging
from modules.media_platform.service import MediaPlatformService
from modules.media_platform.models import MediaFilter
from modules.thumbnail_engine.service import ThumbnailEngineService
from modules.media_ai.service import MediaAIIntelligenceService

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    print("=========================================================")
    print("STARTING STAGE 5.7 VALIDATION: MEDIA PLATFORM")
    print("=========================================================")
    
    media_service = MediaPlatformService()
    ai_service = MediaAIIntelligenceService()
    thumb_service = ThumbnailEngineService()
    
    print("\n--- 1. Simulating Media Uploads ---")
    
    uploads = [
        {"file": "Furnace_Pump_Blueprint.pdf", "type": "application/pdf"},
        {"file": "Safety_Incident_04.jpg", "type": "image/jpeg"},
        {"file": "EAF_Training_Video.mp4", "type": "video/mp4"}
    ]
    
    for u in uploads:
        # 1. Register
        asset = media_service.register_asset(filename=u["file"], file_type=u["type"], owner="u-system", file_size=1024*1024)
        
        # 2. AI Intelligence
        ai_res = ai_service.analyze_asset(asset)
        asset = media_service.update_metadata(asset.id, tags=ai_res["suggested_tags"], keywords=ai_res["keywords"])
        
        # 3. Thumbnail
        thumb = thumb_service.generate_thumbnail(asset)
        print(f"[OK] Asset {asset.id} Processed | Thumb: {thumb} | Tags: {asset.tags}")
        
    print(f"\n--- 2. Verifying Media Search ---")
    filter_params = MediaFilter(tags=["Safety"])
    results = media_service.search_assets(filter_params)
    print(f"[OK] Search for 'Safety' returned {len(results)} assets.")
    assert len(results) > 0, "Expected at least 1 asset with Safety tag."
    
    print(f"\n--- 3. Verifying Version Management ---")
    # Take the first asset and update it
    asset_to_update = list(media_service._assets.values())[0]
    updated_asset = media_service.add_new_version(
        asset_id=asset_to_update.id, 
        file_size=2048*1024, 
        uploader="u-engineer", 
        summary="Added new dimensions"
    )
    
    print(f"[OK] Asset {updated_asset.id} updated to Version {updated_asset.current_version}")
    assert len(updated_asset.versions) == 2, "Expected 2 versions in the history."
    
    print("\n=========================================================")
    print("VALIDATION SUCCESSFUL: MEDIA PLATFORM IS OPERATIONAL")
    print("=========================================================")

if __name__ == "__main__":
    main()
