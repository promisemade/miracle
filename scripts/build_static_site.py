from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
DATA = ROOT / "data"


@dataclass(frozen=True)
class BuildTarget:
    output_dir: Path
    fiches_url: str
    questions_url: str
    pdf_base: str
    resource_base: str


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def apply_common_route_replacements(text: str) -> str:
    replacements = [
        ('href="/"', 'href="./index.html#fiches"'),
        ('href="/ministeres"', 'href="./ministeres.html"'),
        ('href="/training"', 'href="./index.html#training"'),
        ('href="/stats"', 'href="./index.html#stats"'),
        ('href="/quiz"', 'href="./quiz.html"'),
        ('href="/welcome"', 'href="./index.html#fiches"'),
        (
            'href="/feedback?from={{ request.path }}"',
            'href="https://github.com/promisemade/miracle/issues" target="_blank" rel="noreferrer"',
        ),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def build_app_page(target: BuildTarget) -> str:
    template = (TEMPLATES / "app.html").read_text(encoding="utf-8")
    fiches = load_json(DATA / "fiches.json")

    stats = {
        "total": len(fiches),
        "centrale": sum(1 for f in fiches if "CENTRALE" in f["administration"]),
        "deconcentree": sum(1 for f in fiches if "DÉCONCENTRÉE" in f["administration"]),
        "scolaire": sum(1 for f in fiches if "SCOLAIRE" in f["administration"]),
    }
    structures = sorted({f["structure"] for f in fiches if f.get("structure")}, key=lambda value: value.lower())
    structures_html = "\n".join(
        f'                                <div class="custom-select-option" data-value="{escape_html(s)}">{escape_html(s[:40])}{"..." if len(s) > 40 else ""}</div>'
        for s in structures
    )
    static_stats = {
        "total": len(fiches),
        "by_administration": count_by(fiches, "administration"),
        "by_structure": count_by(fiches, "structure"),
        "by_domaine": count_by(fiches, "domaine"),
    }

    template = apply_common_route_replacements(template)
    template = template.replace("{{ stats.total }}", str(stats["total"]))
    template = template.replace("{{ stats.centrale }}", str(stats["centrale"]))
    template = template.replace("{{ stats.deconcentree }}", str(stats["deconcentree"]))
    template = template.replace("{{ stats.scolaire }}", str(stats["scolaire"]))

    template = re.sub(
        r"\s*{% for s in structures %}.*?{% endfor %}",
        "\n" + structures_html + "\n",
        template,
        flags=re.S,
    )

    template = template.replace(
        "const defaultView = '{{ default_view|default(\"fiches\") }}';",
        "const defaultView = ['fiches', 'training', 'stats'].includes(window.location.hash.replace('#', '')) ? window.location.hash.replace('#', '') : 'fiches';",
    )
    template = template.replace(
        "let allFiches = [];",
        f"const STATIC_STATS = {json.dumps(static_stats, ensure_ascii=False)};\n        let allFiches = [];",
    )
    template = template.replace(
        "        async function loadFiches() {",
        f"""        const STATIC_PDF_BASE = {json.dumps(target.pdf_base, ensure_ascii=False)};\n\n        function toStaticPdfUrl(path) {{\n            return `${{STATIC_PDF_BASE}}/${{path.split('/').map(encodeURIComponent).join('/')}}`;\n        }}\n\n        async function loadFiches() {{""",
    )
    template = template.replace(
        "const res = await fetch('/api/fiches');",
        f"const res = await fetch({json.dumps(target.fiches_url, ensure_ascii=False)});",
    )
    template = template.replace("/pdf/${encodeURIComponent(f.path)}", "${toStaticPdfUrl(f.path)}")
    template = template.replace(
        "            const res = await fetch('/api/random');\n            const f = await res.json();",
        "            const f = allFiches[Math.floor(Math.random() * allFiches.length)];",
    )
    template = template.replace(
        "            const res = await fetch('/api/stats');\n            const stats = await res.json();",
        "            const stats = STATIC_STATS;",
    )
    template = template.replace(
        "        loadFiches();\n        setActiveView(getViewFromUrl());\n        updateTimer();",
        "        window.addEventListener('hashchange', () => setActiveView(getViewFromUrl()));\n        loadFiches();\n        setActiveView(getViewFromUrl());\n        updateTimer();",
    )
    return template


def build_quiz_page(target: BuildTarget) -> str:
    template = (TEMPLATES / "quiz.html").read_text(encoding="utf-8")
    template = apply_common_route_replacements(template)
    template = template.replace(
        "const res = await fetch('/api/quiz/data');",
        f"const res = await fetch({json.dumps(target.questions_url, ensure_ascii=False)});",
    )
    template = template.replace(
        "        // Load data\n        function augmentExplanation(q) {",
        f"""        const STATIC_RESOURCE_BASE = {json.dumps(target.resource_base, ensure_ascii=False)};\n\n        function toStaticSourceUrl(url) {{\n            if (!url) return null;\n            if (url.startsWith('http://') || url.startsWith('https://')) return url;\n            if (url.startsWith('/resource/')) {{\n                const relativePath = url.slice('/resource/'.length).split('/').map(encodeURIComponent).join('/');\n                return `${{STATIC_RESOURCE_BASE}}/${{relativePath}}`;\n            }}\n            return url;\n        }}\n\n        // Load data\n        function augmentExplanation(q) {{""",
    )
    template = template.replace(
        "                    source_url: q.source_url || source?.source_url || null,",
        "                    source_url: toStaticSourceUrl(q.source_url || source?.source_url || null),",
    )
    template = template.replace(
        "            data.flashcards = (data.flashcards || []).map((f, i) => ({ ...f, _id: f.id || `fc-${i}` }));",
        "            data.flashcards = (data.flashcards || []).map((f, i) => ({ ...f, _id: f.id || `fc-${i}`, source_url: toStaticSourceUrl(f.source_url || null) }));",
    )
    return template


def build_ministeres_page(target: BuildTarget) -> str:
    template = (TEMPLATES / "ministeres.html").read_text(encoding="utf-8")
    payload = load_json(DATA / "ministeres.json")
    template = apply_common_route_replacements(template)
    embedded_json = json.dumps(payload["ministeres"], ensure_ascii=False)
    template = template.replace(
        '<script type="application/json" id="ministeresData">{{ ministeres | tojson }}</script>',
        f'<script type="application/json" id="ministeresData">{embedded_json}</script>',
    )
    return template


def count_by(items: list[dict], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = item.get(key)
        if not value:
            continue
        counts[value] = counts.get(value, 0) + 1
    return counts


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def git_output(*args: str) -> str | None:
    try:
        return (
            subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL)
            .strip()
        )
    except (OSError, subprocess.CalledProcessError):
        return None


def detect_raw_base_url() -> str | None:
    remote_url = git_output("config", "--get", "remote.origin.url")
    branch = git_output("branch", "--show-current") or "main"
    if not remote_url:
        return None

    match = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$", remote_url)
    if not match:
        return None

    owner = match.group("owner")
    repo = match.group("repo")
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}"


def build_targets() -> list[BuildTarget]:
    targets = [
        BuildTarget(
            output_dir=ROOT,
            fiches_url="./data/fiches.json",
            questions_url="./data/questions.json",
            pdf_base="./Fiches de postes",
            resource_base="./Ressources",
        )
    ]

    raw_base = detect_raw_base_url()
    if raw_base:
        targets.append(
            BuildTarget(
                output_dir=ROOT / "docs",
                fiches_url=f"{raw_base}/data/fiches.json",
                questions_url=f"{raw_base}/data/questions.json",
                pdf_base=f"{raw_base}/Fiches%20de%20postes",
                resource_base=f"{raw_base}/Ressources",
            )
        )
    return targets


def main() -> None:
    outputs: dict[Path, str] = {}
    for target in build_targets():
        target.output_dir.mkdir(parents=True, exist_ok=True)
        outputs[target.output_dir / "index.html"] = build_app_page(target)
        outputs[target.output_dir / "quiz.html"] = build_quiz_page(target)
        outputs[target.output_dir / "ministeres.html"] = build_ministeres_page(target)

    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
        print(f"[OK] {path.relative_to(ROOT)} généré")


if __name__ == "__main__":
    main()
