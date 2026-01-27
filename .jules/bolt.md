## 2024-05-22 - [Multiprocessing IPC Bottleneck in Filtering]
**Learning:** Using `pool.map` to filter a large list (returning `None` for filtered items) creates massive IPC overhead due to pickling/unpickling useless data.
**Action:** When filtering with multiprocessing, chunk the work manually and perform the filtering *inside* the worker, returning only the valid results. This reduces IPC payload size and object creation overhead.
