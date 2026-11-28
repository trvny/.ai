"""Build the public wiki and crawler artifacts from canonical repository files."""
import json
import posixpath
import re
import shutil
import zipfile
from pathlib import Path
from urllib.parse import quote, urlsplit
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
DOCS = WIKI / "src/content/docs"
PUBLIC = WIKI / "public"
BASE = "https://trvny.github.io/.ai/"
REPO = "https://github.com/trvny/.ai"
PAGES = {}


def url(slug):
    return BASE + (slug + "/" if slug else "")


def source(path):
    return REPO + "/blob/main/" + quote(path, safe="/")


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def link(slug, label):
    return f"[{label}]({url(slug)})"


def code(content, language="text"):
    fence = "\x60" * max(3, 1 + max((len(x) for x in re.findall(r"\x60+", content)), default=0))
    return f"{fence}{language}\n{content.rstrip()}\n{fence}\n"


SOURCES = {
    "docs/submodule.md": "guides/submodule",
    "docs/profile-reference.md": "guides/profile-reference",
    "instructions/instructions.md": "reference/instructions",
    "styles/styles.md": "reference/styles",
    "AGENTS.md": "reference/agents",
    ".github/copilot-instructions.md": "reference/copilot",
    ".github/instructions/cloudflare.instructions.md": "reference/cloudflare",
    ".github/instructions/microsoft.instructions.md": "reference/microsoft",
    "templates/README.md": "templates",
    "templates/spec-kit/travny-lean/README.md": "templates/travny-lean",
    "profiles/default.yaml": "reference/default-profile",
    "examples/profile.overlay.yaml": "reference/overlay-example",
    "schema/style-profile.schema.json": "reference/schema",
    "templates/openai-agent.py": "templates/openai-agent",
    "templates/wrangler.jsonc": "templates/wrangler",
    "templates/.dev.vars.example": "templates/dev-vars",
    "templates/outcome-task.md": "templates/outcome-task",
    "templates/spec-kit/travny-lean/preset.yml": "templates/spec-kit-preset",
    "tools/merge_profile.py": "tools/merge-profile",
    "tools/render_profile.py": "tools/render-profile",
}
GROUPS = {"guides": "Guides", "reference": "Reference", "templates": "Templates",
          "tools": "Tools", "skills": "Skills"}


def rewrite_links(body, path):
    # Rewrite ordinary inline Markdown links outside fenced code.
    def replace(match):
        target = match.group(2)
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path or target.startswith("/"):
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), parsed.path))
        destination = url(SOURCES[resolved]) if resolved in SOURCES else source(resolved)
        if parsed.fragment:
            destination += "#" + parsed.fragment
        return f"[{match.group(1)}]({destination})"

    result = []
    fence = None
    for line in body.splitlines():
        marker = re.match(r"^\s*(\x60{3,}|~{3,})", line)
        if marker:
            value = marker.group(1)
            if fence is None:
                fence = value
            elif value[0] == fence[0] and len(value) >= len(fence):
                fence = None
            result.append(line)
        elif fence is None:
            result.append(re.sub(r"(?<!!)\[([^\]\n]+)\]\(([^()\s]+)\)", replace, line))
        else:
            result.append(line)
    return "\n".join(result)


def page(slug, title, description, body, path=None):
    if slug in PAGES:
        raise ValueError(f"Duplicate page: {slug}")
    if path:
        body = f"[View source on GitHub]({source(path)})\n\n" + body
    PAGES[slug] = (title, description, body.strip() + "\n")


def markdown(path, title, description):
    body = read(path).lstrip("\ufeff")
    body = re.sub(r"^# [^\n]+\n+", "", body, count=1)
    page(SOURCES[path], title, description, rewrite_links(body, path), path)


def raw(path, title, description, language):
    page(SOURCES[path], title, description, code(read(path), language), path)


def catalog(directory, pattern):
    paths = sorted((ROOT / directory).glob(pattern))
    return "\n".join(f"- [{p.name}]({source(p.relative_to(ROOT).as_posix())})" for p in paths if p.is_file())


