## 2024-05-23 - Multiprocessing Chunk Size & IPC
**Learning:** When using `multiprocessing.Pool` for CPU-bound tasks (prime finding), simply increasing chunk size isn't always better. While it reduces IPC overhead, it can cause severe load balancing issues if the tasks vary in complexity (checking larger primes takes longer).
**Action:** For variable-complexity tasks, find a "sweet spot" chunk size that balances IPC overhead against load distribution. For this prime finder, 10,000 items per chunk was optimal, while 100,000 caused a regression due to uneven worker utilization.
