---
name: verify-frontend-change
description: Verify UI and frontend changes end to end in a real browser before completion. Use after editing pages, components, styles, client demos, or any user-visible behavior, and before reporting frontend work as done.
---

# Verify Frontend Changes

Treat a successful edit or build as insufficient evidence that the UI works.

1. Start the documented dev server and open the edited page in a real browser. Prefer the in-app Browser for interactive signed-in testing, or Playwright when terminal automation is the better fit.
2. Exercise the changed flow directly. Click new controls, enter realistic values, and confirm the expected state and navigation changes.
3. Capture and inspect desktop and 375px mobile views.
4. Check the browser console for new errors or warnings.
5. Check relevant network requests for failures introduced by the change.
6. Fix any failure and repeat the affected checks. Do not hand back partially verified work.
7. Report the routes, interactions, viewport sizes, console state, and network state that were verified.

For Agency client demos, also confirm the hero renders, the primary CTA is visible and clickable above the fold on mobile, and no placeholder or lorem ipsum text remains.
