APPROVAL_RULES = {
    "manager": 10000,
    "director": 50000,
    "cfo": 200000,
    "board": float("inf")
}

DEPARTMENT_BUDGETS = {
    "Marketing": {"total": 120000, "spent": 134500, "available": 0},
    "Operations": {"total": 500000, "spent": 487200, "available": 12800},
    "IT": {"total": 80000, "spent": 45000, "available": 35000},
    "HR": {"total": 60000, "spent": 38000, "available": 22000}
}

SAMPLE_INVOICES = [
    {
        "id": "INV-2025-001",
        "vendor": "Salesforce Inc.",
        "department": "IT",
        "amount": 28000,
        "description": "CRM annual license renewal",
        "submitted_by": "John Martinez"
    },
    {
        "id": "INV-2025-002",
        "vendor": "Google Ads",
        "department": "Marketing",
        "amount": 15000,
        "description": "Q1 digital advertising campaign",
        "submitted_by": "Sarah Chen"
    },
    {
        "id": "INV-2025-003",
        "vendor": "AWS",
        "department": "Operations",
        "amount": 8500,
        "description": "Cloud infrastructure - January",
        "submitted_by": "Mike Torres"
    }
]