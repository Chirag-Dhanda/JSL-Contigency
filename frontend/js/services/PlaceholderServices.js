// ========================================
// services/PlaceholderServices.js
// ========================================
import { fetchApi } from '../api/api.config.js';

export class MetadataService {
    static async getMetadata(entityId) {
        try { return await fetchApi(`/metadata/objects/${entityId}`); } 
        catch (e) { return { tags: ["mock-tag-1"], created: "2026-06-01" }; }
    }
    static async getAllTypes() {
        try { return await fetchApi(`/metadata/types`); }
        catch (e) { return [{type_id: "mock_type", display_name: "Mock Type", category: "General", status: "Active"}]; }
    }
    static async searchMetadata(query) {
        try { return await fetchApi(`/metadata/search?q=${query}`); }
        catch (e) { return [{name: "mock-obj", display_name: "Mock Object", entity_type: "mock_type"}]; }
    }
}

export class UserService {
    static async getUsers() {
        // Fallback to our existing mock if backend doesn't have a /users endpoint
        try { return await fetchApi(`/users`); }
        catch (e) { 
            const { demoUsers } = await import('../demo-data/users.js');
            return demoUsers; 
        }
    }
}

export class AIService {
    static async getRecommendations(userId) {
        try { return await fetchApi(`/ai/recommendations/${userId}`); } 
        catch (e) { return ["Safety 101", "Advanced SAP"]; }
    }
}

export class RelationshipService {
    static async getRelatedEntities(entityId) {
        try { return await fetchApi(`/relationships/${entityId}`); } 
        catch (e) { return []; }
    }
}

export class KnowledgeService {
    static async searchKnowledgeBase(query) {
        try { return await fetchApi(`/knowledge/search?q=${query}`); } 
        catch (e) { return []; }
    }
}

export class WorkflowService {
    static async getActiveWorkflows(userId) {
        try { return await fetchApi(`/workflows/active?user=${userId}`); } 
        catch (e) { return []; }
    }
}

export class SAPService {
    static async syncSAPData(module) {
        try { return await fetchApi(`/sap/sync/${module}`); } 
        catch (e) { return { status: "success", timestamp: Date.now() }; }
    }
}

export class LearningService {
    static async getModules() {
        try { return await fetchApi(`/learning/modules`); } 
        catch (e) { return [{ id: 1, title: "Plant Workflow Basics" }]; }
    }
}
