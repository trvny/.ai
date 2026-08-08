# Templates

Small starting points, not a framework wearing a hard hat.

- `openai-agent.py`: minimal OpenAI Agents SDK scaffold. Uses `AI_PROMPT` for a local one-shot prompt.
- `wrangler.jsonc`: baseline Cloudflare Worker configuration with placeholders and no secrets.
- `.dev.vars.example`: names for common local credentials; copy it to an ignored `.dev.vars` and fill values locally.
- `outcome-task.md`: compact outcome-first brief for complex reusable tasks.

Review every template before copying it into a real project. Remove unused
bindings, dependencies, fields, and assumptions.

Keep credentials in environment variables or provider secret storage, never in
the maintained template.
