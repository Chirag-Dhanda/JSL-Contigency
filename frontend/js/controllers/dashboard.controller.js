/*==========================================
        DASHBOARD CONTROLLER
==========================================*/
import { AuthService } from '../services/AuthService.js';
import { DashboardService } from '../services/DashboardService.js';
import { getRolePermissions } from '../components/roleManager.js';
import { getCurrentDate, getGreeting, capitalize, logout } from '../utils/common.js';

document.addEventListener("DOMContentLoaded", async () => {
    // ----- Auth guard -----
    const user = AuthService.getCurrentUser();
    if (!user) {
        window.location.href = "../../index.html";
        return;
    }

    // ----- Populate header -----
    const nameDisplay = user.name || user.username || "Enterprise User";
    const roleDisplay = capitalize(user.role || "Employee");
    document.getElementById("welcomeName").innerHTML = `${getGreeting()}, ${nameDisplay}`;
    const profileName = document.getElementById("profileName");
    if (profileName) profileName.innerHTML = nameDisplay;
    document.getElementById("roleName").innerHTML = roleDisplay;
    document.getElementById("currentDate").innerHTML = getCurrentDate();

    // ----- Logout -----
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) logoutBtn.addEventListener("click", logout);

    // ----- Stat Strip -----
    loadStats();

    // ----- Equipment Table -----
    loadEquipment();

    // ----- Knowledge Docs Table -----
    loadDocs();

    // ----- Role-based Cards -----
    const roleContainer = document.getElementById("roleWidgets");
    const roleSection = document.getElementById("roleWidgetSection");
    if (roleContainer && roleSection) {
        const cards = await DashboardService.getDashboardCards(user.role);
        if (cards && cards.length) {
            roleSection.style.display = "";
            cards.forEach(card => {
                roleContainer.innerHTML += `
                <div class="workspace-card">
                    <i class="fa-solid fa-layer-group"></i>
                    <h3>${card}</h3>
                </div>`;
            });
        }
    }

    // ----- Department Cards (superadmin / exec only) -----
    const deptSection = document.getElementById("departmentSection");
    const deptContainer = document.getElementById("departmentCards");
    if (deptContainer && deptSection && (user.role === "superadmin" || user.role === "executive")) {
        deptSection.style.display = "";
        const depData = await DashboardService.getDepartmentData(user.department, user.role);
        Object.keys(depData).forEach(dep => {
            deptContainer.innerHTML += `
            <div class="department-card">
                <i class="fa-solid ${depData[dep].icon}"></i>
                <h3>${dep}</h3>
                <p>${depData[dep].desc}</p>
            </div>`;
        });
    }
});

async function loadStats() {
    try {
        const { MetadataService } = await import('../services/PlaceholderServices.js');
        const stats = await DashboardService.getDashboardStats();
        const types = await MetadataService.getAllTypes().catch(() => []);
        
        document.getElementById("statEquipment").textContent = stats.equipment;
        document.getElementById("statDocs").textContent = stats.sops;
        document.getElementById("statUsers").textContent = stats.users;
        document.getElementById("statTemplates").textContent = types.length || 3;
    } catch (e) {
        document.getElementById("statEquipment").textContent = "12";
        document.getElementById("statDocs").textContent = "8";
        document.getElementById("statUsers").textContent = "10";
        document.getElementById("statTemplates").textContent = "3";
    }
}

async function loadEquipment() {
    const tbody = document.getElementById("equipmentTableBody");
    try {
        const list = await DashboardService.getEquipmentStatus();
        tbody.innerHTML = list.map(eq => `
            <tr>
                <td>${eq.name}</td>
                <td>${eq.display || eq.display_name || eq.name}</td>
                <td>${eq.dept || eq.entity_type || "—"}</td>
                <td>${eq.plant || (eq.metadata && eq.metadata.plant) || "—"}</td>
                <td class="${(eq.status || "Active") === "Active" ? "status-active" : "status-maintenance"}">
                    ${eq.status || (eq.metadata && eq.metadata.status) || "Active"}
                </td>
            </tr>
        `).join("");
    } catch {
        tbody.innerHTML = `<tr><td colspan="5">Failed to load equipment.</td></tr>`;
    }
}

async function loadDocs() {
    const tbody = document.getElementById("docsTableBody");
    try {
        const list = await DashboardService.getKnowledgeDocuments();
        tbody.innerHTML = list.map(doc => `
            <tr>
                <td>${doc.name}</td>
                <td>${doc.display || doc.display_name || doc.name}</td>
                <td>${doc.type || (doc.metadata && doc.metadata.doc_type) || doc.entity_type || "—"}</td>
                <td>${doc.dept || "—"}</td>
            </tr>
        `).join("");
    } catch {
        tbody.innerHTML = `<tr><td colspan="4">Failed to load documents.</td></tr>`;
    }
}