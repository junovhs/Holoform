# Design Note: Incremental Holoform Regeneration

This document outlines a strategy for incremental Holoform regeneration.

## 1. The Need for Incremental Regeneration

The current Holoform generator re-parses all the files in a project every time it is run. This can be inefficient for large projects, where only a small number of files may have changed. Incremental regeneration is a mechanism that allows the Holoform generator to only re-parse the files that have changed since the last run.

## 2. Proposed Strategy

The following is a proposed strategy for incremental Holoform regeneration:

1.  **Store a hash of each file.** When the Holoform generator is run, it will calculate a hash of each file and store it in a cache.
2.  **Compare the hashes on subsequent runs.** On subsequent runs, the Holoform generator will compare the hash of each file with the hash in the cache. If the hashes are different, the file will be re-parsed.
3.  **Update the cache.** After each run, the Holoform generator will update the cache with the new hashes.

This strategy will ensure that only the changed files are re-parsed, which will significantly improve the performance of the Holoform generator for large projects.
