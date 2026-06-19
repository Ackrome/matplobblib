"""Offline access to computer-vision exam tickets.

Ticket content is package data exported from Google Docs ahead of time. Runtime
access deliberately has no dependency on Google Drive or network access.
"""

import atexit
import base64
import json
import random as _random
import re
import shutil
import sys
import tempfile
import unicodedata
from pathlib import Path, PurePosixPath

try:
    from importlib.resources import files
except ImportError:  # pragma: no cover - exercised only on Python < 3.9
    from importlib_resources import files  # type: ignore


DATA_PACKAGE = "matplobblib.cv.data"
_MANIFEST_CACHE = None
_RUNTIME_ASSET_DIR = None

_BAD_GOOGLE_MATH_RE = re.compile(
    r"\\(?:subscript|superscript|s?bracelr|EquationFunction|EquationSymbol|Equation)",
    re.IGNORECASE,
)
_GLUED_LATEX_COMMAND_RE = re.compile(
    r"\\(?:Delta|Theta|Sigma|alpha|beta|gamma|delta|theta|lambda|mu|sigma|pi)"
    r"(?=[A-Za-z])"
)
_PROTECTED_MARKDOWN_RE = re.compile(
    r"```[\s\S]*?```|`[^`\n]*`|!\[[^\]\n]*\]\([^\)\n]*\)"
)
_MATH_FRAGMENT_PATTERNS = (
    re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$", re.DOTALL),
    re.compile(r"\\\[(.+?)\\\]", re.DOTALL),
    re.compile(r"\\\((.+?)\\\)", re.DOTALL),
    re.compile(r"(?<![\\$])\$(?!\$)([^\n$]+?)(?<![\\$])\$(?!\$)"),
)
_PLAIN_MATH_SYMBOLS = {
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "delta": "δ",
    "Delta": "Δ",
    "theta": "θ",
    "Theta": "Θ",
    "lambda": "λ",
    "mu": "μ",
    "sigma": "σ",
    "Sigma": "Σ",
    "pi": "π",
    "leq": "≤",
    "geq": "≥",
    "neq": "≠",
    "approx": "≈",
    "to": "→",
    "rightarrow": "→",
    "infty": "∞",
    "times": "×",
    "cdot": "·",
    "pm": "±",
}


def _data_root():
    """Return the resource root without assuming a filesystem-backed package."""
    return files(DATA_PACKAGE)


def _resource(relative_path):
    """Resolve a POSIX-style, package-relative resource path safely."""
    normalized = str(relative_path).replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ValueError("Unsafe package resource path: %r" % relative_path)

    resource = _data_root()
    for part in path.parts:
        resource = resource.joinpath(part)
    return resource


def _manifest():
    global _MANIFEST_CACHE
    if _MANIFEST_CACHE is None:
        text = _resource("manifest.json").read_text(encoding="utf-8")
        manifest = json.loads(text)
        if not isinstance(manifest, dict):
            raise RuntimeError("matplobblib.cv manifest must contain a JSON object")
        if not isinstance(manifest.get("tickets"), list):
            raise RuntimeError("matplobblib.cv manifest must contain a tickets list")
        if not isinstance(manifest.get("assets", []), list):
            raise RuntimeError("matplobblib.cv manifest assets must be a list")
        _MANIFEST_CACHE = manifest
    return _MANIFEST_CACHE


def _all_ticket_meta():
    return list(_manifest().get("tickets", []))


def _all_assets_meta():
    return list(_manifest().get("assets", []))


def _index_by_number():
    index = {}
    for item in _all_ticket_meta():
        number = item.get("number")
        if number is not None and number not in index:
            index[number] = item
    return index


def _index_by_slug():
    return {
        _normalize_query(item.get("slug")): item
        for item in _all_ticket_meta()
        if item.get("slug")
    }


def _index_by_title():
    return {
        _normalize_query(item.get("title")): item
        for item in _all_ticket_meta()
        if item.get("title")
    }


def _normalize_query(text):
    normalized = unicodedata.normalize("NFKC", str(text or ""))
    return normalized.strip().casefold().replace("ё", "е")


