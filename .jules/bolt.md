## 2024-10-24 - [Optimizing Multiprocessing with Chunking]
**Learning:** `pool.map` with small tasks (integers) has high overhead even with `chunksize`. Grouping tasks into larger batches (ranges) and processing them inside the worker significantly reduces IPC and function call overhead.
**Action:** When using `multiprocessing.Pool`, prefer passing coarse-grained tasks (like ranges or large data chunks) over fine-grained items, even if `chunksize` is available.
