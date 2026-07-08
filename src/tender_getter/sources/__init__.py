"""Tender source plug-ins – Racket-Factory style."""
from typing import Protocol, List, runtime_checkable, Dict, Any
from pathlib import Path
import logging

from ..schemas import TenderOpportunity

logger = logging.getLogger(__name__)

@runtime_checkable
class TenderSource(Protocol):
    source_id: str
    def fetch(self, limit: int | None = None) -> List[TenderOpportunity]: ...

# Re-export the built-in parsers / syncers
# National
from .national.etenders_ocds import sync_live_tenders, parse_ocds_release_to_tender
from .national.etenders_csv import sync_csv_tenders, parse_csv_row_to_tender
from .national.cidb import CIDBSource

# SOEs
from .soes.sanral import SANRALSource
from .soes.eskom import EskomSource
from .soes.transnet import TransnetSource
from .soes.prasa import PRASASource
from .soes.landbank import LandbankSource
from .soes.sabc import SABCSource
from .soes.acsa import ACSASource
from .soes.denel import DenelSource
from .soes.sentech import SentechSource
from .soes.safcol import SAFCOLSource
from .soes.necsa import NECSASource
from .soes.petrosa import PetroSASource
from .soes.infraco import BroadbandInfracoSource
from .soes.atns import ATNSSource
from .soes.alexkor import AlexkorSource

# Provincial
from .provincial.gauteng import GautengSource
from .provincial.westerncape import WesternCapeSource
from .provincial.kzn import KZNSource
from .provincial.easterncape import EasternCapeSource
from .provincial.freestate import FreeStateSource
from .provincial.limpopo import LimpopoSource
from .provincial.mpumalanga import MpumalangaSource
from .provincial.northwest import NorthWestSource
from .provincial.northerncape import NorthernCapeSource


# Provincial Infrastructure Departments
from .provincial_depts.gdid import GDIDSource
from .provincial_depts.gdrt import GDRTSource
from .provincial_depts.gde import GDESource
from .provincial_depts.gdh import GDHSource
from .provincial_depts.wcdi import WCDISource
from .provincial_depts.wc_health import WCHealthSource
from .provincial_depts.kzn_dot import KZNDoTSource
from .provincial_depts.kzn_human_settlements import KZNHumanSettlementsSource
from .provincial_depts.ec_public_works import ECPublicWorksSource
from .provincial_depts.ec_education import ECEducationSource
from .provincial_depts.fs_police_roads import FSPoliceRoadsSource
from .provincial_depts.limpopo_pwri import LimpopoPWRISource
from .provincial_depts.mpumalanga_education import MpumalangaEducationSource
from .provincial_depts.nw_public_works import NWPublicWorksSource
from .provincial_depts.nc_roads import NCRoadsSource

# National Government Departments
from .national_depts.saps import SAPSSource
from .national_depts.doel import DoELSource
from .national_depts.dpwi import DPWISource
from .national_depts.dws import DWSSource
from .national_depts.dod import DoDSource
from .national_depts.doh import DoHSource
from .national_depts.dbe import DBESource
from .national_depts.dhet import DHETSource
from .national_depts.dha import DHASource
from .national_depts.dmre import DMRESource
from .national_depts.dalrrd import DALRRDSource
from .national_depts.dffe import DFFESource
from .national_depts.dot import DoTSource
from .national_depts.national_treasury import NationalTreasurySource
from .national_depts.dcs import DCSSource
from .national_depts.tourism import TourismSource
from .national_depts.dsac import DSACSource
from .national_depts.dsi import DSISource
from .national_depts.dcdt import DCDTSource
from .national_depts.dsbd import DSBDSource
from .national_depts.dhs import DHSSource
from .national_depts.cogta import COGTASource
from .national_depts.dpsa import DPSASource
from .national_depts.dtic import DTICSource
from .national_depts.dpme import DPMESource
from .national_depts.presidency import PresidencySource

# Research
from .research.sita import SITASource

# DFI / Regulators
from .dfi.dbsa import DBSASource
from .dfi.idc import IDCSource
from .dfi.sars import SARSSource
from .dfi.samsa import SAMSASource
from .dfi.sanparks import SANParksSource
from .dfi.seda import SEDASource
from .dfi.sefa import SefaSource
from .dfi.raf import RAFSource
from .dfi.compensation_fund import CompensationFundSource
from .dfi.uif import UIFSource

# Metros
from .metros.capetown import CapeTownSource
from .metros.johannesburg import JohannesburgSource
from .metros.ethekwini import EthekwiniSource
from .metros.tshwane import TshwaneSource
from .metros.ekurhuleni import EkurhuleniSource
from .metros.nelson_mandela_bay import NelsonMandelaBaySource
from .metros.buffalo_city import BuffaloCitySource
from .metros.mangaung import MangaungSource

