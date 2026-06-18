import bleach
import markdown
from markupsafe import Markup


ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS.union(
    {"p", "br", "pre", "code", "h1", "h2", "h3", "h4", "h5", "h6", "img", "table", "thead", "tbody", "tr", "th", "td"}
)
ALLOWED_ATTRIBUTES = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    "a": ["href", "title"],
    "img": ["src", "alt", "title"],
}


def sanitize_markdown(text):
    html = markdown.markdown(text or "", extensions=["extra", "nl2br"])
    clean = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    return Markup(clean)


def rating_title(value):
    return {
        5: "отлично",
        4: "хорошо",
        3: "удовлетворительно",
        2: "неудовлетворительно",
        1: "плохо",
        0: "ужасно",
    }.get(int(value), "без оценки")


def register_filters(app):
    app.jinja_env.filters["markdown"] = sanitize_markdown
    app.jinja_env.filters["rating_title"] = rating_title

