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


def test_render_sanitizes_existing_ticket_math_with_opt_out():
    raw = cv.ticket(10).markdown()
    assert "\\subscript" in raw

    sanitized = cv.render(10, mode="text")
    assert "\\subscript" not in sanitized
    assert "\\superscript" not in sanitized
    assert "\\sbracelr" not in sanitized
    assert "\\DeltaI" not in sanitized
    assert "![image](../assets/" in sanitized
    assert cv.render(10, mode="text", sanitize_math=False) == raw

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
