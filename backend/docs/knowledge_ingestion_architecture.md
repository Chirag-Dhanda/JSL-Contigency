# Enterprise Knowledge Ingestion & Indexing Pipeline

## Overview
Implementation Plan 4.4 establishes the automated workflow for digesting organizational knowledge (SOPs, Manuals, Policies) and transforming it into strictly-typed vector embeddings. This pipeline acts as the sole entry point for new AI knowledge, guaranteeing consistency, security stamping, and quality control.

## The Ingestion Lifecycle

1. **Ingestion & Validation (`modules/ingestion`)**
   - The `IngestionEngine` receives the upload and immediately spawns a `ProcessingMonitor` job.
   - The `DocumentValidator` enforces safety rules (checking MIME types, rejecting unsupported extensions like `.exe`, and enforcing size limits).

2. **Parsing & Cleaning (`modules/document_processing`)**
   - A specific parser (e.g., `PDFParser` or `MarkdownParser`) extracts the raw string data.
   - The `MetadataExtractor` queries the file's system properties to populate the `DocumentMetadata` model (enforcing roles and department tags).
   - The `ContentCleaner` runs aggressive regex sweeps to normalize unicode, delete extraneous whitespace, and strip headers/footers (e.g., "Page 1 of 5"), preventing the AI from ingesting noise.

3. **OCR Fallback (`modules/ocr`)**
   - If a parser (like PDF) extracts zero string characters but detects heavy byte volume, it recognizes a scanned image and defers to the `OCREngine` framework to attempt visual text extraction.

4. **Chunking Engine (`modules/chunking`)**
   - The cleaned monolithic document string is sliced into smaller `DocumentChunk` objects (e.g., 500 words each with a 50-word overlap to preserve semantic context across chunk boundaries).
   - *Crucially*, the `DocumentMetadata` is stamped onto *every single chunk*. If a 100-page SOP is chunked into 1,000 vectors, all 1,000 vectors individually carry the security clearance tags.

5. **Indexing Pipeline (`modules/indexing`)**
   - The final chunks are batched and sent to the `EmbeddingEngine` (which acts as a bridge to Ollama).
   - The resulting vector arrays, along with the text and metadata, are committed to the `VectorDatabaseManager`.
   - The `ProcessingMonitor` is marked as `COMPLETED`.

## Future Integration
In future phases, the `IngestionEngine` will hook into SAP to automatically ingest and update SOPs whenever a new transaction or document revision is detected in the ERP system.
