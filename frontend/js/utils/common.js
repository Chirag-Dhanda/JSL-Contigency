/*==========================================
        COMMON FUNCTIONS
==========================================*/

import { AuthService } from '../services/AuthService.js';

// Make logout available globally for inline onclick handlers if any
window.logout = function() {
    AuthService.logout();
};

export function logout() {
    AuthService.logout();
}

// Display Current Date
export function getCurrentDate() {
    const date = new Date();
    return date.toLocaleDateString("en-IN", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric"
    });
}

// Greeting
export function getGreeting() {
    const hour = new Date().getHours();
    if (hour < 12) return "Good Morning";
    if (hour < 17) return "Good Afternoon";
    return "Good Evening";
}

// Capitalize
export function capitalize(text) {
    if(!text) return "";
    return text.charAt(0).toUpperCase() + text.slice(1);
}