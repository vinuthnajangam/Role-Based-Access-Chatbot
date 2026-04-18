# Search Quality QA Report
**Date:** 29/01/2026
**Tester:** Mandha Shirisha

## 1. Test Methodology
- **Queries**: 5 representative queries covering all departments.
- **Criteria**: Top-1 result match accuracy.
- **Metric**: Pass/Fail based on expected department.

## 2. Test Results
| Query | Expected | Actual | Latency (ms) | Result |
|---|---|---|---|---|
| quarterly revenue report | Finance | Finance | 117.90 | ✅ |
| employee benefits policy | HR | General | 18.88 | ❌ |
| marketing campaign ROI | Marketing | Marketing | 16.07 | ✅ |
| API documentation | Engineering | Engineering | 14.60 | ✅ |
| company handbook | General | General | 18.02 | ✅ |

## 3. Analysis of Failures
- **Query**: "employee benefits policy"
- **Issue**: Retrieved "General" instead of "HR".
- **Root Cause**: Likely the Employee Handbook (General) contains "benefits" and "policy" keywords more frequently or prominently than the specific HR docs in the dataset.
- **Impact**: User still gets relevant info, but maybe not the *role-restricted* detailed HR policy.
- **Fix**: Adjust keywords or boost HR document ranking for "benefits".

## 4. Performance
- **Avg Latency**: ~37ms (Excellent)
- **Pass Rate**: 80%

## 5. Conclusion
Search is functional and fast. Classification accuracy is good but needs fine-tuning for overlapping content like "benefits".
