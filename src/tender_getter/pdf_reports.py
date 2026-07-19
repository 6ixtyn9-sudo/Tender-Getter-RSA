"""Portable PDF rendering for Tender Opportunity Reports."""
from __future__ import annotations
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT
from .schemas import CompanyProfile, TenderOpportunity, MatchResult
from .reporter import _build_report, _safe_filename

def generate_report_pdf(company: CompanyProfile, tender: TenderOpportunity, result: MatchResult, output_dir: Path | None = None) -> Path:
    """Render the same auditable report content as Markdown to a downloadable PDF."""
    directory = Path(output_dir) if output_dir else Path(__file__).resolve().parents[2] / "localdata"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / _safe_filename(company.company_name, tender.tender_id).replace('.md', '.pdf')
    styles = getSampleStyleSheet(); normal = styles['BodyText']; normal.leading = 14; normal.alignment = TA_LEFT
    story=[]
    for raw in _build_report(company, tender, result).splitlines():
        line=raw.strip()
        if not line: story.append(Spacer(1, 3)); continue
        if line.startswith('# '): story.append(Paragraph(f'<b>{line[2:]}</b>', styles['Title']))
        elif line.startswith('## '): story.append(Paragraph(f'<b>{line[3:]}</b>', styles['Heading2']))
        elif line.startswith('### '): story.append(Paragraph(f'<b>{line[4:]}</b>', styles['Heading3']))
        elif line.startswith('|') or line.startswith('---'): continue
        else: story.append(Paragraph(line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'), normal))
    SimpleDocTemplate(str(path), pagesize=A4, rightMargin=16*mm, leftMargin=16*mm, topMargin=16*mm, bottomMargin=16*mm).build(story)
    return path
