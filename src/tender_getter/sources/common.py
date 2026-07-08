"""Shared parsing helpers – CIDB, province, dates."""
import re
from datetime import datetime, timezone
from typing import Optional

_CIDB_PATTERN = re.compile(r"(?:level\s*)?(\d)\s*([A-Z]{2})\b", re.IGNORECASE)

_PROVINCE_MAP: dict[str, str] = {
 "gauteng": "Gauteng", "gp": "Gauteng", "gt": "Gauteng",
 "western cape": "Western Cape", "wc": "Western Cape",
 "eastern cape": "Eastern Cape", "ec": "Eastern Cape",
 "kwazulu-natal": "KwaZulu-Natal", "kwazulu natal": "KwaZulu-Natal", "kzn": "KwaZulu-Natal",
 "limpopo": "Limpopo", "lp": "Limpopo",
 "mpumalanga": "Mpumalanga", "mp": "Mpumalanga",
 "north west": "North West", "nw": "North West",
 "northern cape": "Northern Cape", "nc": "Northern Cape",
 "free state": "Free State", "fs": "Free State",
}

_VALID_CIDB_CLASSES = {
 "CE", "GB", "EE", "ME", "SB", "PE", "PS", "EP", "SF", "SI", "SO", "SP", "SW",
}

def re_search_cidb(text: str) -> Optional[tuple[str, str]]:
    for match in _CIDB_PATTERN.finditer(text):
        level_str = match.group(1)
        class_code = match.group(2).upper()
        if class_code in _VALID_CIDB_CLASSES and 1 <= int(level_str) <= 9:
            return (level_str, class_code)
    return None

def province_from_text(text: str) -> Optional[str]:
    if not text:
        return None
    text_lower = text.lower()
    for key, province in _PROVINCE_MAP.items():
        if re.search(r"\b" + re.escape(key) + r"\b", text_lower):
            return province
    return None

def parse_closing_date(s: Optional[str]) -> datetime:
    if not s:
        return datetime(2099, 12, 31, tzinfo=timezone.utc)
    s = s.strip()
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        pass
    for fmt in ("%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s[:19], fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return datetime(2099, 12, 31, tzinfo=timezone.utc)
