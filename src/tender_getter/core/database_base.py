"""
database_base.py - Abstract base class for Tender Getter RSA database drivers.

All concrete database implementations (SQLite, PostgreSQL/Supabase, etc.)
must inherit from TenderDatabaseBase and implement every abstract method.

This contract prevents method-level drift between drivers and allows
call-sites to type-hint against TenderDatabaseBase without caring which
backend is active at runtime.
"""

from abc import ABC, abstractmethod
from typing import Optional

from .schemas import CompanyProfile, TenderOpportunity, MatchResult

class TenderDatabaseBase(ABC):
    """
    Abstract interface for Tender Getter RSA persistence drivers.

    Usage (concrete subclass):
    class MyDriver(TenderDatabaseBase):
        def connect(self): ...
        def close(self): ...
        def upsert_company(self, company): ...
        def upsert_tender(self, tender): ...
        def save_match(self, company, result): ...
        def list_open_tenders(self, limit, province): ...
    """

    # -- Connection lifecycle ------------------------------------------------

    @abstractmethod
    def connect(self) -> "TenderDatabaseBase":
        """
        Open the database connection and perform any setup (table creation,
        schema migration checks, etc.).

        Must return `self` so that callers can chain:
        db = MyDriver().connect()
        """

    @abstractmethod
    def close(self) -> None:
        """Release the database connection and free resources."""

    # -- Context manager support ---------------------------------------------

    def __enter__(self) -> "TenderDatabaseBase":
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    # -- Company profiles ----------------------------------------------------

    @abstractmethod
    def upsert_company(self, company: CompanyProfile) -> None:
        """
        Insert or update a company profile and its associated CIDB gradings.

        Implementations must handle the CIDB gradings child-table atomically
        with the parent company_profiles row (delete-then-reinsert or upsert).
        """

    # -- Tenders -------------------------------------------------------------

    @abstractmethod
    def upsert_tender(self, tender: TenderOpportunity) -> None:
        """
        Insert or update a tender opportunity.

        Implementations must store closing_date in a timezone-aware format
        (ISO 8601 string for SQLite, TIMESTAMPTZ for PostgreSQL).
        """

    @abstractmethod
    def list_open_tenders(self, limit: int = 50, province: Optional[str] = None) -> list[TenderOpportunity]:
        """
        Return open tenders, soonest closing first.

        Args:
            limit: Maximum number of tenders to return
            province: If provided, filter to tenders matching this province,
                      or National / NULL location_target (open to all)

        Returns:
            List of TenderOpportunity, ordered by closing_date ASC
        """

    # -- Match results -------------------------------------------------------

    @abstractmethod
    def save_match(self, company: CompanyProfile, result: MatchResult) -> None:
        """
        Persist a MatchResult to the matches table.

        The combination (company_reg_number, tender_id) must be treated as a
        unique key — repeated saves must update, not duplicate.
        """