def build():
    page("", ".ai documentation", "Portable AI instructions, profiles, overlays, provider adapters, templates and skills.",
         f"""Use the public core as a pinned submodule. Compose a local overlay, validate the result and render provider instructions. Profiles define preferences, not permissions.

## Start here

- {link('guides/submodule', 'Install and update the core')}
- {link('guides/profile-reference', 'Profile fields and modifier levels')}
- {link('overlays', 'Compose and render a profile')}

## Browse the repository

| Section | Contents |
| --- | --- |
| {link('reference/instructions', 'Instructions')} | Portable guidance and provider defaults |
| {link('reference/styles', 'Styles')} | Voice, modifiers and collaboration |
| {link('reference/default-profile', 'Profiles')} | Default YAML, example overlay, JSON Schema |
| {link('tools/merge-profile', 'Tools')} | Merge and render entrypoints |
| {link('templates', 'Templates')} | Agent, Worker, task brief and Spec Kit preset |
| {link('skills', 'Skills')} | Downloadable skill packages and descriptions |
| {link('field-notes', 'Repository map')} | Workflows, tests, source files |

[GitHub repository]({REPO}) · [LLM index]({BASE}llms.txt) · [Full documentation]({BASE}llms-full.txt)
""")
    markdown("docs/submodule.md", "Install as a submodule", "Installation, updates, composition, rendering and CI checkout.")
    markdown("docs/profile-reference.md", "Profile reference", "Profile fields, layering, voices, modifiers, collaboration and renderer behavior.")
    markdown("instructions/instructions.md", "Portable instructions", "Reusable assistant instructions and working behavior.")
    markdown("styles/styles.md", "Style guide", "Base voices, modifiers, adaptation and collaboration.")
    markdown("AGENTS.md", "Repository instructions", "Canonical repository rules and public/private boundary.")
    markdown(".github/copilot-instructions.md", "GitHub Copilot instructions", "Repository defaults for GitHub Copilot.")
    markdown(".github/instructions/cloudflare.instructions.md", "Cloudflare instructions", "Cloudflare-specific repository guidance.")
    markdown(".github/instructions/microsoft.instructions.md", "Microsoft instructions", "Microsoft-specific repository guidance.")
    raw("profiles/default.yaml", "Default profile", "Complete portable YAML baseline.", "yaml")
    raw("examples/profile.overlay.yaml", "Example overlay", "Partial YAML overlay for local preferences.", "yaml")
    raw("schema/style-profile.schema.json", "Profile JSON Schema", "Machine-readable contract for composed profiles.", "json")
    markdown("templates/README.md", "Templates", "Starter files for agents, Cloudflare Workers and reusable tasks.")
    markdown("templates/spec-kit/travny-lean/README.md", "Travny Lean / Spec Kit", "Opt-in spec-driven development for chat, MCP and native Spec Kit.")
    raw("templates/openai-agent.py", "OpenAI agent template", "Minimal Agents SDK scaffold.", "python")
    raw("templates/wrangler.jsonc", "Cloudflare Worker template", "Baseline Wrangler configuration.", "jsonc")
    raw("templates/.dev.vars.example", "Local variables example", "Placeholder variable names; no credentials.", "dotenv")
    raw("templates/outcome-task.md", "Outcome task template", "Compact outcome-first task brief.", "markdown")
    raw("templates/spec-kit/travny-lean/preset.yml", "Spec Kit preset", "Native preset configuration.", "yaml")
    for path, title, description in [
        ("tools/merge_profile.py", "Merge profiles", "Compose YAML layers and validate the effective profile."),
        ("tools/render_profile.py", "Render instructions", "Render a composed profile as provider-ready instructions."),
    ]:
        page(SOURCES[path], title, description,
             f"See {link('guides/submodule', 'the setup guide')} for runnable commands and {link('guides/profile-reference', 'the profile reference')} for the contract.\n\n## Source\n\n" + code(read(path), "python"), path)
    page("principles", "Core rules", "Public core, private overlays, canonical repository guidance.",
         f"{link('reference/agents', 'Canonical AGENTS.md')}\n\n{read('AGENTS.md').split(chr(10), 1)[1].strip()}\n\n{link('guides/submodule', 'Installation and local overrides')}")
    page("overlays", "Compose and render", "Commands and examples for combining the default profile with an overlay.",
         f"Mappings merge recursively; lists and scalars replace. Later layers win.\n\n## Example overlay\n\n" + code(read("examples/profile.overlay.yaml"), "yaml") +
         f"\n## Commands\n\n{link('guides/submodule', 'Install, merge, render and update')}\n\n{link('guides/profile-reference', 'Field reference')} · {link('reference/schema', 'Schema')} · {link('reference/default-profile', 'Baseline')}")
    page("field-notes", "Repository map", "Canonical source files, provider adapters, workflows and tests.",
         f"""## Provider adapters

- [AGENTS.md]({source('AGENTS.md')}) (canonical)
- [CLAUDE.md]({source('CLAUDE.md')}) and [GEMINI.md]({source('GEMINI.md')}) (symlinks)
- {link('reference/copilot', 'Copilot')}
- {link('reference/cloudflare', 'Cloudflare')}
- {link('reference/microsoft', 'Microsoft')}

## Workflows

{catalog('.github/workflows', '*.yml')}

## Tests

{catalog('tests', '*.py')}

## Spec Kit commands

{catalog('templates/spec-kit/travny-lean/commands', '*.md')}

## Project

[README]({source('README.md')}) · [License]({source('LICENSE')}) · [Citation]({source('CITATION')})
""")
    skills = []
    for archive in sorted((ROOT / "skills").iterdir()):
        if not archive.is_file() or archive.suffix not in {".zip", ".skill"}:
            continue
        path = archive.relative_to(ROOT).as_posix()
        download = REPO + "/raw/main/" + quote(path, safe="/")
        description = ""
        members = []
        if zipfile.is_zipfile(archive):
            with zipfile.ZipFile(archive) as z:
                members = [n for n in z.namelist() if not n.endswith("/")]
                manifests = sorted((n for n in members if n.split("/")[-1].lower() == "skill.md"), key=lambda n: (n.count("/"), n))
                if manifests:
                    info = z.getinfo(manifests[0])
                    if info.file_size <= 256_000:
                        manifest = z.read(info).decode("utf-8", errors="replace")
                        match = re.search(r"(?m)^description:\s*(.+)$", manifest)
                        if match:
                            description = match.group(1).strip("\"' ")
        skills.append(f"### {archive.name}\n\n{description + chr(10)*2 if description and description not in {'|', '>', '>-', '|-'} else ''}[Download]({download}) · [Source]({source(path)})" +
                      (f" · {len(members)} files" if members else ""))
    page("skills", "Skill catalog", "Downloadable portable skill packages from the repository.",
         "Opt-in packages. Inspect before installation; skills do not grant permissions.\n\n" + "\n\n".join(skills))


