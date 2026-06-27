# Enterprise RAG Architecture

## Overview
Implementation Plan 4.3 establishes the Enterprise RAG (Retrieval-Augmented Generation) Architecture. The goal is to ensure the AI never hallucinates manufacturing details by forcing it to retrieve truth from trusted internal knowledge bases before answering.

## 1. Vector Database Abstraction
Because the choice of Vector DB (e.g., Chroma, Qdrant, pgvector) may change as the enterprise scales, the `VectorDatabaseManager` acts as an abstract interface. All persistence and similarity searches are routed through this layer, allowing seamless migration in the future.

## 2. Knowledge Collections
To prevent cross-contamination of search results (e.g., pulling an HR policy when searching for a blast furnace SOP), knowledge is segmented into configurable `KnowledgeCollection` enums:
- `MANUFACTURING`
- `SAFETY`
- `SOP`
- `EQUIPMENT`
- `POLICIES`

## 3. Strict Metadata Security
Every vector stored must carry a `DocumentMetadata` payload. This ensures that every chunk of text retains its organizational origin. 
The `RetrievalSecurity` framework intercepts the raw search results *before* the AI sees them. It evaluates the metadata against the user's requesting profile. If a chunk belongs to `department="HR"` with `security_level=5` and the requesting user is a Level 1 Intern, the chunk is silently dropped from the retrieval pipeline.

## 4. The RAG Engine
The `RAGEngine` is the public API for the AI Router. It executes the retrieval pipeline and wraps the authorized passages into an `AIContextPackage`. This package contains the raw text, the similarity score, and the original document source string. 

## 5. Integration with the AI Gateway
In future stages, the `AIContextPackage.format_for_prompt()` will be injected into the `PromptEngine`, effectively providing the LLM with the context string: `--- RELEVANT INTERNAL KNOWLEDGE --- [1] Source: res-eaf-001...` allowing it to generate highly accurate, locally cited answers.
