# AI Knowledge Pipeline

The Knowledge Pipeline transforms raw enterprise documents into AI-understandable vectors for Retrieval-Augmented Generation (RAG).

## 1. Document Upload & Authoring
Users author or upload documents via the `KnowledgeService`. Documents are instantiated as `KnowledgeObject`s and remain in a `DRAFT` status.

## 2. Validation & OCR
If a document is an image or PDF, it passes through the `ocr` module to extract raw text. The text is validated against minimum length and quality thresholds.

## 3. Parsing & Chunking
LLMs have fixed context windows. We cannot feed an entire 500-page SOP into the AI.
- The `chunking` module splits the document into smaller semantic chunks (e.g., 500 tokens).
- Overlap (e.g., 50 tokens) is used to ensure context isn't lost between chunk boundaries.

## 4. Embedding
The chunks are sent to the `EmbeddingPipeline`.
- We use the `nomic-embed-text` model running locally via Ollama.
- It transforms the text chunk into a high-dimensional mathematical vector (e.g., 768 dimensions).

## 5. Vector Storage
The vectors and their associated textual metadata are saved into the `ChromaDB` collection. The `KnowledgeObject` status is updated to `PUBLISHED`.

## 6. Retrieval & Context Injection
When a user asks a question (e.g., "What is the EAF safety protocol?"):
1. The question is embedded using the same `nomic-embed-text` model.
2. ChromaDB performs a similarity search (Cosine Similarity) to find the top 3 most mathematically similar chunks.
3. The `Orchestrator` injects those 3 text chunks into the `OllamaClient` prompt as context.
4. The LLM generates an answer strictly based on that retrieved context.
