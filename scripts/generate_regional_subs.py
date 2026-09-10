import re
from pathlib import Path

INPUT_FILE = Path("configs/proxy_configs.txt")
OUTPUT_DIR = Path("configs/regional")

REGIONS = {
    "usa-canada": {"US", "CA"},
    "western-europe": {"DE", "FR", "NL", "BE", "LU", "CH", "AT", "GB", "IE", "ES", "PT", "IT"},
    "scandinavia": {"SE", "NO", "DK", "FI", "IS"},
    "russia-cis": {"RU", "BY", "UA", "MD", "KZ", "KG", "UZ", "TJ", "TM", "AM", "AZ", "GE"},
    "china-east-asia": {"CN", "HK", "MO", "TW", "JP", "KR", "KP", "MN", "SG", "TH", "VN", "MY", "ID", "PH"},
    "middle-east": {"IR", "IQ", "TR", "SY", "LB", "JO", "IL", "PS", "SA", "AE", "QA", "KW", "BH", "OM", "YE"},
    "eastern-europe": {"PL", "CZ", "SK", "HU", "RO", "BG", "RS", "HR", "SI", "BA", "ME", "MK", "AL", "EE", "LV", "LT"},
    "africa": {"DZ", "AO", "EG", "ET", "GH", "KE", "MA", "NG", "TN", "ZA", "TZ", "UG"},  # کوتاه‌شده
}

def get_country_code(fragment: str) -> str:
    """فقط از فرمت ثابت: 'flag id - CC - TAGS - port' استفاده می‌کنه."""
    parts = fragment.split(" - ")
    if len(parts) >= 2:
        code = parts[1].strip()
        if re.fullmatch(r"[A-Z]{2}", code):
            return code
    return "XX"

def get_region(country: str) -> str:
    for region, countries in REGIONS.items():
        if country in countries:
            return region
    return "other"

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = INPUT_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()

    regional = {region: [] for region in REGIONS}
    regional["other"] = []
    seen = set()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("//") or line.startswith("#") or "#" not in line:
            continue  # هدرها و خطوط خالی رد می‌شن

        if line in seen:
            continue
        seen.add(line)

        fragment = line.split("#", 1)[1]  # فقط قسمت بعد از # رو می‌گیره
        country = get_country_code(fragment)
        region = get_region(country)
        regional[region].append(line)

    for region, configs in regional.items():
        out = OUTPUT_DIR / f"{region}.txt"
        content = "\n".join(configs) + ("\n" if configs else "")
        out.write_text(content, encoding="utf-8")
        print(f"{region}: {len(configs)} configs")

if __name__ == "__main__":
    main()
