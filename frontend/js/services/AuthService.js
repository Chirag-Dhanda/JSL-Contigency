// ========================================
// services/AuthService.js
// ========================================

import { fetchApi } from '../api/api.config.js';
import { demoUsers } from '../demo-data/users.js';

export class AuthService {
    static async login(username, password) {
        try {
            // Attempt to use real API first
            const response = await fetchApi("/auth/login", {
                method: "POST",
                body: JSON.stringify({ username, password })
            });
            
            // Backend AuthResponse parsing
            if (response.access_token) {
                sessionStorage.setItem("jwt_token", response.access_token);
                // Create a generic user object since our backend AuthResponse doesn't return full user details yet
                const user = { username: username, role: username === "admin" ? "superadmin" : "engineer" };
                sessionStorage.setItem("user", JSON.stringify(user));
                return user;
            }
            throw new Error("Missing token in response");
        } catch (error) {
            // Fallback to Demo Data
            console.log("[AuthService] Falling back to demo data login.");
            const foundUser = demoUsers.find(user => 
                (user.email === username || user.username === username) && user.password === password
            );
            
            if (foundUser) {
                // Simulate JWT token
                sessionStorage.setItem("jwt_token", "demo_token_12345");
                sessionStorage.setItem("user", JSON.stringify(foundUser));
                return foundUser;
            }
            throw new Error("Invalid Email or Password");
        }
    }

    static logout() {
        sessionStorage.clear();
        window.location.href = "../../index.html"; // Adjust based on calling page
    }

    static getCurrentUser() {
        return JSON.parse(sessionStorage.getItem("user"));
    }
}
