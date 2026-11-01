"""
Multi-region holiday date module.

Returns the actual dates of retail-relevant holidays for any given year, across
the three regions the skill supports (US, UK/EU, Canada/AU/NZ).

Many holidays have computed dates that vary year-to-year:
- 4th Thursday of November (Thanksgiving — US)
- 2nd Sunday in May (Mother's Day — US, Canada, AU/NZ)
- 4th Sunday of Lent (UK Mother's Day / Mothering Sunday — requires Easter calculation)
- last Monday of May (Memorial Day — US)
- etc.

This module implements the date arithmetic so the calendar can correctly
position campaigns regardless of which year the buyer plans for.

Usage from another script:
    from holiday_dates import holidays_for_region_in_range, easter_for_year

    holidays = holidays_for_region_in_range("us", date(2026, 5, 1), date(2026, 12, 31))
    # Returns list of {"date": date, "name": str, "type": str, "retail_relevance": str}
"""

import argparse
import json
import sys
from datetime import date, timedelta


# ============================================================================
# DATE ARITHMETIC HELPERS
# ============================================================================

def nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date:
    """
    Return the date of the Nth occurrence of `weekday` (0=Mon, 6=Sun) in
    the given month/year. E.g., 4th Thursday of November = Thanksgiving (US).
    """
    d = date(year, month, 1)
    # Find first occurrence of weekday
    offset = (weekday - d.weekday()) % 7
    first = d + timedelta(days=offset)
    return first + timedelta(weeks=n - 1)


def last_weekday_of_month(year: int, month: int, weekday: int) -> date:
    """
    Return the date of the last occurrence of `weekday` in the given
    month/year. E.g., last Monday of May = Memorial Day (US).
    """
    # Find last day of the month
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    last_day = next_month - timedelta(days=1)
    offset = (last_day.weekday() - weekday) % 7
    return last_day - timedelta(days=offset)


def easter_for_year(year: int) -> date:
    """
    Compute Western Easter Sunday for a given year (Anonymous Gregorian
    algorithm / Meeus / Jones / Butcher). Returns a date object.
    """
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def mothering_sunday_uk(year: int) -> date:
    """UK Mother's Day = 4th Sunday of Lent = 3 weeks before Easter Sunday."""
    return easter_for_year(year) - timedelta(weeks=3)


def good_friday(year: int) -> date:
    return easter_for_year(year) - timedelta(days=2)


def easter_monday(year: int) -> date:
    return easter_for_year(year) + timedelta(days=1)


def victoria_day_canada(year: int) -> date:
    """Canada's Victoria Day = last Monday before May 25."""
    target = date(year, 5, 25)
    # Walk back to find Monday (weekday 0)
    offset = (target.weekday() - 0) % 7
    if offset == 0:
        # If May 25 itself is Monday, then the *previous* Monday
        return target - timedelta(weeks=1)
    return target - timedelta(days=offset)


# ============================================================================
# HOLIDAY DEFINITIONS PER REGION
# ============================================================================