# Water Boards
from .water.rand_water import RandWaterSource
from .water.umgeni_water import UmgeniWaterSource
from .water.mhlathuze_water import MhlathuzeWaterSource
from .water.overberg_water import OverbergWaterSource
from .water.amatola_water import AmatolaWaterSource
from .water.lepelle_water import LepelleWaterSource
from .water.magalies_water import MagaliesWaterSource
from .water.bloem_water import BloemWaterSource
from .water.sedibeng_water import SedibengWaterSource
from .water.tcta import TCTASource

# District Municipalities
from .districts.west_rand import WestRandSource
from .districts.sedibeng_dm import SedibengDMSource
from .districts.cape_winelands import CapeWinelandsSource
from .districts.garden_route import GardenRouteSource
from .districts.king_cetshwayo import KingCetshwayoSource
from .districts.ilembe import ILembeSource
from .districts.or_tambo import ORTamboSource
from .districts.capricorn import CapricornSource
from .districts.ehlanzeni import EhlanzeniSource

from .common import re_search_cidb, province_from_text

def load_sources() -> List[Dict[str, Any]]:
    """Load src/tender_getter/sources.yaml – returns [] if PyYAML missing."""
    try:
        import yaml  # type: ignore
    except ImportError:
        logger.warning("PyYAML not installed – load_sources() returning empty list")
        return []
    sources_path = Path(__file__).parent.parent / "sources.yaml"
    if not sources_path.exists():
        return []
    with sources_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("sources", []) if isinstance(data, dict) else []

__all__ = [
    "TenderSource",
    "sync_live_tenders", "parse_ocds_release_to_tender",
    "sync_csv_tenders", "parse_csv_row_to_tender",
    "SANRALSource",
    "EskomSource",
    "TransnetSource",
    "PRASASource",
    "LandbankSource",
    "SABCSource",
    "ACSASource",
    "DenelSource",
    "SentechSource",
    "SAFCOLSource",
    "NECSASource",
    "PetroSASource",
    "BroadbandInfracoSource",
    "ATNSSource",
    "AlexkorSource",
    "GautengSource",
    "CIDBSource",
    "WesternCapeSource",
    "SITASource",
    "CSIRSource",
    "NHLSSource",
    "SANSASource",
    "GeoscienceSource",
    "MintekSource",
    "HSRCSource",
    "WRCSource",
    "SABSSource",
    "CapeTownSource",
    "KZNSource",
    "JohannesburgSource",
    "EthekwiniSource",
    "TshwaneSource",
    "EkurhuleniSource",
    "NelsonMandelaBaySource",
    "BuffaloCitySource",
    "MangaungSource",
    "EasternCapeSource",
    "FreeStateSource",
    "LimpopoSource",
    "MpumalangaSource",
    "NorthWestSource",
        "NorthernCapeSource",
    "GDIDSource",
    "GDRTSource",
    "GDESource",
    "GDHSource",
    "WCDISource",
    "WCHealthSource",
    "KZNDoTSource",
    "KZNHumanSettlementsSource",
    "ECPublicWorksSource",
    "ECEducationSource",
    "FSPoliceRoadsSource",
    "LimpopoPWRISource",
    "MpumalangaEducationSource",
    "NWPublicWorksSource",
    "NCRoadsSource",
    "SAPSSource",
    "DoELSource",
    "DPWISource",
    "DWSSource",
    "DoDSource",
    "DoHSource",
    "DBESource",
    "DHETSource",
    "DHASource",
    "DMRESource",
    "DALRRDSource",
    "DFFESource",
    "DoTSource",
    "NationalTreasurySource",
    "DCSSource",
    "TourismSource",
    "DSACSource",
    "DSISource",
    "DCDTSource",
    "DSBDSource",
    "DHSSource",
    "COGTASource",
    "DPSASource",
    "DTICSource",
    "DPMESource",
    "PresidencySource",
    "DBSASource",
    "DBSASource",
    "IDCSource",
    "SARSSource",
    "SAMSASource",
    "SANParksSource",
    "SEDASource",
    "SefaSource",
    "RAFSource",
    "CompensationFundSource",
    "UIFSource",
    "RandWaterSource",
    "UmgeniWaterSource",
    "MhlathuzeWaterSource",
    "OverbergWaterSource",
    "AmatolaWaterSource",
    "LepelleWaterSource",
    "MagaliesWaterSource",
    "BloemWaterSource",
    "SedibengWaterSource",
    "TCTASource",
    "WestRandSource",
    "SedibengDMSource",
    "CapeWinelandsSource",
    "GardenRouteSource",
    "KingCetshwayoSource",
    "ILembeSource",
    "ORTamboSource",
    "CapricornSource",
    "EhlanzeniSource",
    "re_search_cidb", "province_from_text",
    "load_sources",
]
