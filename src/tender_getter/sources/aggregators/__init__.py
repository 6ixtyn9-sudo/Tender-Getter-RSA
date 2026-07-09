"""Third-party aggregator source plug-ins.

Aggregators scrape consolidated tender databases (TenderBulletins.co.za,
ProTenders.co.za) rather than individual government portals. They serve as
high-reliability fallbacks for sources whose own websites are down, block
automated access, or use JS-only rendering that defeats static parsing.
"""
from .tenderbulletins import (
    TenderBulletinsSource,
    fetch_tenderbulletins,
    SLUG_MAP,
)

__all__ = [
    "TenderBulletinsSource",
    "fetch_tenderbulletins",
    "SLUG_MAP",
]