def _strip_markdown(text):
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_>`#-]+", " ", text)
    text = re.sub(r"\|", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _guess_mime(path):
    suffix = Path(path).suffix.lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
        ".bmp": "image/bmp",
    }.get(suffix, "application/octet-stream")


def _cleanup_runtime_assets():
    if _RUNTIME_ASSET_DIR:
        shutil.rmtree(_RUNTIME_ASSET_DIR, ignore_errors=True)


def _ensure_runtime_asset_dir():
    global _RUNTIME_ASSET_DIR
    if _RUNTIME_ASSET_DIR is None:
        _RUNTIME_ASSET_DIR = tempfile.mkdtemp(prefix="matplobblib-cv-assets-")
        atexit.register(_cleanup_runtime_assets)
    return _RUNTIME_ASSET_DIR


def _materialize_asset(asset_rel_path):
    """Copy a packaged asset to a temporary filesystem path when one is needed."""
    src = _resource(asset_rel_path)
    if not src.is_file():
        return None

    relative = PurePosixPath(str(asset_rel_path).replace("\\", "/"))
    root = Path(_ensure_runtime_asset_dir())
    dst = root.joinpath(*relative.parts)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        dst.write_bytes(src.read_bytes())
    return dst


def _asset_bytes(asset_rel_path):
    src = _resource(asset_rel_path)
    if not src.is_file():
        return None
    return src.read_bytes()


def _ticket_markdown(meta):
    resource = _resource(meta["path"])
    if not resource.is_file():
        raise FileNotFoundError("Ticket resource is missing: %s" % meta["path"])
    return resource.read_text(encoding="utf-8")


def _first_paragraph(markdown_text):
    blocks = re.split(r"\n\s*\n", markdown_text)
    for block in blocks:
        cleaned = _strip_markdown(block)
        if cleaned and len(cleaned) >= 30:
            return cleaned
    return _strip_markdown(markdown_text)[:240]


def _find_asset_meta(asset_rel_path):
    for item in _all_assets_meta():
        if item.get("path") == asset_rel_path:
            return item
    return None


def _resolve_meta(ref):
    if isinstance(ref, Ticket):
        return ref.meta

    if isinstance(ref, int) and not isinstance(ref, bool):
        meta = _index_by_number().get(ref)
        if meta is None:
            raise KeyError("Ticket number %r not found" % ref)
        return meta

    query = _normalize_query(ref)
    if not query:
        raise KeyError("Empty ticket reference")

    if query.isdigit():
        meta = _index_by_number().get(int(query))
        if meta is not None:
            return meta

    meta = _index_by_slug().get(query) or _index_by_title().get(query)
    if meta is not None:
        return meta

    for item in _all_ticket_meta():
        title = _normalize_query(item.get("title"))
        slug = _normalize_query(item.get("slug"))
        if query in title or query in slug:
            return item

    raise KeyError("Ticket reference %r not found" % ref)


def _asset_path_from_markdown_target(target):
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if target.startswith(("http://", "https://", "data:")):
        return None
    if target.startswith("../"):
        target = target[3:]
    elif target.startswith("./"):
        target = target[2:]
    if not target.startswith("assets/"):
        return None
    return target


def _malformed_math_to_plain_text(fragment):
    text = str(fragment)
    text = _BAD_GOOGLE_MATH_RE.sub("", text)
    for command, symbol in _PLAIN_MATH_SYMBOLS.items():
        text = re.sub(r"\\%s" % command, symbol, text)
    text = re.sub(r"\\([A-Za-z]+)", r"\1", text)
    text = text.replace("{", "(").replace("}", ")")
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return "[formula]"

    text = text.replace("\\", "\\\\")
    for character in ("`", "*", "_", "[", "]", "$"):
        text = text.replace(character, "\\" + character)
    return text


def sanitize_markdown_math(markdown: str) -> str:
    """Neutralize malformed Google Docs pseudo-LaTeX in Markdown math blocks."""
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a string")

    protected = []

    def protect(match):
        protected.append(match.group(0))
        return "\x00CVPROTECTED%s\x00" % (len(protected) - 1)

    text = _PROTECTED_MARKDOWN_RE.sub(protect, markdown)

    def sanitize_fragment(match):
        fragment = match.group(1)
        if not (
            _BAD_GOOGLE_MATH_RE.search(fragment)
            or _GLUED_LATEX_COMMAND_RE.search(fragment)
        ):
            return match.group(0)
        return _malformed_math_to_plain_text(fragment)

    for pattern in _MATH_FRAGMENT_PATTERNS:
        text = pattern.sub(sanitize_fragment, text)

    for index, original in enumerate(protected):
        text = text.replace("\x00CVPROTECTED%s\x00" % index, original)
    return text


