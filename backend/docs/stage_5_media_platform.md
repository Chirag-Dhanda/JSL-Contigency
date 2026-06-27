# Stage 5.7: Enterprise Media Platform (DAM)

This document outlines the architecture for the Enterprise Digital Asset Management platform, which elevates basic file uploads into intelligent, version-controlled Knowledge Graph entities.

## 1. Asset Management (`modules/media_platform/`)
The `MediaPlatformService` manages the lifecycle of a `MediaAsset`. Instead of just storing files, each upload registers a new asset.
- **Version Control**: When a user uploads a new file over an existing asset (e.g., updating a CAD blueprint), the platform generates a new `AssetVersion` record, tracking the filesize, uploader, timestamp, and generating a distinct storage path.
- **Search & Filtering**: Assets can be queried by type, tags, or semantic AI keywords.

## 2. AI Asset Intelligence (`modules/media_ai/`)
As soon as a file is uploaded, the `MediaAIIntelligenceService` runs inference on it.
- **Keyword Extraction**: It reads textual or visual context to extract high-value semantic keywords.
- **Tagging**: It proposes business tags (e.g., "Safety", "EAF", "Equipment") to classify the asset.
- **Relationship Discovery**: Like the Document Intake pipeline, it infers graph edges. For instance, if an incident photo is named `Pump_Failure.jpg`, the AI suggests linking it to the specific Pump equipment entity.

## 3. Thumbnail Engine (`modules/thumbnail_engine/`)
The `ThumbnailEngineService` is responsible for generating visual previews for all assets, ensuring the Media Library looks highly polished and professional. It handles generation logic for PDFs, Images, Videos, and CAD files.

## 4. Frontend Media Library (`modules/media_library/`)
- **MediaLibraryLayout**: A high-performance gallery view allowing users to quickly filter thousands of assets by file type (PDF, CAD, Video) or AI tags.
- **AssetPreviewModal**: Clicking any asset opens a rich preview modal. This modal displays not only the visual thumbnail but all underlying AI metadata, keywords, versions, and hyperlinked connections into the deeper Knowledge Graph.

## 5. Storage Strategy
For this implementation, storage paths are simulated (`mock_storage/asset-id/v1/...`). In production, this architecture will seamlessly connect to an S3 or Azure Blob Storage bucket for true binary storage.
