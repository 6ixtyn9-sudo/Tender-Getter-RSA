"""Deprecated compatibility facade.

Canonical implementation: :mod:`tender_getter.cidb_directory`.  This module deliberately
re-exports it so legacy imports cannot diverge from the running implementation.
"""
from ..cidb_directory import *  # noqa: F401,F403