def _embed_or_resolve_images(markdown_text, mode="dataurl"):
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    def repl(match):
        alt = match.group(1)
        relative = _asset_path_from_markdown_target(match.group(2))
        if relative is None:
            return match.group(0)

        if mode == "dataurl":
            payload = _asset_bytes(relative)
            if payload is None:
                return "![%s](missing:%s)" % (alt, relative)
            asset_meta = _find_asset_meta(relative) or {}
            mime = asset_meta.get("mime_type") or _guess_mime(relative)
            encoded = base64.b64encode(payload).decode("ascii")
            return "![%s](data:%s;base64,%s)" % (alt, mime, encoded)

        if mode == "absolute":
            path = _materialize_asset(relative)
            if path is None:
                return "![%s](missing:%s)" % (alt, relative)
            target = path.as_posix()
            if any(char in target for char in " ()"):
                target = "<%s>" % target
            return "![%s](%s)" % (alt, target)

        return match.group(0)

    return pattern.sub(repl, markdown_text)


def _in_ipython():
    try:
        from IPython import get_ipython

        return get_ipython() is not None
    except Exception:
        return False


class Ticket(object):
    """A lightweight view over one manifest entry and its packaged Markdown."""

    def __init__(self, meta):
        self.meta = dict(meta)

    @property
    def number(self):
        return self.meta.get("number")

    @property
    def title(self):
        return self.meta.get("title", "")

    @property
    def slug(self):
        return self.meta.get("slug", "")

    @property
    def path(self):
        return self.meta.get("path", "")

    @property
    def assets(self):
        return list(self.meta.get("assets", []))

    @property
    def short(self):
        return self.meta.get("short") or _first_paragraph(self.markdown())

    def markdown(self, image_mode="relative"):
        """Return Markdown with relative, embedded, or materialized image links."""
        text = _ticket_markdown(self.meta)
        if image_mode == "relative":
            return text
        if image_mode == "dataurl":
            return _embed_or_resolve_images(text, mode="dataurl")
        if image_mode == "absolute":
            return _embed_or_resolve_images(text, mode="absolute")
        raise ValueError("Unknown image_mode=%r" % image_mode)

    def to_dict(self):
        payload = dict(self.meta)
        payload["markdown"] = self.markdown()
        return payload

    def __repr__(self):
        return "Ticket(number=%r, title=%r)" % (self.number, self.title)


def description():
    """Return a concise description of the installed offline ticket dataset."""
    manifest = _manifest()
    tickets_meta = _all_ticket_meta()
    numbers = [item.get("number") for item in tickets_meta if item.get("number") is not None]
    minimum = min(numbers) if numbers else None
    maximum = max(numbers) if numbers else None
    source = manifest.get("source", {})

    lines = [
        "matplobblib.cv — офлайн-билеты по компьютерному зрению",
        "",
        "Источник: %s" % source.get("google_doc_title", "не указан"),
        "Билетов: %d" % len(tickets_meta),
        "Диапазон номеров: %s"
        % (("%s..%s" % (minimum, maximum)) if minimum is not None else "не задан"),
        "Формат данных: manifest.json + tickets/*.md + assets/*",
        "",
        "Примеры: show_tickets(), ticket(1), search('свёртка'), render(1)",
    ]
    return "\n".join(lines)


def _ticket_topic(item):
    """Return one plain-text topic line for the ticket index."""
    topic = _strip_markdown(item.short).strip()
    if item.number is not None:
        prefix = r"^\s*%s(?:\s*[.)]\s*|\s*[-—:]\s*|\s+)" % re.escape(
            str(item.number)
        )
        topic = re.sub(prefix, "", topic, count=1).strip()
    return topic or item.title or "Без названия"


def _tickets_markdown():
    items = sorted(
        all_tickets(),
        key=lambda item: (item.number is None, item.number or 0, item.title),
    )
    lines = ["# Вопросы", ""]
    for item in items:
        lines.extend(["%s. %s" % (item.number, _ticket_topic(item)), ""])
    return "\n".join(lines).rstrip() + "\n"


