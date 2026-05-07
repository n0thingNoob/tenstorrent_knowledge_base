#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


USER_AGENT = "tenstorrent-wiki-collector/0.1 (+local research vault)"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def slugify(value: str, fallback: str = "item") -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return normalized[:100] or fallback


def normalize_whitespace(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def strip_html_to_text(value: str) -> str:
    value = re.sub(r"(?is)<script.*?</script>", " ", value)
    value = re.sub(r"(?is)<style.*?</style>", " ", value)
    value = re.sub(r"(?is)<noscript.*?</noscript>", " ", value)
    value = re.sub(r"(?is)<svg.*?</svg>", " ", value)
    return normalize_whitespace(value)


def wrap_summary(value: str) -> str:
    return "\n".join(textwrap.wrap(value, width=100)) if value else ""


def parse_iso_date(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    patterns = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S GMT",
        "%B %d, %Y",
        "%b %d, %Y",
    ]
    for pattern in patterns:
        try:
            parsed = dt.datetime.strptime(value, pattern)
            return parsed.date().isoformat()
        except ValueError:
            continue
    return value


def within_since_days(published: str | None, since_days: int | None) -> bool:
    if not published or since_days is None:
        return True
    try:
        published_date = dt.date.fromisoformat(published)
    except ValueError:
        return True
    cutoff = dt.date.today() - dt.timedelta(days=since_days)
    return published_date >= cutoff


def parse_feed_entries(feed_xml: str) -> list[dict]:
    root = ET.fromstring(feed_xml)
    entries: list[dict] = []

    if root.tag.endswith("rss") or root.find("./channel") is not None:
        for item in root.findall("./channel/item"):
            title = item.findtext("title", default="Untitled")
            link = item.findtext("link", default="").strip()
            summary = item.findtext("description", default="")
            published = parse_iso_date(item.findtext("pubDate"))
            entries.append(
                {
                    "title": normalize_whitespace(title),
                    "link": link,
                    "summary": normalize_whitespace(summary),
                    "published": published,
                }
            )
        return entries

    for entry in root.findall("atom:entry", ATOM_NS):
        title = entry.findtext("atom:title", default="Untitled", namespaces=ATOM_NS)
        summary = entry.findtext("atom:summary", default="", namespaces=ATOM_NS)
        published = (
            entry.findtext("atom:published", default="", namespaces=ATOM_NS)
            or entry.findtext("atom:updated", default="", namespaces=ATOM_NS)
        )
        link = ""
        for link_node in entry.findall("atom:link", ATOM_NS):
            rel = link_node.attrib.get("rel", "alternate")
            href = link_node.attrib.get("href", "")
            if rel == "alternate" and href:
                link = href
                break
        if not link:
            id_value = entry.findtext("atom:id", default="", namespaces=ATOM_NS)
            link = id_value.strip()
        authors = [
            author.findtext("atom:name", default="", namespaces=ATOM_NS)
            for author in entry.findall("atom:author", ATOM_NS)
        ]
        entries.append(
            {
                "title": normalize_whitespace(title),
                "link": link,
                "summary": normalize_whitespace(summary),
                "published": parse_iso_date(published),
                "authors": [author for author in authors if author],
            }
        )
    return entries


def collect_feed_source(source: dict) -> list[dict]:
    xml_text = fetch_text(source["url"])
    entries = parse_feed_entries(xml_text)
    results: list[dict] = []
    for entry in entries[: source.get("max_items", 20)]:
        entry["source_name"] = source["name"]
        entry["source_type"] = source["source_type"]
        entry["evidence_hint"] = source.get("evidence_hint", source["source_type"])
        results.append(entry)
    return results


def extract_html_candidates(index_html: str, base_url: str, url_patterns: list[str]) -> list[str]:
    matches = re.findall(r"""href=["']([^"'#>]+)["']""", index_html, flags=re.IGNORECASE)
    compiled = [re.compile(pattern) for pattern in url_patterns]
    candidates: list[str] = []
    seen: set[str] = set()
    for href in matches:
        absolute = urllib.parse.urljoin(base_url, href)
        if absolute in seen:
            continue
        if compiled and not any(pattern.search(absolute) for pattern in compiled):
            continue
        seen.add(absolute)
        candidates.append(absolute)
    return candidates


def extract_meta_content(page_html: str, attr_name: str, attr_value: str) -> str | None:
    pattern = rf"""<meta[^>]+{attr_name}=["']{re.escape(attr_value)}["'][^>]+content=["']([^"']+)["']"""
    match = re.search(pattern, page_html, flags=re.IGNORECASE)
    if match:
        return normalize_whitespace(match.group(1))
    return None


def extract_page_record(url: str, source: dict) -> dict | None:
    page_html = fetch_text(url)
    title_match = re.search(r"(?is)<title>(.*?)</title>", page_html)
    title = normalize_whitespace(title_match.group(1)) if title_match else url
    summary = (
        extract_meta_content(page_html, "name", "description")
        or extract_meta_content(page_html, "property", "og:description")
        or ""
    )
    published = None
    time_match = re.search(r"""<time[^>]+datetime=["']([^"']+)["']""", page_html, flags=re.IGNORECASE)
    if time_match:
        published = parse_iso_date(time_match.group(1))
    if not published:
        posted_match = re.search(r"Posted on\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", page_html)
        if posted_match:
            published = parse_iso_date(posted_match.group(1))
    content_text = strip_html_to_text(page_html)
    include_keywords = [keyword.lower() for keyword in source.get("include_keywords", [])]
    if include_keywords:
        haystack = " ".join([title, summary, content_text[:4000]]).lower()
        if not any(keyword in haystack for keyword in include_keywords):
            return None
    return {
        "title": title,
        "link": url,
        "summary": summary,
        "published": published,
        "source_name": source["name"],
        "source_type": source["source_type"],
        "evidence_hint": source.get("evidence_hint", source["source_type"]),
        "body_text": content_text[: source.get("max_body_chars", 50000)],
    }


def collect_html_index_source(source: dict) -> list[dict]:
    index_html = fetch_text(source["url"])
    candidates = extract_html_candidates(index_html, source["url"], source.get("url_patterns", []))
    results: list[dict] = []
    for candidate in candidates[: source.get("max_candidates", 12)]:
        try:
            record = extract_page_record(candidate, source)
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] failed to fetch article {candidate}: {exc}", file=sys.stderr)
            continue
        if record:
            results.append(record)
    return results


