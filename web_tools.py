import requests
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": "KTJ-MI_miniProject/1.0 (email: lpgjpz@hallgato.uniduna.hu)"
}


def search_duckduckgo(query: str):
    q = query.strip()
    if not q:
        return {"text": "", "url": ""}
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": q,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code != 200:
            return {"text": "", "url": ""}
        data = resp.json()
        text = data.get("AbstractText") or ""
        related = data.get("RelatedTopics") or []
        if not text and related:
            for item in related:
                if isinstance(item, dict) and item.get("Text"):
                    text = item["Text"]
                    break
        link = data.get("AbstractURL") or ""
        if not link and related:
            for item in related:
                if isinstance(item, dict) and item.get("FirstURL"):
                    link = item["FirstURL"]
                    break
        if not link:
            link = "https://duckduckgo.com/?q=" + quote_plus(q)
        return {"text": text, "url": link}
    except Exception:
        return {"text": "", "url": ""}


def search_wikipedia_lang(query: str, lang: str):
    q = query.strip()
    if not q:
        return {"text": "", "url": ""}
    try:
        base = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": q,
            "format": "json"
        }
        resp = requests.get(base, params=params, headers=HEADERS, timeout=5)
        if resp.status_code != 200:
            return {"text": "", "url": ""}
        data = resp.json()
        results = data.get("query", {}).get("search", [])
        if not results:
            return {"text": "", "url": ""}
        title = results[0]["title"]
        summary_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/" + title.replace(" ", "_")
        resp2 = requests.get(summary_url, headers=HEADERS, timeout=5)
        if resp2.status_code != 200:
            return {"text": "", "url": ""}
        data2 = resp2.json()
        extract = data2.get("extract") or ""
        if not extract:
            return {"text": "", "url": ""}
        parts = extract.split(".")
        if len(parts) > 2:
            text = ".".join(parts[:2]) + "."
        else:
            text = extract
        content_urls = data2.get("content_urls") or {}
        desktop = content_urls.get("desktop") or {}
        page_url = desktop.get("page") or ""
        if not page_url:
            page_url = f"https://{lang}.wikipedia.org/wiki/" + title.replace(" ", "_")
        return {"text": text, "url": page_url}
    except Exception:
        return {"text": "", "url": ""}


def search_wikipedia_hu(query: str):
    return search_wikipedia_lang(query, "hu")


def search_wikipedia_en(query: str):
    return search_wikipedia_lang(query, "en")


def search_web(query: str):
    r = search_duckduckgo(query)
    if r["text"]:
        return r
    r = search_wikipedia_hu(query)
    if r["text"]:
        return r
    r = search_wikipedia_en(query)
    return r
