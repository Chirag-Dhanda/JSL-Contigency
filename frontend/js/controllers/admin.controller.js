import { UserService } from '../services/PlaceholderServices.js';
import { AuthService } from '../services/AuthService.js';

document.addEventListener("DOMContentLoaded", async () => {
    // Auth Check
    const user = AuthService.getCurrentUser();
    if (!user) {
        window.location.href = "../../index.html";
        return;
    }
    document.getElementById("userNameDisplay").textContent = user.username || user.email || "Admin";

    // Load Data
    await loadUsers();
});

async function loadUsers() {
    const tbody = document.getElementById("usersTableBody");
    try {
        const users = await UserService.getUsers();
        tbody.innerHTML = users.map(u => `
            <tr>
                <td>${u.id || Math.floor(Math.random()*10000)}</td>
                <td><i class="fa-solid fa-user" style="margin-right:8px; color:var(--text-secondary)"></i> ${u.name || u.username || 'System User'}</td>
                <td>${u.email}</td>
                <td><span class="badge-role">${u.role || u.roles?.[0] || 'Employee'}</span></td>
                <td>${u.department || 'General'}</td>
            </tr>
        `).join("");
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="5" style="color:red">Failed to load users.</td></tr>`;
    }
}
