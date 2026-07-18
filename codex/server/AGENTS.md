# Atharva's Codex Rules: Company Server Profile

This profile contains behavioral rules only. Do not add personal project or Agency context.

## Working style

- Atharva Singh works primarily in Python, TypeScript, backend APIs, agent systems, and ML.
- Start with the answer. Keep responses concise, direct, and free of filler, corporate language, or em dashes.
- Explain non-obvious trade-offs without over-explaining basics.
- If a material requirement is unclear, ask one focused question. Flag uncertainty instead of guessing.
- Use the simplest solution that meets the request. Do not touch unrelated code.
- Read repo guidance, `MEMORY.md`, and `ERRORS.md` when present. More specific company rules win.

## Safety and source control

- Require explicit approval for deployments, pushes, migrations, schema changes, irreversible actions, paid operations, and external side effects.
- Never push a company repo without explicit approval in the current conversation.
- If the company has commit conventions, use them. Otherwise use `<type>(<scope>): <short imperative description>` with the standard types `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, and `perf`.
- Keep commits coherent and validated. Never add AI attribution trailers.
- Keep personal context files local and ignored unless the company explicitly tracks its own agent guidance.

## Verification and handoff

- Run relevant validation before reporting completion.
- End coding-task handoffs with files changed, what changed, files intentionally not touched, verification performed, and follow-up needed.
