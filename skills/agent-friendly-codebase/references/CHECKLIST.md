# CHECKLIST

## Review

- [ ] Bound the work area to one to three primary paths
- [ ] Identify entrypoints, key dependencies, and reverse dependencies
- [ ] Identify public contracts and external boundaries
- [ ] Confirm the proof path and area-scoped validation command
- [ ] Capture search seeds or starting files for future exploration
- [ ] Score each ACRS category with supporting evidence
- [ ] Record proof path and evidence refs in the score record
- [ ] Record proof results explicitly

## Transform

- [ ] Record the before-state proof commands before changing anything
- [ ] Capture or reuse a before review snapshot
- [ ] Confirm the fastest trusted validation path for the area
- [ ] Confirm the broader regression check that should remain green
- [ ] Choose the smallest diff that improves the target rule gaps
- [ ] Avoid changing shared contracts without mapping likely dependents first
- [ ] Keep always-loaded guidance compact
- [ ] Prefer executable artifacts (examples, scripts, tests) over broad prose
- [ ] Run area-scoped proof before broader regression checks
- [ ] If behavior changed intentionally, document the new contract explicitly
- [ ] If validation is missing or flaky, do not claim the transformation is safe
- [ ] Score after-state with same rubric and proof path as before-state
- [ ] Include absolute deltas in before/after comparison
- [ ] Capture remaining risks and unverified behavior in the report
- [ ] Save learned patterns back into the repository
