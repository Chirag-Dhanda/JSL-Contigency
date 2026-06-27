// ========================================
// components/roleManager.js
// ========================================

export function getRolePermissions(role) {
    const permissions = {
        superadmin: [
            "Dashboard",
            "User Management",
            "Organization Settings",
            "System Audit",
            "AI Platform Settings",
            "Metadata Schema"
        ],
        admin: [
            "Dashboard",
            "Employee Directory",
            "Learning Content",
            "Department Configuration",
            "Reports"
        ],
        manager: [
            "Dashboard",
            "My Team",
            "Team Training",
            "Approvals"
        ],
        supervisor: [
            "Dashboard",
            "Shift Reports",
            "Line Performance",
            "Safety Incidents"
        ],
        engineer: [
            "Dashboard",
            "System Diagnostics",
            "Equipment Maintenance",
            "SOPs"
        ],
        executive: [
            "Dashboard",
            "Company KPIs",
            "Financial Reports",
            "Strategic Overview"
        ],
        operator: [
            "Dashboard",
            "My Workflows",
            "Machine Manuals",
            "Safety Guidelines"
        ],
        intern: [
            "Dashboard",
            "Onboarding Tasks",
            "Training Modules",
            "Company Policies"
        ]
    };
    
    // Default to a basic set if role is not strictly defined
    return permissions[role] || [
        "Dashboard",
        "My Profile",
        "Company Resources"
    ];
}