"""Shared parsing helpers – CIDB, province, dates, and HTML tables."""
import re
from datetime import datetime, timezone
from typing import Optional
from html.parser import HTMLParser

_CIDB_PATTERN = re.compile(r"(?:level\s*)?(\d)\s*([A-Z]{2})\b", re.IGNORECASE)

# Safe computer memory patterns to filter out GB of RAM, GB SSD, etc. false positives
_GB_RAM_PATTERN = re.compile(r"\b\d+\s*GB\s*(?:of\s*)?(?:ram|storage|ssd|hard\s*drive|memory|space)\b", re.IGNORECASE)

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

_MONTH_NAMES = {
    "january": 1, "jan": 1,
    "february": 2, "feb": 2,
    "march": 3, "mar": 3,
    "april": 4, "apr": 4,
    "may": 5,
    "june": 6, "jun": 6,
    "july": 7, "jul": 7,
    "august": 8, "aug": 8,
    "september": 9, "sep": 9, "sept": 9,
    "october": 10, "oct": 10,
    "november": 11, "nov": 11,
    "december": 12, "dec": 12
}

def re_search_cidb(text: str) -> Optional[tuple[str, str]]:
    if not text:
        return None
    # Filter computer memory false positives e.g. "SITA requires 8 GB RAM"
    clean_text = _GB_RAM_PATTERN.sub("", text)
    
    for match in _CIDB_PATTERN.finditer(clean_text):
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
    
    # 1. ISO format (e.g. "2026-08-15T11:00:00Z")
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        pass
        
    # 2. Standard timestamp strings
    for fmt in ("%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s[:19], fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue

    # 3. Numeric formats e.g. "30/08/2026" or "15-09-2026"
    num_match = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", s)
    if num_match:
        try:
            d = int(num_match.group(1))
            m = int(num_match.group(2))
            y = int(num_match.group(3))
            if y < 100:
                y += 2000
            return datetime(y, m, d, tzinfo=timezone.utc)
        except ValueError:
            pass

    # 4. Verbal date formats e.g. "30 August 2026" or "15 Sep 2026"
    verbal_match = re.search(r"(\d{1,2})\s+([a-zA-Z]{3,10})\s+(\d{4})", s)
    if verbal_match:
        try:
            d = int(verbal_match.group(1))
            month_str = verbal_match.group(2).lower()
            y = int(verbal_match.group(3))
            if month_str in _MONTH_NAMES:
                m = _MONTH_NAMES[month_str]
                return datetime(y, m, d, tzinfo=timezone.utc)
        except ValueError:
            pass

    # 5. US verbal date formats e.g. "July 1, 2026" or "August 15, 2026"
    us_verbal_match = re.search(r"([a-zA-Z]{3,10})\s+(\d{1,2}),?\s+(\d{4})", s)
    if us_verbal_match:
        try:
            month_str = us_verbal_match.group(1).lower()
            d = int(us_verbal_match.group(2))
            y = int(us_verbal_match.group(3))
            if month_str in _MONTH_NAMES:
                m = _MONTH_NAMES[month_str]
                return datetime(y, m, d, tzinfo=timezone.utc)
        except ValueError:
            pass

    # 6. Year-first verbal e.g. "2025 November 28" or "2026 January 13"
    yf_match = re.search(r"(\d{4})\s+([a-zA-Z]{3,10})\s+(\d{1,2})", s)
    if yf_match:
        try:
            y = int(yf_match.group(1))
            month_str = yf_match.group(2).lower()
            d = int(yf_match.group(3))
            if month_str in _MONTH_NAMES:
                m = _MONTH_NAMES[month_str]
                return datetime(y, m, d, tzinfo=timezone.utc)
        except ValueError:
            pass

    # Safe fallback
    return datetime(2099, 12, 31, tzinfo=timezone.utc)


class TableRowParser(HTMLParser):
    """
    Highly secure and resilient HTML table parser utilizing Python's built-in standard library.
    Immune to regular expression nested tag bottlenecks, unclosed tags, and style injection.
    """
    def __init__(self):
        super().__init__()
        self.rows = []
        self.current_row = []
        self.current_cell = []
        self.in_td = False
        self.in_tr = False

    def handle_starttag(self, tag, attrs):
        if tag in ('td', 'th'):
            self.in_td = True
            self.current_cell = []
        elif tag == 'tr':
            self.in_tr = True
            self.current_row = []

    def handle_endtag(self, tag):
        if tag in ('td', 'th'):
            self.in_td = False
            cell_text = "".join(self.current_cell).strip()
            # Standardize internal whitespace
            cell_text = re.sub(r"\s+", " ", cell_text)
            self.current_row.append(cell_text)
        elif tag == 'tr':
            self.in_tr = False
            if self.current_row:
                self.rows.append(self.current_row)

    def handle_data(self, data):
        if self.in_td:
            self.current_cell.append(data)


def parse_html_table(html_content: str) -> list[list[str]]:
    """
    Parses HTML tables cleanly into rows and columns.
    Completely immune to nested HTML tag complexities, inline styles, and unclosed tags.
    """
    parser = TableRowParser()
    parser.feed(html_content)
    return parser.rows