def us_holidays(year: int) -> list[dict]:
    """Return US retail-relevant holidays for the given year."""
    out: list[dict] = []

    def add(d: date, name: str, type_: str, relevance: str, categories: list[str] | None = None):
        out.append({
            "date": d,
            "name": name,
            "type": type_,
            "retail_relevance": relevance,
            "categories": categories or [],
            "region": "us",
        })

    # January
    add(date(year, 1, 1), "New Year's Day", "cultural", "low", ["fitness", "wellness", "supplements"])
    add(nth_weekday_of_month(year, 1, 0, 3), "MLK Day", "federal", "low")

    # February
    add(date(year, 2, 14), "Valentine's Day", "retail", "high",
        ["jewelry", "beauty", "gifts", "food", "drink"])
    add(nth_weekday_of_month(year, 2, 0, 3), "Presidents' Day", "federal-retail", "medium",
        ["home", "mattresses", "appliances"])

    # March
    add(date(year, 3, 8), "International Women's Day", "cultural", "low-brand-fit")
    add(date(year, 3, 17), "St. Patrick's Day", "cultural", "low",
        ["beverages", "party"])

    # April
    add(easter_for_year(year), "Easter", "religious-retail", "medium-high",
        ["kids", "food", "gifts"])
    add(date(year, 4, 22), "Earth Day", "cultural", "low-brand-fit", ["sustainability"])

    # May
    add(nth_weekday_of_month(year, 5, 6, 2), "Mother's Day", "retail", "very-high",
        ["jewelry", "beauty", "flowers", "gifts", "food", "home", "apparel"])
    add(last_weekday_of_month(year, 5, 0), "Memorial Day", "federal-retail", "high",
        ["apparel", "home", "outdoor", "summer-prep"])

    # June
    add(nth_weekday_of_month(year, 6, 6, 3), "Father's Day", "retail", "high",
        ["tools", "tech", "grilling", "men's grooming", "men's apparel"])
    add(date(year, 6, 19), "Juneteenth", "federal-cultural", "low-brand-fit")

    # July
    add(date(year, 7, 4), "Independence Day / July 4th", "federal-retail", "high",
        ["outdoor", "BBQ", "apparel", "Americana"])

    # August (no major federal holidays — BTS only flagged in cultural calendar)

    # September
    add(nth_weekday_of_month(year, 9, 0, 1), "Labor Day", "federal-retail", "high",
        ["apparel", "home", "fall-prep"])

    # October
    add(date(year, 10, 31), "Halloween", "cultural-retail", "high",
        ["costumes", "party", "candy", "kids"])

    # November
    add(date(year, 11, 11), "Singles' Day", "international-retail", "medium")
    thanksgiving = nth_weekday_of_month(year, 11, 3, 4)
    add(thanksgiving, "Thanksgiving", "federal-cultural", "low-direct-retail")
    black_friday = thanksgiving + timedelta(days=1)
    add(black_friday, "Black Friday", "retail", "very-very-high",
        ["all"])
    cyber_monday = thanksgiving + timedelta(days=4)
    add(cyber_monday, "Cyber Monday", "retail", "very-very-high", ["all"])
    giving_tuesday = thanksgiving + timedelta(days=5)
    add(giving_tuesday, "Giving Tuesday", "cause-marketing", "medium-brand-fit")

    # December
    add(date(year, 12, 25), "Christmas Day", "federal-cultural", "low-direct-retail")
    add(date(year, 12, 26), "Boxing Day (growing in US)", "post-holiday-retail", "medium-growing")
    add(date(year, 12, 31), "New Year's Eve", "cultural", "medium")

    return out


def uk_eu_holidays(year: int) -> list[dict]:
    """Return UK + EU retail-relevant holidays for the given year."""
    out: list[dict] = []

    def add(d: date, name: str, type_: str, relevance: str, categories: list[str] | None = None, market: str = "uk"):
        out.append({
            "date": d,
            "name": name,
            "type": type_,
            "retail_relevance": relevance,
            "categories": categories or [],
            "region": f"uk-eu",
            "market_specific": market,
        })

    # January
    add(date(year, 1, 1), "New Year's Day", "cultural", "low", market="all")
    add(date(year, 1, 6), "Twelfth Night / Three Kings Day", "religious-retail", "medium",
        ["gifts", "kids"], market="spain-italy")

    # February
    add(date(year, 2, 14), "Valentine's Day", "retail", "high",
        ["jewelry", "beauty", "gifts"], market="all")

    # March
    mothering = mothering_sunday_uk(year)
    add(mothering, "Mothering Sunday (UK Mother's Day)", "retail", "very-high",
        ["jewelry", "beauty", "flowers", "gifts", "food", "home"], market="uk-ireland")

    # April
    add(easter_for_year(year), "Easter Sunday", "religious-retail", "high",
        ["kids", "gifts", "food"], market="all")
    add(good_friday(year), "Good Friday", "religious-bank-holiday", "high", market="uk-eu")
    add(easter_monday(year), "Easter Monday", "religious-bank-holiday", "high", market="uk-eu")

    # May
    add(nth_weekday_of_month(year, 5, 0, 1), "Early May Bank Holiday", "bank-holiday-retail", "medium",
        market="uk")
    add(date(year, 5, 1), "May Day / Labour Day", "public-holiday", "low",
        market="france-germany-italy-spain")
    add(last_weekday_of_month(year, 5, 0), "Spring Bank Holiday", "bank-holiday-retail", "medium",
        market="uk")
    add(last_weekday_of_month(year, 5, 6), "Mother's Day (France)", "retail", "high",
        ["jewelry", "beauty", "flowers", "gifts"], market="france")
    add(nth_weekday_of_month(year, 5, 6, 2), "Mother's Day (Germany/Italy)", "retail", "high",
        ["jewelry", "beauty", "flowers"], market="germany-italy")
    add(nth_weekday_of_month(year, 5, 6, 1), "Mother's Day (Spain)", "retail", "high",
        ["jewelry", "beauty", "flowers"], market="spain")

    # June
    add(nth_weekday_of_month(year, 6, 6, 3), "Father's Day", "retail", "high",
        ["tools", "tech", "grilling"], market="uk-eu")

    # August
    add(last_weekday_of_month(year, 8, 0), "Summer Bank Holiday", "bank-holiday-retail", "medium",
        market="uk")
    add(date(year, 8, 15), "Ferragosto (Italy)", "public-holiday", "low",
        market="italy")

    # November
    thanksgiving_us = nth_weekday_of_month(year, 11, 3, 4)
    black_friday = thanksgiving_us + timedelta(days=1)
    cyber_monday = thanksgiving_us + timedelta(days=4)
    add(black_friday, "Black Friday", "retail", "high", ["all"], market="uk-eu")
    add(cyber_monday, "Cyber Monday", "retail", "high", ["all"], market="uk-eu")

    # December
    add(date(year, 12, 5), "Sinterklaas / St. Nicholas", "religious-retail", "high",
        ["toys", "gifts", "kids"], market="netherlands-belgium-germany")
    add(date(year, 12, 25), "Christmas Day", "religious", "low-direct-retail", market="all")
    add(date(year, 12, 26), "Boxing Day", "post-holiday-retail", "very-high", ["all"], market="uk")
    add(date(year, 12, 31), "New Year's Eve", "cultural", "medium", market="all")

    return out


