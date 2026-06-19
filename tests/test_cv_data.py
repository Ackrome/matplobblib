import importlib
import re
from pathlib import Path

from matplobblib import cv
from matplobblib.cv.CV import _manifest, _materialize_asset, _resource


def test_manifest_loads():
    manifest = _manifest()
    assert manifest["format_version"] == 1
    assert isinstance(manifest["tickets"], list)
    assert isinstance(manifest["assets"], list)


def test_at_least_one_ticket_exists():
    assert cv.all_tickets()


def test_only_numbered_theory_tickets_are_packaged():
    manifest = _manifest()
    entries = manifest["tickets"]
    assert [entry["number"] for entry in entries] == list(range(1, 49))
    assert all(
        re.match(
            r"^%s(?:$|[\s.):—-])" % entry["number"],
            entry["title"],
        )
        for entry in entries
    )

    manifest_paths = {entry["path"] for entry in entries}
    packaged_paths = {
        "tickets/%s" % resource.name
        for resource in _resource("tickets").iterdir()
        if resource.is_file() and resource.name.endswith(".md")
    }
    assert packaged_paths == manifest_paths


def test_ticket_lookup_by_number_works():
    first = _manifest()["tickets"][0]
    item = cv.ticket(first["number"])
    assert item.number == first["number"]
    assert item.title == first["title"]
    assert item.markdown().startswith("# ")


def test_show_tickets_replaces_the_questions_service_tab():
    markdown = cv.show_tickets(mode="text")
    listed_numbers = [
        int(number) for number in re.findall(r"^(\d+)\. ", markdown, re.MULTILINE)
    ]

    assert markdown.startswith("# Вопросы\n")
    assert listed_numbers == list(range(1, 49))
    assert "Практика" not in markdown
    assert "show_tickets()" in cv.description()


def test_search_works_and_normalizes_yo():
    limit = len(cv.all_tickets())
    results_without_yo = cv.search("свертка", limit=limit)
    results_with_yo = cv.search("свёртка", limit=limit)

    assert isinstance(results_without_yo, list)
    assert results_without_yo
    assert [item.path for item in results_without_yo] == [
        item.path for item in results_with_yo
    ]


def test_short_summary_works():
    first = cv.all_tickets()[0]
    full_summary = cv.short(first, max_chars=10_000)
    summary = cv.short(first, max_chars=48)

    assert summary
    assert len(summary) <= 48
    if len(full_summary) > 48:
        assert summary.endswith("…")
    else:
        assert summary == full_summary


def test_markdown_image_links_resolve_to_package_assets():
    pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    resolved_count = 0

    for item in cv.all_tickets():
        for target in pattern.findall(item.markdown()):
            relative = target.strip()
            if relative.startswith("../"):
                relative = relative[3:]
            elif relative.startswith("./"):
                relative = relative[2:]
            if relative.startswith("assets/"):
                local_path = _materialize_asset(relative)
                assert local_path is not None
                assert Path(local_path).is_file()
                resolved_count += 1

    assert resolved_count > 0


def test_repair_iou_formula():
    bad = "textIoU =\nfractextArea(B_pcapB_gt)textArea(B_pcupB_gt)"
    fixed = cv.repair_markdown_math(bad)

    assert "\\mathrm{IoU}" in fixed
    assert "\\frac" in fixed
    assert "\\cap" in fixed
    assert "\\cup" in fixed
    assert "fractext" not in fixed
    assert "pcap" not in fixed
    assert "pcup" not in fixed


def test_repair_known_equation_tokens():
    bad = "\n".join(
        (
            "textArea",
            "fracAB",
            "pcap",
            "pcup",
            "subscriptG_x",
            "superscriptG_y",
        )
    )
    fixed = cv.repair_markdown_math(bad)

    assert "\\mathrm{Area}" in fixed
    assert "\\frac{A}{B}" in fixed
    assert "\\cap" in fixed
    assert "\\cup" in fixed
    assert "$G_x$" in fixed
    assert "$G^y$" in fixed
    assert not any(
        token in fixed
        for token in ("textArea", "fracAB", "pcap", "pcup", "subscript", "superscript")
    )

def test_repair_ap_formula():
    bad = "AP =\nint_0^1 p(r)dr"
    fixed = cv.repair_markdown_math(bad)

    assert "\\int_0^1" in fixed
    assert "\\,dr" in fixed


