// ========================================
// services/DashboardService.js
// ========================================

import { fetchApi } from '../api/api.config.js';
import { departmentData, equipmentData, knowledgeDocs } from '../demo-data/departments.js';

export class DashboardService {
    static async getDashboardCards(role) {
        try {
            return await fetchApi(`/dashboard/cards?role=${role}`);
        } catch (error) {
            console.log("[DashboardService] Falling back to demo data for cards.");
            let cards = [];
            switch(role){
                case "superadmin":
                case "executive":
                    cards = [
                        "Metadata Engine", "User Directory", "Manufacturing Equipment",
                        "Knowledge Studio", "AI Platform", "Audit Logs"
                    ];
                    break;
                case "admin":
                    cards = [
                        "Employee Directory", "Learning Programs", "Training Reports",
                        "SOPs & Policies", "Department Workflow", "SAP Module"
                    ];
                    break;
                case "manager":
                    cards = [
                        "My Team", "Assign Learning", "Training Progress",
                        "Equipment Status", "Shift Reports", "Assessments"
                    ];
                    break;
                case "supervisor":
                    cards = [
                        "Shift Schedule", "Line Performance", "Team Training",
                        "Safety Audits", "PTW System", "Checklist Records"
                    ];
                    break;
                case "engineer":
                    cards = [
                        "My Assignments", "SOPs Library", "Equipment Manuals",
                        "Maintenance Logs", "SAP Learning", "Assessment"
                    ];
                    break;
                default:
                    cards = [
                        "Company Overview", "Plant Workflow", "SOPs & Policies",
                        "SAP Learning", "Assessment", "Certificates"
                    ];
            }
            return cards;
        }
    }

    static async getDepartmentData(department, role) {
        try {
            return await fetchApi(`/dashboard/departments?dept=${department}`);
        } catch (error) {
            console.log("[DashboardService] Falling back to demo data for departments.");
            if (role === "superadmin" || role === "executive") {
                return departmentData;
            } else {
                return {
                    [department]: departmentData[department] || { icon: "fa-building", desc: "General Department Information." }
                };
            }
        }
    }

    static async getEquipmentStatus() {
        try {
            return await fetchApi(`/metadata/search?q=machine`);
        } catch (error) {
            console.log("[DashboardService] Falling back to demo equipment list.");
            return equipmentData;
        }
    }

    static async getKnowledgeDocuments() {
        try {
            return await fetchApi(`/metadata/search?q=sop`);
        } catch (error) {
            console.log("[DashboardService] Falling back to demo knowledge docs.");
            return knowledgeDocs;
        }
    }

    static async getDashboardStats() {
        let stats = { equipment: 0, sops: 0, users: 0 };
        try {
            const [eq, docs] = await Promise.all([
                DashboardService.getEquipmentStatus(),
                DashboardService.getKnowledgeDocuments()
            ]);
            stats.equipment = Array.isArray(eq) ? eq.length : 12;
            stats.sops = Array.isArray(docs) ? docs.length : 8;
            stats.users = 10;
        } catch {
            stats = { equipment: 12, sops: 8, users: 10 };
        }
        return stats;
    }
}
