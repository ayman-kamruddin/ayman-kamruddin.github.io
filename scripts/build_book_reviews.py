"""Build the individual static book-review pages from the shared template.

Run from the repository root: python3 scripts/build_book_reviews.py
"""

from html import escape
from json import load
from pathlib import Path
from string import Template


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = Template((ROOT / "templates" / "book_template.html").read_text())
REVIEWS_PATH = ROOT / "books" / "reviews.json"


def render_paragraphs(paragraphs: list[str]) -> str:
    return "\n".join(f"\t\t<p>{escape(paragraph, quote=False)}</p>" for paragraph in paragraphs)


def main() -> None:
    with REVIEWS_PATH.open() as reviews_file:
        reviews = load(reviews_file)

    for review in reviews:
        page = TEMPLATE.substitute(
            PAGE_TITLE=escape(review["page_title"], quote=False),
            REVIEW_HEADING=escape(review["review_heading"], quote=False),
            REVIEW_CONTENT=render_paragraphs(review["paragraphs"]),
        )
        (ROOT / "books" / review["filename"]).write_text(page)


if __name__ == "__main__":
    main()
