import re


def normalize(text):
    """Lowercase and turn '-' and '/' into spaces, so 'SDE-1' matches 'sde 1'."""
    text = (text or "").lower()
    return text.replace("-", " ").replace("/", " ")


def has_word(text, words):
    """True if any word or phrase appears in text as a whole word."""
    for word in words:
        if re.search(rf"\b{re.escape(word)}\b", text):
            return True
    return False


def location_ok(location, india_words):
    """True if the location mentions India or an Indian city.
    'Remote - India' passes because it contains 'india'."""
    return has_word(location, india_words)


def match_level(job, filters):
    """Return 'strong', 'possible', or None."""
    title = normalize(job["title"])
    location = normalize(job["location"])

    if has_word(title, filters["exclude_words"]):
        return None
    if not has_word(title, filters["tech_words"]):
        return None
    if not location_ok(location, filters["india_words"]):
        return None
    if has_word(title, filters["level_words"]):
        return "strong"
    if has_word(title, filters["possible_words"]):
        return "possible"
    return None


def is_match(job, filters):
    """Kept so test_filters.py still works: True only for strong matches."""
    return match_level(job, filters) == "strong"