def emit():
    DOCS.mkdir(parents=True, exist_ok=True)
    # Only generated Markdown lives in this directory. No MDX evaluation.
    for path in DOCS.glob("*.md"):
        path.unlink()
    for group in GROUPS:
        path = DOCS / group
        if path.exists():
            shutil.rmtree(path)
    for slug, (title, description, body) in PAGES.items():
        crumbs = [("Home", ""), (title, slug)] if slug else [("Home", "")]
        group = slug.split("/")[0]
        if "/" in slug and group in {"templates", "skills"}:
            crumbs.insert(1, (GROUPS[group], group))
        structured = {"@context": "https://schema.org", "@type": "TechArticle" if slug else "WebSite",
                      "name": title, "description": description, "url": url(slug),
                      "inLanguage": "en", "isAccessibleForFree": True}
        head = [{"tag": "script", "attrs": {"type": "application/ld+json"},
                 "content": json.dumps(structured, ensure_ascii=True)}]
        if slug:
            breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                          "itemListElement": [{"@type": "ListItem", "position": i, "name": name, "item": url(s)}
                                              for i, (name, s) in enumerate(crumbs, 1)]}
            head.append({"tag": "script", "attrs": {"type": "application/ld+json"},
                         "content": json.dumps(breadcrumb, ensure_ascii=True)})
        meta = {"title": title, "description": description, "head": head}
        frontmatter = "---\n" + "\n".join(f"{key}: {json.dumps(value, ensure_ascii=True)}" for key, value in meta.items()) + "\n---\n\n"
        trail = " / ".join(link(s, name) if s != slug else name for name, s in crumbs) + "\n\n" if slug else ""
        file = DOCS / (slug + ".md" if slug else "index.md")
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(frontmatter + trail + body, encoding="utf-8")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{escape(url(slug))}</loc></url>\n" for slug in PAGES) + "</urlset>\n"
    (PUBLIC / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    index = "# .ai\n\n> Portable AI configuration: public core, local overlays, provider adapters, templates and skills.\n\n## Documentation\n\n"
    index += "".join(f"- [{title}]({url(slug)}): {description}\n" for slug, (title, description, _) in PAGES.items())
    index += f"\n## Optional\n\n- [Full documentation]({BASE}llms-full.txt)\n- [Source repository]({REPO})\n"
    (PUBLIC / "llms.txt").write_text(index, encoding="utf-8")
    full = "# .ai documentation\n\n" + "\n\n".join(f"## {title}\n\nSource page: {url(slug)}\n\n{body}" for slug, (title, _, body) in PAGES.items())
    (PUBLIC / "llms-full.txt").write_text(full + "\n", encoding="utf-8")
    print(f"Generated {len(PAGES)} wiki pages and crawler indexes")


if __name__ == "__main__":
    build()
    emit()