def show_tickets(mode="auto", file=None):
    """Render or return the numbered theory-ticket index."""
    if mode == "auto":
        mode = "jupyter" if _in_ipython() else "cli"

    text = _tickets_markdown()
    if mode == "jupyter":
        try:
            from IPython.display import Markdown, display

            display(Markdown(text))
        except Exception:
            (file or sys.stdout).write(text)
        return text

    if mode == "cli":
        (file or sys.stdout).write(text)
        return text

    if mode == "text":
        return text

    raise ValueError("Unknown show_tickets mode=%r" % mode)


def ticket(ref):
    """Find a ticket by number, numeric string, title, title fragment, or slug."""
    return Ticket(_resolve_meta(ref))


def all_tickets():
    """Return all tickets in manifest order."""
    return [Ticket(meta) for meta in _all_ticket_meta()]


def search(query, limit=10):
    """Search ticket titles, metadata, and Markdown content."""
    if limit is None:
        limit = 10
    if not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    if limit <= 0:
        return []

    normalized_query = _normalize_query(query)
    if not normalized_query:
        return []
    query_tokens = [token for token in re.split(r"\W+", normalized_query) if token]
    scored = []

    for meta in _all_ticket_meta():
        metadata_text = " ".join(
            [
                meta.get("title", ""),
                meta.get("slug", ""),
                meta.get("short", ""),
                " ".join(meta.get("keywords", [])),
            ]
        )
        haystack = _normalize_query(metadata_text + " " + _strip_markdown(_ticket_markdown(meta)))
        score = 50 if normalized_query in haystack else 0
        score += sum(10 for token in query_tokens if token in haystack)
        if haystack.startswith(normalized_query):
            score += 5
        if score:
            scored.append((score, meta))

    scored.sort(
        key=lambda pair: (
            -pair[0],
            pair[1].get("number", 10 ** 9),
            pair[1].get("title", ""),
        )
    )
    return [Ticket(meta) for _, meta in scored[:limit]]


def random_ticket(seed=None):
    """Return a random ticket; pass a seed for deterministic selection."""
    items = _all_ticket_meta()
    if not items:
        raise RuntimeError("No tickets found in manifest")
    return Ticket(_random.Random(seed).choice(items))


def short(ref, max_chars=280):
    """Return a ticket summary truncated to at most ``max_chars`` characters."""
    if not isinstance(max_chars, int):
        raise TypeError("max_chars must be an integer")
    if max_chars < 0:
        raise ValueError("max_chars must be non-negative")
    text = ticket(ref).short
    if len(text) <= max_chars:
        return text
    if max_chars == 0:
        return ""
    if max_chars == 1:
        return "…"
    return text[: max_chars - 1].rstrip() + "…"


def flashcards(ref, limit=12):
    """Derive simple question/answer cards from headings, definitions, and tables."""
    if not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    if limit <= 0:
        return []

    item = ticket(ref)
    lines = item.markdown().splitlines()
    cards = []

    for index, line in enumerate(lines):
        match = re.match(r"^(#{2,6})\s+(.*)", line.strip())
        if not match:
            continue
        heading = _strip_markdown(match.group(2))
        answer = ""
        for candidate_line in lines[index + 1 :]:
            if candidate_line.lstrip().startswith("#"):
                break
            candidate = _strip_markdown(candidate_line)
            if candidate:
                answer = candidate
                break
        if heading and answer:
            cards.append(
                {
                    "q": "Что относится к теме «%s»?" % heading,
                    "a": answer,
                    "source": item.title,
                }
            )

    for line in lines:
        raw = line.strip()
        if raw.startswith(("#", "|", "!")):
            continue
        match = re.match(r"^\**([A-ZА-ЯЁ][^—:-]{2,80})\**\s*[—:-]\s*(.+)$", raw)
        if match:
            term = _strip_markdown(match.group(1))
            explanation = _strip_markdown(match.group(2))
            if term and explanation:
                cards.append(
                    {
                        "q": "Что такое %s?" % term,
                        "a": explanation,
                        "source": item.title,
                    }
                )

    for line in lines:
        if not line.strip().startswith("|"):
            continue
        columns = [column.strip() for column in line.strip().strip("|").split("|")]
        if len(columns) < 2 or re.match(r"^:?-{3,}:?$", columns[0]):
            continue
        left = _strip_markdown(columns[0])
        right = _strip_markdown(columns[1])
        if left and right:
            cards.append(
                {
                    "q": "Что соответствует «%s»?" % left,
                    "a": right,
                    "source": item.title,
                }
            )

    unique = []
    seen = set()
    for card in cards:
        key = (card["q"], card["a"])
        if key not in seen:
            seen.add(key)
            unique.append(card)
    return unique[:limit]


