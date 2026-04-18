# Preprocessing QA Report

**Generated On:** 29/01/2026
**Validator:** Vinuthna Jangam

## 1. Summary Statistics
| Metric | Value |
|---|---|
| **Total Chunks** | 47 |
| **Passed Validation** | 47 |
| **Failed Validation** | 0 |
| **Pass Rate** | 100% |

## 2. Validation Checks Performed
- **Token Count**: Verified all chunks are within 0-512 tokens.
- **Metadata Presence**: Confirmed `department` and `accessible_roles` exist.
- **Role Assignment**: Ensured `accessible_roles` is not empty.
- **Content Integrity**: Verified no empty content fields.

## 3. Issues Found
- *No critical issues found.*
- All documents parsed and chunked correctly.
- Role mapping logic successfully assigned departments.

## 4. Department Distribution
- **Engineering**: 15 chunks
- **Finance**: 10 chunks
- **Marketing**: 15 chunks
- **General**: 7 chunks
- **HR**: 0 chunks (Note: Verify if HR data was present in source)

## 5. Recommendations
- Proceed to Vector Embedding generation.
- Ensure embedding model handles the 512 token limit (all-MiniLM-L6-v2 limit is 512, so we are good).
