// ========================================
// api/api.config.js
// ========================================

export const API_CONFIG = {
    BASE_URL: "http://localhost:8000/api/v1", // Future FastAPI base URL
    TIMEOUT: 5000
};

export async function fetchApi(endpoint, options = {}) {
    // 1. JWT Storage retrieval
    const token = sessionStorage.getItem("jwt_token");
    
    // 2. Authentication Headers
    const headers = {
        "Content-Type": "application/json",
        ...options.headers
    };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers
    };

    // 3. Request Wrapper with Retry Logic and Error Handling
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, config);
        
        // Handle common errors
        if (response.status === 401) {
            console.warn("[API Wrapper] 401 Unauthorized. Clearing token.");
            sessionStorage.removeItem("jwt_token");
            window.location.href = "/index.html"; // Adjust path as needed based on execution root
            throw new Error("Unauthorized");
        }
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.warn(`[API Wrapper] ${endpoint} failed. Using graceful fallback. Error:`, error.message);
        throw error; // Let the service layer catch this and provide the mock fallback
    }
}
