# SAFE TRANSFORM CHECKLIST

Use this when applying a transformation to a live work area.

- [ ] Record the before-state proof commands before changing anything.
- [ ] Confirm the fastest trusted validation path for the area.
- [ ] Confirm the broader regression check that should remain green.
- [ ] Prefer the smallest diff that improves the target rule gaps.
- [ ] Avoid changing shared contracts without mapping likely dependents first.
- [ ] If several agents may touch the area, keep ownership lanes, handoff points, and collision hotspots current.
- [ ] Run area-scoped proof before broader regression checks.
- [ ] If behavior changed intentionally, document the new contract explicitly.
- [ ] If validation is missing or flaky, do not claim the transformation is safe.
- [ ] Capture remaining risks and unverified behavior in the report.
