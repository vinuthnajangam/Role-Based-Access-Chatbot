# Performance Benchmark Report
**Date:** 29/01/2026
**Tester:** Vinuthna Jangam

## 1. Executive Summary
The system demonstrates excellent performance characteristics, well within the project targets.
- **Search Latency:** ~18ms (Target < 500ms) 🚀
- **Embedding Generation:** ~25ms per document (Batch mode)

## 2. Embedding Performance
| Operation | Time (ms) | Throughput (docs/sec) |
|---|---|---|
| Single Document | 59.14 ms | ~17 docs/sec |
| Batch (Avg per doc) | 24.55 ms | ~40 docs/sec |

*Observation: Batch processing significantly improves throughput.*

## 3. Search Retrieval Latency
| Metric | Value (ms) |
|---|---|
| Average Latency | 18.38 ms |
| Min Latency | ~11 ms |
| Max Latency | ~47 ms |
| P95 Latency | 46.29 ms |

*Observation: P95 latency is under 50ms, ensuring a real-time feel for the user.*

## 4. Scalability Projections
Given the current latency of ~18ms for 47 chunks:
- Extrapolating to 1,000 chunks: ~25ms (Vector search is logarithmic/highly optimized).
- Extrapolating to 10,000 chunks: ~50ms.
- **Conclusion:** ChromaDB configuration is suitable for the target dataset size.

## 5. System Specifications
- **Model:** `all-MiniLM-L6-v2`
- **Database:** ChromaDB (Local InMemory/Persistent)
- **Hardware:** Local Dev Environment