def canada_au_nz_holidays(year: int) -> list[dict]:
    """Return Canada + AU + NZ retail-relevant holidays for the given year."""
    out: list[dict] = []

    def add(d: date, name: str, type_: str, relevance: str, categories: list[str] | None = None, market: str = "all"):
        out.append({
            "date": d,
            "name": name,
            "type": type_,
            "retail_relevance": relevance,
            "categories": categories or [],
            "region": "canada-au-nz",
            "market_specific": market,
        })

    # January
    add(date(year, 1, 1), "New Year's Day", "cultural", "low", market="all")
    add(date(year, 1, 26), "Australia Day", "national-retail", "medium",
        ["apparel", "food", "outdoor"], market="au")

    # February
    add(date(year, 2, 6), "Waitangi Day", "national", "low", market="nz")
    add(date(year, 2, 14), "Valentine's Day", "retail", "high",
        ["jewelry", "beauty", "gifts"], market="all")

    # March/April — Easter
    add(easter_for_year(year), "Easter Sunday", "religious-retail", "medium-high",
        ["kids", "gifts", "food"], market="all")
    add(good_friday(year), "Good Friday", "religious-public-holiday", "high", market="all")
    add(easter_monday(year), "Easter Monday", "religious-public-holiday", "high", market="all")
    add(date(year, 4, 25), "ANZAC Day", "remembrance", "PAUSE-PROMOTIONS",
        market="au-nz")

    # May
    add(nth_weekday_of_month(year, 5, 6, 2), "Mother's Day", "retail", "very-high",
        ["jewelry", "beauty", "flowers", "gifts", "home"], market="all")
    add(victoria_day_canada(year), "Victoria Day", "federal-retail", "medium",
        ["home", "outdoor", "summer-prep"], market="canada")

    # June
    add(nth_weekday_of_month(year, 6, 6, 3), "Father's Day (Canada)", "retail", "high",
        ["tools", "tech", "grilling"], market="canada")
    add(nth_weekday_of_month(year, 6, 0, 2), "Queen's Birthday (AU most states)", "public-holiday", "medium",
        market="au")

    # July
    add(date(year, 7, 1), "Canada Day", "national-retail", "high",
        ["outdoor", "Canadiana", "apparel"], market="canada")

    # September
    add(nth_weekday_of_month(year, 9, 0, 1), "Labour Day (Canada)", "federal-retail", "high",
        ["apparel", "school", "home"], market="canada")
    add(nth_weekday_of_month(year, 9, 6, 1), "Father's Day (AU + NZ)", "retail", "high",
        ["tools", "tech"], market="au-nz")

    # October
    add(nth_weekday_of_month(year, 10, 0, 2), "Canadian Thanksgiving", "federal-cultural", "medium",
        ["food", "home"], market="canada")
    add(date(year, 10, 31), "Halloween", "cultural-retail", "high",
        ["costumes", "party", "kids"], market="all")

    # November
    add(date(year, 11, 11), "Remembrance Day", "remembrance", "PAUSE-PROMOTIONS", market="all")
    thanksgiving_us = nth_weekday_of_month(year, 11, 3, 4)
    black_friday = thanksgiving_us + timedelta(days=1)
    cyber_monday = thanksgiving_us + timedelta(days=4)
    add(black_friday, "Black Friday", "retail", "high", ["all"], market="all")
    add(cyber_monday, "Cyber Monday", "retail", "high", ["all"], market="all")

    # December
    add(date(year, 12, 25), "Christmas Day (summer in AU/NZ)", "religious-retail", "very-high",
        ["all"], market="all")
    add(date(year, 12, 26), "Boxing Day", "post-holiday-retail", "very-very-high", ["all"], market="all")
    add(date(year, 12, 31), "New Year's Eve", "cultural", "medium", market="all")

    return out


