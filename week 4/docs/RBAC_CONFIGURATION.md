# RBAC Configuration Guide
**Author:** Sri Saranya Chandrapati

## 1. Role Hierarchy Diagram
```ascii
      Level 100: C-LEVEL (Admin)
                │
                ▼
      Level 50: DEPARTMENT HEADS
   (Finance, HR, Marketing, Engineering)
                │
                ▼
      Level 10: GENERAL EMPLOYEES
```

## 2. Permission Matrix
This matrix defines which departments each role can access.

| Role ⬇️ | Finance Docs | HR Docs | Marketing Docs | Engineering Docs | General Docs |
|---|---|---|---|---|---|
| **C-Level** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Finance** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **HR** | ❌ | ✅ | ❌ | ❌ | ✅ |
| **Marketing** | ❌ | ❌ | ✅ | ❌ | ✅ |
| **Engineering** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Employees** | ❌ | ❌ | ❌ | ❌ | ✅ |

## 3. Search Flow with RBAC
The search pipeline enforces these permissions dynamically:

1.  **User Query** ("revenue report")
2.  **Vector Search** (Retrieves 25 raw chunks from ALL departments)
3.  **RBAC Filter** (Checks user role vs. chunk `department` metadata)
    - *If Role=Marketing -> Drop Finance/HR docs*
4.  **Ranking** (Select top 5 remaining chunks)
5.  **Result** (Safe chunks only)

## 4. Configuration
Modify `week 4/config/role_hierarchy.json` to update permissions.

```json
{
  "department_access": {
    "finance": ["Finance", "General", "New_Dept"]
  }
}
```

## 5. Security Considerations
- **Metadata Integrity**: Ensure upstream metadata tagging is secure.
- **Fail-Safe**: Code defaults to `unknown` department -> Access Denied.
- **Audit Logging**: All filtered attempts are logged.