def render(ref, mode="auto", sanitize_math=True, file=None):
    """Render a ticket, sanitizing malformed exported math by default."""
    item = ticket(ref)
    if mode == "auto":
        mode = "jupyter" if _in_ipython() else "cli"

    text = item.markdown(image_mode="relative")
    if sanitize_math:
        text = sanitize_markdown_math(text)

    if mode == "jupyter":
        text = _embed_or_resolve_images(text, mode="dataurl")
        try:
            from IPython.display import Markdown, display

            display(Markdown(text))
        except Exception:
            (file or sys.stdout).write(text + "\n")
        return text

    if mode == "cli":
        text = _embed_or_resolve_images(text, mode="absolute")
        (file or sys.stdout).write(text + "\n")
        return text

    if mode == "text":
        return text

    raise ValueError("Unknown render mode=%r" % mode)


def _print_search(results):
    if not results:
        print("No matches.")
        return
    for item in results:
        print("[%s] %s" % (item.number, item.title))
        print("  %s" % item.short)


def _coerce_ref(value):
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return value


def main(argv=None):
    """Command-line entry point used by ``python -m matplobblib.cv.CV``."""
    import argparse

    parser = argparse.ArgumentParser(prog="python -m matplobblib.cv.CV")
    subparsers = parser.add_subparsers(dest="cmd")
    subparsers.add_parser("description")
    tickets_parser = subparsers.add_parser("tickets")
    tickets_parser.add_argument(
        "--mode", choices=["auto", "jupyter", "cli", "text"], default="cli"
    )

    ticket_parser = subparsers.add_parser("ticket")
    ticket_parser.add_argument("ref")
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=10)
    random_parser = subparsers.add_parser("random")
    random_parser.add_argument("--seed", default=None)
    short_parser = subparsers.add_parser("short")
    short_parser.add_argument("ref")
    short_parser.add_argument("--max-chars", type=int, default=280)
    flashcards_parser = subparsers.add_parser("flashcards")
    flashcards_parser.add_argument("ref")
    flashcards_parser.add_argument("--limit", type=int, default=12)
    render_parser = subparsers.add_parser("render")
    render_parser.add_argument("ref")
    render_parser.add_argument(
        "--mode", choices=["auto", "jupyter", "cli", "text"], default="auto"
    )
    render_parser.add_argument(
        "--no-sanitize-math",
        action="store_false",
        dest="sanitize_math",
        help="render the original exported math without compatibility sanitizing",
    )

    args = parser.parse_args(argv)
    if args.cmd == "description":
        print(description())
        return 0
    if args.cmd == "tickets":
        show_tickets(mode=args.mode)
        return 0
    if args.cmd == "ticket":
        print(ticket(_coerce_ref(args.ref)).markdown())
        return 0
    if args.cmd == "search":
        _print_search(search(args.query, limit=args.limit))
        return 0
    if args.cmd == "random":
        item = random_ticket(seed=args.seed)
        print("[%s] %s" % (item.number, item.title))
        return 0
    if args.cmd == "short":
        print(short(_coerce_ref(args.ref), max_chars=args.max_chars))
        return 0
    if args.cmd == "flashcards":
        print(
            json.dumps(
                flashcards(_coerce_ref(args.ref), limit=args.limit),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    if args.cmd == "render":
        render(
            _coerce_ref(args.ref),
            mode=args.mode,
            sanitize_math=args.sanitize_math,
        )
        return 0
    parser.print_help()
    return 1


__all__ = [
    "Ticket",
    "all_tickets",
    "description",
    "show_tickets",
    "ticket",
    "search",
    "random_ticket",
    "short",
    "flashcards",
    "sanitize_markdown_math",
    "render",
    "main",
]


if __name__ == "__main__":
    raise SystemExit(main())
