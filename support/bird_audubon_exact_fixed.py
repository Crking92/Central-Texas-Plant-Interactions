"""
Audubon Native Plants exact species-page scraper

Purpose
-------
Scrape Audubon's Native Plants species pages without creating false bird/resource
cross-products.

Key rule
--------
Audubon bird-family groups and plant resources are separate profile fields.
Do NOT multiply every bird group by every resource.

Outputs
-------
1. audubon_bird_family_support.csv
   One row per plant x exact Audubon bird-family group.
2. audubon_plant_resource_profiles.csv
   One row per plant with the exact Audubon resource list.
3. audubon_plant_resource_long.csv
   One row per plant x resource, for filters/UI only.
4. audubon_species_page_audit.csv
   One row per plant, with counts and warnings.
5. Audubon_Hays_Exact_Profile_Output.xlsx
   Excel workbook with all of the above sheets.

Install/run
-----------
pip install pandas openpyxl playwright
playwright install chromium
python bird_audubon_exact_fixed.py --zipcode 78666 --output-dir audubon_exact_output
"""

from __future__ import annotations

import argparse
import re
import time
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin

import pandas as pd
from playwright.sync_api import Page, sync_playwright

BASE_URL = "https://www.audubon.org"
SOURCE_NAME = "National Audubon Society Native Plants"
DEFAULT_ZIPCODE = "78666"

# Section boundaries seen on Audubon plant pages. These are intentionally broad
# so the scraper stops before footer/recommendation text can contaminate a plant.
MAY_ATTRACT_STOP_MARKERS = (
    "my saved plants",
    "where to buy",
    "clear list",
    "send my list",
    "learn more about",
)

PROFILE_STOP_MARKERS = (
    "may attract",
    "where to buy",
    "my saved plants",
)

NON_GROUP_LINES = {
    "family",
    "may attract",
    "attributes",
    "type",
    "location",
    "where to buy",
    "use location",
    "may not be native",
    "native plants",
}


def clean_line(value: str) -> str:
    """Normalize one visible text line while preserving names like New World Sparrows."""
    return re.sub(r"\s+", " ", value or "").strip()


def visible_lines(text: str) -> list[str]:
    """Return non-empty normalized body text lines."""
    return [clean_line(line) for line in text.splitlines() if clean_line(line)]


def first_text(page: Page, selectors: Iterable[str]) -> str:
    """Return the first non-empty inner_text from a list of selectors."""
    for selector in selectors:
        try:
            loc = page.locator(selector).first
            if loc.count() > 0:
                txt = clean_line(loc.inner_text(timeout=2500))
                if txt:
                    return txt
        except Exception:
            continue
    return ""


def extract_slug_name(url: str) -> str:
    slug = url.rstrip("/").split("/")[-1].split("?")[0]
    return slug.replace("-", " ").title()


def extract_names(page: Page, body_lines: list[str], url: str) -> tuple[str, str]:
    """Extract common and scientific plant names from a species page."""
    common_name = first_text(page, ["h1", ".page-title", ".common-name"])
    scientific_name = first_text(
        page,
        [
            ".scientific-name",
            ".plant-scientific-name",
            "em",
            "h1 + *",
        ],
    )

    # Text fallback based on the current Audubon page structure:
    # Native Plants / Common Name / Scientific name / Where to buy.
    if not common_name or not scientific_name:
        for i, line in enumerate(body_lines):
            if line.lower() == "native plants" and i + 2 < len(body_lines):
                possible_common = body_lines[i + 1]
                possible_scientific = body_lines[i + 2]
                if not common_name and possible_common.lower() not in NON_GROUP_LINES:
                    common_name = possible_common
                if not scientific_name and looks_like_scientific_name(possible_scientific):
                    scientific_name = possible_scientific
                break

    # Another fallback: page title appears before scientific name and "Where to buy".
    if not scientific_name:
        for i, line in enumerate(body_lines):
            if line.lower() == "where to buy" and i >= 1:
                candidate = body_lines[i - 1]
                if looks_like_scientific_name(candidate):
                    scientific_name = candidate
                    if not common_name and i >= 2:
                        common_name = body_lines[i - 2]
                break

    if common_name and scientific_name and scientific_name in common_name:
        common_name = clean_line(common_name.replace(scientific_name, ""))

    if not common_name:
        common_name = extract_slug_name(url)
    if not scientific_name:
        scientific_name = ""

    return common_name, scientific_name