def test_repair_map_formula():
    bad = "mAP =\nfrac1N\nsum_i = 1^N AP_i"
    fixed = cv.repair_markdown_math(bad)

    assert "\\frac{1}{N}" in fixed
    assert "\\sum_{i=1}^{N}" in fixed


def test_repair_preserves_images_fenced_code_and_prose():
    fence = chr(96) * 3
    code = (
        fence
        + "text\ntextIoU =\n"
        + "fractextArea(B_pcapB_gt)textArea(B_pcupB_gt)\n"
        + fence
    )
    image = "![image](../assets/example.png)"
    prose = "This normal text mentions Area and union without being a formula."
    markdown = code + "\n\n" + image + "\n\n" + prose

    assert cv.repair_markdown_math(markdown) == markdown


def test_repair_real_ticket_35():
    raw = cv.ticket(35).markdown()
    fixed = cv.repair_markdown_math(raw)
    rendered = cv.render(35, mode="text")

    forbidden = (
        "fractext",
        "textArea",
        "textIoU",
        "pcap",
        "pcup",
        "subscript",
        "superscript",
    )
    assert not any(token in fixed for token in forbidden)
    assert not any(token in rendered for token in forbidden)
    assert "\\mathrm{IoU}" in rendered
    assert "\\frac" in rendered
    assert "\\cap" in rendered
    assert "\\cup" in rendered
    assert "\\\\mathrm" not in rendered
    assert "\\\\frac" not in rendered

def test_math_sanitizer_neutralizes_google_docs_pseudo_latex():
    markdown = (
        r"Horizontal ($\subscriptG_x$), vertical ($\superscriptG_y$), "
        r"combined $\subscriptG_x + \subscriptG_y$, "
        r"legacy $\Equation \EquationFunction \EquationSymbol \DeltaI$."
    )
    sanitized = cv.sanitize_markdown_math(markdown)

    assert "\\subscript" not in sanitized
    assert "\\superscript" not in sanitized
    assert "\\Equation" not in sanitized
    assert "G\\_x" in sanitized
    assert "G\\_y" in sanitized
    assert "ΔI" in sanitized
    assert "ParserError" not in sanitized


def test_math_sanitizer_preserves_images_text_and_valid_latex():
    markdown = (
        "Normal text ![plot](../assets/plot.png) "
        r"with valid $G_x = \sqrt{x^2 + y^2}$ and $\Theta$."
    )
    assert cv.sanitize_markdown_math(markdown) == markdown


def test_render_sanitizes_legacy_math_with_opt_out(monkeypatch):
    cv_module = importlib.import_module("matplobblib.cv.CV")
    item = cv.ticket(10)
    assert item.assets
    legacy_markdown = (
        "# 10\n\n"
        r"Legacy ($\subscriptG_x$), $\superscriptG_y + \DeltaI$."
        "\n\n![image](../%s)\n" % item.assets[0]
    )
    monkeypatch.setattr(cv_module, "_ticket_markdown", lambda meta: legacy_markdown)

    sanitized = cv.render(10, mode="text")
    assert "\\subscript" not in sanitized
    assert "\\superscript" not in sanitized
    assert "\\sbracelr" not in sanitized
    assert "\\DeltaI" not in sanitized
    assert "![image](../assets/" in sanitized
    assert cv.render(10, mode="text", sanitize_math=False) == legacy_markdown

    notebook_markdown = cv.render(10, mode="jupyter")
    assert "\\subscript" not in notebook_markdown
    assert "data:image/png;base64," in notebook_markdown


def test_jupyter_render_embeds_images_as_data_urls_without_crashing():
    item = next(ticket for ticket in cv.all_tickets() if ticket.assets)
    markdown = cv.render(item, mode="jupyter")

    assert re.search(r"\]\(data:image/[^;]+;base64,", markdown)


def test_flashcards_and_seeded_random_ticket():
    card = next(
        (
            cards[0]
            for item in cv.all_tickets()
            if (cards := cv.flashcards(item, limit=1))
        ),
        None,
    )
    assert card is not None
    assert {"q", "a", "source"} <= card.keys()

    first_pick = cv.random_ticket(seed=42)
    second_pick = cv.random_ticket(seed=42)
    assert first_pick.path == second_pick.path
