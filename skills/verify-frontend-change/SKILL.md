---
name: verify-frontend-change
description: Verify any UI or frontend change end-to-end in a real browser before declaring it done. Trigger after editing anything user-visible - pages, components, styles, client demos - before reporting the work complete.
---

# Verifying Frontend Changes

Never report a UI change as complete based on a successful edit alone. Client
demos get seen by clients — "the edit applied" is not "it works".

## Steps

1. Start the dev server (use `.claude/launch.json` / preview tools if
   available) and open the edited page.
2. Interact with the change directly. For a new control (button, input,
   toggle): click it, confirm the expected state change actually happens.
3. Screenshot at desktop width AND mobile width (375px). Client demos are
   opened on phones.
4. Check the browser console: zero new errors or warnings.
5. Check network: no failed requests introduced by the change.
6. If any step fails, fix and rerun from step 1. Do not hand back partially
   verified work — report what was verified and how.

## For client demo work (Agency)

Additionally eyeball: hero section renders, primary CTA is visible and
clickable above the fold on mobile, no placeholder text or lorem ipsum left in.