def looks_like_scientific_name(value: str) -> bool:
    """Loose check for binomial/trinomial plant names."""
    value = clean_line(value)
    return bool(re.match(r"^[A-Z][a-z-]+\s+[a-z][a-z.-]+(?:\s+(?:var\.|ssp\.|subsp\.|f\.)?\s?[a-z][a-z.-]+)?$", value))


def extract_type(body_lines: list[str]) -> str:
    for i, line in enumerate(body_lines):
        if line.lower() == "type" and i + 1 < len(body_lines):
            return body_lines[i + 1]
    return ""


def extract_attributes(body_lines: list[str]) -> list[str]:
    """Extract the exact resource list from the Attributes line only."""
    for i, line in enumerate(body_lines):
        if line.lower() == "attributes" and i + 1 < len(body_lines):
            raw = body_lines[i + 1]
            # Audubon commonly gives one comma-separated line: Fruit, Nuts, Seeds
            resources = [clean_line(x) for x in raw.split(",") if clean_line(x)]
            return list(dict.fromkeys(resources))
    return []


def extract_description(body_lines: list[str]) -> str:
    """Capture the short plant description after attributes, if present."""
    try:
        start = next(i for i, line in enumerate(body_lines) if line.lower() == "attributes") + 2
    except StopIteration:
        return ""

    parts: list[str] = []
    for line in body_lines[start:]:
        low = line.lower()
        if any(low.startswith(stop) for stop in PROFILE_STOP_MARKERS):
            break
        # Skip photo credits and obvious UI labels.
        if low.startswith("photo:") or low in NON_GROUP_LINES:
            continue
        parts.append(line)
    return " ".join(parts).strip()


def extract_may_attract_groups(body_lines: list[str]) -> list[str]:
    """Extract exact bird-family group labels from the plant's May Attract section.

    Important: this reads only the species page section after "May Attract" and
    only accepts labels that follow an explicit "Family" line. It does not scan
    the whole page for bird keywords, so global filters/footer text cannot leak in.
    """
    start = None
    for i, line in enumerate(body_lines):
        if line.lower() == "may attract":
            start = i
            break
    if start is None:
        return []

    section: list[str] = []
    for line in body_lines[start + 1 :]:
        low = line.lower()
        if any(low.startswith(stop) for stop in MAY_ATTRACT_STOP_MARKERS):
            break
        section.append(line)

    groups: list[str] = []
    for i, line in enumerate(section):
        if line.lower() == "family":
            # Next non-empty, non-caption, non-UI line should be the exact Audubon group.
            for candidate in section[i + 1 : i + 5]:
                c = clean_line(candidate)
                low = c.lower()
                if not c:
                    continue
                if low in NON_GROUP_LINES:
                    continue
                if low.startswith("image") or low.startswith("photo:"):
                    continue
                if "photo:" in low and "audubon" in low:
                    continue
                groups.append(c)
                break

    # Preserve Audubon's original names/order, but remove accidental duplicates.
    return list(dict.fromkeys(groups))


def normalize_resource_terms(resources: list[str]) -> str:
    """A compact machine-friendly resource profile for filtering/scoring."""
    mapping = {
        "butterflies": "butterflies",
        "caterpillars": "caterpillars",
        "fruit": "fruit",
        "nectar": "nectar",
        "nuts": "nuts",
        "seeds": "seeds",
    }
    normalized = []
    for r in resources:
        low = r.lower()
        normalized.append(mapping.get(low, low))
    return "; ".join(list(dict.fromkeys(normalized)))


