import httpx
from selectolax.parser import HTMLParser


DEFAULT_HEADERS = {
    # basic browser UA to reduce blocking; override by passing headers
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

def get_content(url: str = None, headers: dict = None) -> str | None:
    """
    Fetch and return body HTML as a string, or None on failure.
    Call this from other modules instead of importing top-level variables.
    """
    target = url
    hdrs = {**DEFAULT_HEADERS, **(headers or {})}
    try:
        response = httpx.get(target, headers=hdrs, timeout=15.0)
    except Exception as e:
        print(f"Failed to fetch {target}: {e}")
        return None

    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

    try:
        tree = HTMLParser(response.text)
        # prefer just the text of the body (no scripts/styles); use html if you need markup
        if tree.body is None:
            return tree.html  # fallback to whole document
        return tree.body.html or tree.body.text()
    except Exception as e:
        print(f"Failed to parse HTML: {e}")
        return None

if __name__ == "__main__":
    # keep script runnable for quick tests
    cont = get_content()
    if cont:
        print(cont)