def collect_source(source: dict) -> list[dict]:
    kind = source["kind"]
    if kind == "feed":
        return collect_feed_source(source)
    if kind == "html_index":
        return collect_html_index_source(source)
    raise ValueError(f"Unsupported source kind: {kind}")


def build_raw_markdown(record: dict, collected_at: str) -> str:
    title = record["title"]
    metadata_lines = [
        f"- Source URL: {record['link']}",
        f"- Published: {record.get('published') or 'unknown'}",
        f"- Collected: {collected_at}",
        f"- Collector: weekly_source_collect.py",
        f"- Source bucket: {record['source_type']}",
        f"- Evidence hint: {record['evidence_hint']}",
    ]
    authors = record.get("authors") or []
    if authors:
        metadata_lines.append(f"- Authors: {', '.join(authors)}")
    summary = wrap_summary(record.get("summary", ""))
    body_text = record.get("body_text", "")
    body_section = ""
    if body_text:
        body_section = f"\n## Extracted text\n\n{body_text}\n"
    return "\n".join(
        [
            f"# {title}",
            "",
            "## Source metadata",
            "",
            *metadata_lines,
            "",
            "## Summary snippet",
            "",
            summary or "No summary available.",
            body_section.rstrip(),
            "",
        ]
    ).strip() + "\n"


def write_raw_record(raw_dir: Path, record: dict, collected_date: str, dry_run: bool) -> Path:
    slug = slugify(record["title"], fallback=slugify(record["source_name"]))
    filename = f"{collected_date}__{record['source_type']}__{slug}.md"
    destination = raw_dir / filename
    if dry_run:
        return destination
    raw_dir.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        build_raw_markdown(record, collected_at=utc_now().isoformat(timespec="seconds")),
        encoding="utf-8",
    )
    return destination


def build_report(records: list[dict], skipped: list[str], run_date: str) -> str:
    lines = [
        "# Weekly Source Collection Report",
        "",
        f"- Run date: {run_date}",
        f"- New raw files: {len(records)}",
        f"- Skipped duplicates/old items: {len(skipped)}",
        "",
        "## New files",
        "",
    ]
    if records:
        for record in records:
            lines.extend(
                [
                    f"- `{record['raw_path']}`",
                    f"  - Title: {record['title']}",
                    f"  - Source: {record['source_name']}",
                    f"  - Published: {record.get('published') or 'unknown'}",
                    f"  - URL: {record['link']}",
                ]
            )
    else:
        lines.append("- None.")

    lines.extend(["", "## Skipped", ""])
    if skipped:
        for item in skipped:
            lines.append(f"- {item}")
    else:
        lines.append("- None.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect weekly Tenstorrent-related source candidates into raw/.")
    parser.add_argument("--config", default="scripts/source_feeds.json")
    parser.add_argument("--state", default="scripts/source_collection_state.json")
    parser.add_argument("--raw-dir", default="raw")
    parser.add_argument("--outputs-dir", default="outputs")
    parser.add_argument("--since-days", type=int, default=14)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_root = Path.cwd()
    config_path = repo_root / args.config
    state_path = repo_root / args.state
    raw_dir = repo_root / args.raw_dir
    outputs_dir = repo_root / args.outputs_dir

    config = load_json(config_path, default={"sources": []})
    state = load_json(state_path, default={"seen_urls": {}, "runs": []})

    collected_date = dt.date.today().isoformat()
    new_records: list[dict] = []
    skipped: list[str] = []

    for source in config.get("sources", []):
        try:
            records = collect_source(source)
        except Exception as exc:  # noqa: BLE001
            skipped.append(f"{source['name']}: fetch failed ({exc})")
            continue

        for record in records:
            link = record.get("link")
            if not link:
                skipped.append(f"{source['name']}: missing URL for {record.get('title', 'untitled')}")
                continue
            if link in state.get("seen_urls", {}):
                skipped.append(f"duplicate URL: {record['title']}")
                continue
            if not within_since_days(record.get("published"), args.since_days):
                skipped.append(f"old item: {record['title']}")
                continue

            raw_path = write_raw_record(raw_dir, record, collected_date, args.dry_run)
            record["raw_path"] = raw_path.relative_to(repo_root).as_posix()
            new_records.append(record)
            if not args.dry_run:
                state.setdefault("seen_urls", {})[link] = {
                    "title": record["title"],
                    "raw_path": record["raw_path"],
                    "collected": collected_date,
                }

    report_name = f"source-collection-{collected_date}.md"
    report_path = outputs_dir / report_name
    report_text = build_report(new_records, skipped, collected_date)
    if not args.dry_run:
        outputs_dir.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_text, encoding="utf-8")
        state.setdefault("runs", []).append(
            {
                "date": collected_date,
                "new_files": len(new_records),
                "report": report_path.relative_to(repo_root).as_posix(),
            }
        )
        save_json(state_path, state)

    print(report_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
