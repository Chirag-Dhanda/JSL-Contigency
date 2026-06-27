// ========================================
// controllers/login.controller.js
// ========================================

import { AuthService } from '../services/AuthService.js';

document.getElementById("loginForm").addEventListener("submit", async function(e){
    e.preventDefault();
    
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    try {
        const user = await AuthService.login(email, password);
        if(user) {
            window.location.href = "pages/dashboard/dashboard.html";
        }
    } catch (error) {
        alert(error.message || "Invalid Email or Password");
    }
});