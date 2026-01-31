## 2024-05-22 - [Multiprocessing IPC Bottleneck in Filtering]
**Learning:** Using `pool.map` to filter a large list (returning `None` for filtered items) creates massive IPC overhead due to pickling/unpickling useless data.
**Action:** When filtering with multiprocessing, chunk the work manually and perform the filtering *inside* the worker, returning only the valid results. This reduces IPC payload size and object creation overhead.

## 2024-05-23 - Multiprocessing Chunk Size & IPC
**Learning:** When using `multiprocessing.Pool` for CPU-bound tasks (prime finding), simply increasing chunk size isn't always better. While it reduces IPC overhead, it can cause severe load balancing issues if the tasks vary in complexity (checking larger primes takes longer).
**Action:** For variable-complexity tasks, find a "sweet spot" chunk size that balances IPC overhead against load distribution. For this prime finder, 10,000 items per chunk was optimal, while 100,000 caused a regression due to uneven worker utilization.

## 2024-10-24 - [Optimizing Multiprocessing with Chunking]
**Learning:** `pool.map` with small tasks (integers) has high overhead even with `chunksize`. Grouping tasks into larger batches (ranges) and processing them inside the worker significantly reduces IPC and function call overhead.
**Action:** When using `multiprocessing.Pool`, prefer passing coarse-grained tasks (like ranges or large data chunks) over fine-grained items, even if `chunksize` is available.
