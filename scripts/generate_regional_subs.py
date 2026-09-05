import re
from pathlib import Path
from urllib.parse import unquote

INPUT_FILE = Path("configs/proxy_configs.txt")
OUTPUT_DIR = Path("configs/regional")

REGIONS = {
    "western-europe": {
        "DE", "FR", "NL", "BE", "LU", "CH", "AT",
        "GB", "IE", "ES", "PT", "IT"
    },
    "scandinavia": {
        "SE", "NO", "DK", "FI", "IS"
    },
    "russia-cis": {
        "RU", "BY", "UA", "MD", "KZ", "KG", "UZ",
        "TJ", "TM", "AM", "AZ", "GE"
    },
    "east-asia": {
        "CN", "HK", "MO", "TW", "JP", "KR", "KP", "MN"
    },
    "middle-east": {
        "IR", "IQ", "TR", "SY", "LB", "JO", "IL", "PS",
        "SA", "AE", "QA", "KW", "BH", "OM", "YE"
    },
    "eastern-europe": {
        "PL", "CZ", "SK", "HU", "RO", "BG", "RS", "HR",
        "SI", "BA", "ME", "MK", "AL", "EE", "LV", "LT"
    },
    "africa": {
        "DZ", "AO", "BJ", "BW", "BF", "BI", "CV", "CM",
        "CF", "TD", "KM", "CG", "CD", "CI", "DJ", "EG",
        "GQ", "ER", "SZ", "ET", "GA", "GM", "GH", "GN",
        "GW", "KE", "LS", "LR", "LY", "MG", "MW", "ML",
        "MR", "MU", "MA", "MZ", "NA", "NE", "NG", "RW",
        "ST", "SN", "SC", "SL", "SO", "ZA", "SS", "SD",
        "TZ", "TG", "TN", "UG", "ZM", "ZW"
    },
}


def get_country_code(line):
    """
    Extract country code from the enriched config remark.
    Examples:
      #🇩🇪 12 - DE - ...
      #12 - DE - ...
    """
    decoded = unquote(line)

    matches = re.findall(
        r"(?:^|[\s#\-])([A-Z]{2})(?:[\s\-]|$)",
        decoded
    )

    for code in reversed(matches):
        if any(code in countries for countries in REGIONS.values()):
            return code

    return "XX"


def get_region(country):
    for region, countries in REGIONS.items():
        if country in countries:
            return region
    return "other"


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    lines = INPUT_FILE.read_text(
        encoding="utf-8",
        errors="ignore"
    ).splitlines()

    regional = {region: [] for region in REGIONS}
    regional["other"] = []

    seen_global = set()

    for line in lines:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        # Global duplicate removal
        normalized = line.strip()

        if normalized in seen_global:
            continue

        seen_global.add(normalized)

        country = get_country_code(line)
        region = get_region(country)

        regional[region].append(line)

    for region, configs in regional.items():
        output = OUTPUT_DIR / f"{region}.txt"

        content = "\n".join(configs)

        if content:
            content += "\n"

        output.write_text(
            content,
            encoding="utf-8"
        )

        print(f"{region}: {len(configs)} configs -> {output}")


if __name__ == "__main__":
    main()
