## 2026-01-28 - Multiprocessing Batch Size vs Load Balancing
**Learning:** When using `multiprocessing.Pool`, minimizing IPC by increasing task size is crucial. However, for tasks with variable complexity (finding primes gets harder as N increases), overly large chunks cause poor load balancing, negating IPC gains.
**Action:** Use moderate chunk sizes (e.g. 10k instead of 100k for N=2M) to balance IPC reduction with load distribution.
