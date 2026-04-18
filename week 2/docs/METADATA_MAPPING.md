# RBAC Metadata Mapping

## 1. Role Hierarchy
Visual representation of the access levels:

```ascii
      C-LEVEL (All Access)
            │
    ┌───────┼───────┬───────┐
 Finance   HR   Marketing Engineering
    │       │       │       │
    └───────┼───────┴───────┘
            │
        General Employees
```

| Role | Access Level | Description |
|------|--------------|-------------|
| **C-Level** | Level 1 (Highest) | Access to ALL documents across all departments. |
| **Department Head** | Level 2 | Access to their specific department docs + General docs. |
| **Employee** | Level 3 (Lowest) | Access strictly to General documents (Handbook, Policies). |

## 2. Department-Role Mapping Table

| Department | Content Types | Accessible Roles |
|:---:|---|---|
| **Finance** | Quarterly Reports, Budgets, Revenue | `Finance Users`, `C-Level` |
| **HR** | Employee Data, Payroll, Confidential Policies | `HR Users`, `C-Level` |
| **Marketing** | Campaign Reports, Brand Assets, Analytics | `Marketing Users`, `C-Level` |
| **Engineering** | Architecture, API Keys, Source Code | `Engineering Users`, `C-Level` |
| **General** | Employee Handbook, Holidays, Company Policies | **ALL ROLES** (Employees, C-Level, Dept Heads) |

## 3. Document Classification Rules
Documents are classified based on their file path and content analysis:
- **Path-Based**: If file resides in `/Finance/` folder, it is tagged "Finance".
- **Keyword-Based**: If content contains "revenue", "fiscal", it is tagged "Finance".
- **Default**: Files not matching specific criteria default to "General".

## 4. Chunk Metadata Schema
Each document chunk contains the following metadata structure:
```json
{
  "chunk_id": "chunk_0042",
  "content": "Q4 revenue exceeded expectations...",
  "department": "Finance",
  "accessible_roles": ["finance", "c-level"],
  "source": "q4_report.md",
  "token_count": 450
}
```

## 5. Access Control Matrix
| User Role ⬇️ / Dept ➡️ | Finance | HR | Marketing | Engineering | General |
|---|---|---|---|---|---|
| **C-Level** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Finance** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **HR** | ❌ | ✅ | ❌ | ❌ | ✅ |
| **Marketing** | ❌ | ❌ | ✅ | ❌ | ✅ |
| **Engineering** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Employee** | ❌ | ❌ | ❌ | ❌ | ✅ |

## 6. Examples
**Scenario A: Finance User Query**
- Query: "What is the Q3 revenue?"
- System retrieves chunks tagged `department: "Finance"`.
- Access Check: User has role `finance`. Match found.
- Result: **Access Granted**.

**Scenario B: Marketing User Query**
- Query: "Show me the engineering API keys."
- System retrieves chunks tagged `department: "Engineering"`.
- Access Check: User has role `marketing`. `Engineering` NOT in `accessible_roles`.
- Result: **Access Denied**.