def collect_species_urls(page: Page, zipcode: str, delay_seconds: float = 1.5) -> list[str]:
    """Collect all native plant species links from Audubon's zipcode result pages."""
    plant_urls: list[str] = []
    start_url = f"{BASE_URL}/native-plants/best-results?zipcode={zipcode}"
    page.goto(start_url, wait_until="networkidle", timeout=45000)

    page_number = 1
    while True:
        print(f"Scanning results page {page_number}...")
        page.wait_for_selector("a[href*='/native-plants/species/']", timeout=20000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(delay_seconds)

        for link in page.query_selector_all("a[href*='/native-plants/species/']"):
            href = link.get_attribute("href")
            if not href:
                continue
            full_url = urljoin(BASE_URL, href.split("#")[0])
            if "/native-plants/species/" in full_url and full_url not in plant_urls:
                plant_urls.append(full_url)

        next_button = page.query_selector(
            ".pager__item--next a, a[title='Go to next page'], a[rel='next'], a:has-text('Next')"
        )
        if not next_button:
            break
        try:
            if not next_button.is_visible():
                break
            next_button.click()
            page.wait_for_load_state("networkidle", timeout=30000)
            time.sleep(delay_seconds)
            page_number += 1
        except Exception:
            break

    return plant_urls


def scrape_species_page(page: Page, url: str, delay_seconds: float = 0.75) -> dict:
    """Scrape one Audubon species page into an exact profile dictionary."""
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(delay_seconds)
    body_text = page.locator("body").inner_text(timeout=10000)
    lines = visible_lines(body_text)

    common_name, scientific_name = extract_names(page, lines, url)
    plant_type = extract_type(lines)
    resources = extract_attributes(lines)
    bird_groups = extract_may_attract_groups(lines)
    description = extract_description(lines)

    warnings: list[str] = []
    if not scientific_name:
        warnings.append("missing_scientific_name")
    if not resources:
        warnings.append("missing_attributes")
    if not bird_groups:
        warnings.append("missing_may_attract_groups")

    return {
        "plant_common_name": common_name,
        "plant_scientific_name": scientific_name,
        "plant_type": plant_type,
        "audubon_attributes_original": "; ".join(resources),
        "audubon_attributes_normalized": normalize_resource_terms(resources),
        "audubon_bird_groups_original": "; ".join(bird_groups),
        "audubon_bird_group_count": len(bird_groups),
        "audubon_resource_count": len(resources),
        "description": description,
        "source_url_or_citation": url,
        "evidence_source": SOURCE_NAME,
        "audit_flags": "; ".join(warnings),
        "resources_list": resources,
        "bird_groups_list": bird_groups,
    }


def build_output_tables(profiles: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Build dashboard-safe Audubon output tables."""
    bird_rows: list[dict] = []
    resource_long_rows: list[dict] = []

    for profile in profiles:
        base = {
            "plant_scientific_name": profile["plant_scientific_name"],
            "plant_common_name": profile["plant_common_name"],
            "plant_type": profile["plant_type"],
            "evidence_source": profile["evidence_source"],
            "source_url_or_citation": profile["source_url_or_citation"],
            "audubon_attributes_original": profile["audubon_attributes_original"],
            "audubon_attributes_normalized": profile["audubon_attributes_normalized"],
        }

        # One row per plant x exact Audubon bird-family group.
        # No fruit/seed/nectar multiplication.
        for group in profile["bird_groups_list"]:
            bird_rows.append(
                {
                    **base,
                    "bird_common_name": group,
                    "bird_group_original": group,
                    "bird_scientific_name": "",
                    "rank": "audubon_broad_family_group",
                    "interaction_class": "habitat/resource support",
                    "interaction_type": "Audubon broad bird-family support",
                    "direct_species_interaction": False,
                    "direct_food_interaction": False,
                    "score_use": "trusted broad profile support",
                    "evidence_level": "D - trusted Audubon broad plant profile; not species-level direct interaction",
                    "evidence_notes": (
                        "Audubon states this plant is thought to attract this broad family/group of birds. "
                        "Attributes are plant-level resources and are not assigned to individual bird groups."
                    ),
                }
            )

        # Separate resource/filter rows. These are not bird interaction claims.
        for resource in profile["resources_list"]:
            resource_long_rows.append(
                {
                    **base,
                    "resource_original": resource,
                    "resource_normalized": normalize_resource_terms([resource]),
                    "resource_claim_type": "plant-level Audubon attribute",
                    "direct_bird_interaction": False,
                }
            )

    plant_profiles = []
    for profile in profiles:
        plant_profiles.append(
            {
                key: value
                for key, value in profile.items()
                if key not in {"resources_list", "bird_groups_list"}
            }
        )

    bird_df = pd.DataFrame(bird_rows).drop_duplicates() if bird_rows else pd.DataFrame()
    resource_profile_df = pd.DataFrame(plant_profiles).drop_duplicates() if plant_profiles else pd.DataFrame()
    resource_long_df = pd.DataFrame(resource_long_rows).drop_duplicates() if resource_long_rows else pd.DataFrame()
    audit_df = resource_profile_df[
        [
            "plant_scientific_name",
            "plant_common_name",
            "audubon_bird_group_count",
            "audubon_resource_count",
            "audit_flags",
            "source_url_or_citation",
        ]
    ].copy() if not resource_profile_df.empty else pd.DataFrame()

    return bird_df, resource_profile_df, resource_long_df, audit_df


def scrape_audubon_exact(zipcode: str = DEFAULT_ZIPCODE, output_dir: str | Path = "audubon_exact_output") -> dict[str, pd.DataFrame]:
    """Run the exact Audubon species-page scraper and write output files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1440, "height": 1200},
        )
        page = context.new_page()

        print(f"Collecting Audubon plant species pages for ZIP {zipcode}...")
        urls = collect_species_urls(page, zipcode)
        print(f"Found {len(urls)} unique species URLs.")

        profiles: list[dict] = []
        for idx, url in enumerate(urls, start=1):
            print(f"Scraping {idx}/{len(urls)}: {url}")
            try:
                profiles.append(scrape_species_page(page, url))
            except Exception as exc:
                print(f"  WARNING: failed to scrape {url}: {exc}")
                profiles.append(
                    {
                        "plant_common_name": extract_slug_name(url),
                        "plant_scientific_name": "",
                        "plant_type": "",
                        "audubon_attributes_original": "",
                        "audubon_attributes_normalized": "",
                        "audubon_bird_groups_original": "",
                        "audubon_bird_group_count": 0,
                        "audubon_resource_count": 0,
                        "description": "",
                        "source_url_or_citation": url,
                        "evidence_source": SOURCE_NAME,
                        "audit_flags": f"scrape_failed: {exc}",
                        "resources_list": [],
                        "bird_groups_list": [],
                    }
                )

        browser.close()

    bird_df, profile_df, resource_long_df, audit_df = build_output_tables(profiles)

    files = {
        "audubon_bird_family_support.csv": bird_df,
        "audubon_plant_resource_profiles.csv": profile_df,
        "audubon_plant_resource_long.csv": resource_long_df,
        "audubon_species_page_audit.csv": audit_df,
    }

    for filename, df in files.items():
        df.to_csv(output_path / filename, index=False)

    workbook = output_path / "Audubon_Hays_Exact_Profile_Output.xlsx"
    with pd.ExcelWriter(workbook, engine="openpyxl") as writer:
        bird_df.to_excel(writer, index=False, sheet_name="bird_family_support")
        profile_df.to_excel(writer, index=False, sheet_name="plant_profiles")
        resource_long_df.to_excel(writer, index=False, sheet_name="resource_long")
        audit_df.to_excel(writer, index=False, sheet_name="audit")

    print("\nDONE")
    print(f"Bird-family support rows: {len(bird_df)}")
    print(f"Plant profiles: {len(profile_df)}")
    print(f"Output folder: {output_path.resolve()}")

    return {
        "bird_family_support": bird_df,
        "plant_profiles": profile_df,
        "resource_long": resource_long_df,
        "audit": audit_df,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape exact Audubon species-page bird-family support data.")
    parser.add_argument("--zipcode", default=DEFAULT_ZIPCODE, help="ZIP code for Audubon native plant search.")
    parser.add_argument("--output-dir", default="audubon_exact_output", help="Folder for CSV/XLSX outputs.")
    args = parser.parse_args()
    scrape_audubon_exact(zipcode=args.zipcode, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