# ============================================================================
# PUBLIC API
# ============================================================================

REGION_FUNCTIONS = {
    "us": us_holidays,
    "uk-eu": uk_eu_holidays,
    "canada-au-nz": canada_au_nz_holidays,
}


def holidays_for_region(region: str, year: int) -> list[dict]:
    """Get all holidays for a region in a single year."""
    fn = REGION_FUNCTIONS.get(region)
    if fn is None:
        raise ValueError(f"Unknown region '{region}'. Valid: {list(REGION_FUNCTIONS.keys())}")
    return fn(year)


def holidays_for_region_in_range(region: str, start: date, end: date) -> list[dict]:
    """
    Get all holidays for a region within a date range, possibly spanning years.
    Sorted by date ascending.
    """
    years = set()
    cur = start
    while cur <= end:
        years.add(cur.year)
        cur = date(cur.year + 1, 1, 1)
    years.add(end.year)

    all_holidays: list[dict] = []
    for year in sorted(years):
        all_holidays.extend(holidays_for_region(region, year))

    in_range = [h for h in all_holidays if start <= h["date"] <= end]
    in_range.sort(key=lambda h: h["date"])
    return in_range


def holidays_for_all_regions_in_range(start: date, end: date) -> list[dict]:
    """Get holidays across all regions in a date range (deduplicated where dates match)."""
    all_h: list[dict] = []
    for region in REGION_FUNCTIONS.keys():
        all_h.extend(holidays_for_region_in_range(region, start, end))
    # Sort by date, then by region
    all_h.sort(key=lambda h: (h["date"], h["region"]))
    return all_h


def _parse_date(s: str) -> date:
    parts = s.split("-")
    if len(parts) != 3:
        raise ValueError(f"Invalid date format '{s}'; expected YYYY-MM-DD")
    return date(int(parts[0]), int(parts[1]), int(parts[2]))


def _cli():
    parser = argparse.ArgumentParser(description="Retrieve retail-relevant holidays for a region and date range.")
    parser.add_argument("region", choices=list(REGION_FUNCTIONS.keys()) + ["all"], help="Region to query")
    parser.add_argument("start", help="Start date (YYYY-MM-DD)")
    parser.add_argument("end", help="End date (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    start = _parse_date(args.start)
    end = _parse_date(args.end)

    if args.region == "all":
        holidays = holidays_for_all_regions_in_range(start, end)
    else:
        holidays = holidays_for_region_in_range(args.region, start, end)

    if args.json:
        # Convert date objects to ISO strings for JSON serialization
        serializable = [
            {**h, "date": h["date"].isoformat()}
            for h in holidays
        ]
        print(json.dumps(serializable, indent=2))
    else:
        print(f"{len(holidays)} holidays in {args.region} from {args.start} to {args.end}:")
        for h in holidays:
            cats = ", ".join(h.get("categories", []))
            cats_str = f" [{cats}]" if cats else ""
            print(f"  {h['date'].isoformat()}  {h['name']:<45}  {h['retail_relevance']:<25}{cats_str}")


if __name__ == "__main__":
    _cli()
