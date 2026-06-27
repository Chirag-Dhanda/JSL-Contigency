import { MetadataService } from '../services/PlaceholderServices.js';
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
    await loadTemplates();
    await loadObjects();
});

async function loadTemplates() {
    const tbody = document.getElementById("templatesTableBody");
    try {
        const types = await MetadataService.getAllTypes();
        tbody.innerHTML = types.map(t => `
            <tr>
                <td><span class="badge">${t.type_id}</span></td>
                <td><i class="fa-solid ${t.icon || 'fa-cube'}"></i> ${t.display_name}</td>
                <td>${t.category}</td>
                <td>${t.status}</td>
            </tr>
        `).join("");
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="4" style="color:red">Failed to load templates.</td></tr>`;
    }
}

async function loadObjects() {
    const tbody = document.getElementById("objectsTableBody");
    try {
        // We use the search endpoint with empty query to fetch all objects
        const objects = await MetadataService.searchMetadata("");
        tbody.innerHTML = objects.map(o => `
            <tr>
                <td>${o.id || 'N/A'}</td>
                <td>${o.display_name} (${o.name})</td>
                <td><span class="badge">${o.entity_type}</span></td>
                <td>${o.created_by}</td>
            </tr>
        `).join("");
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="4" style="color:red">Failed to load objects.</td></tr>`;
    }
}
