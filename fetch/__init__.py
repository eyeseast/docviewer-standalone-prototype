"""
Utilities for fetching assets and data for a single document. 
This is a directory module in case I need to split things into files later.

These should be saved in a pattern that matches the original API.
"""
from pathlib import Path
from documentcloud import DocumentCloud, Document

ROOT = Path(__file__).parent.parent
DOCUMENTS = ROOT / "documents"

EXPAND = [
    "user",
    "organization",
    "notes",
    "sections",
    "notes.organization",
    "notes.user",
]


def document(client: DocumentCloud, id: int):
    "Download JSON data for a single document"


def pdf(doc: Document):
    "Download the original PDF to documents/<id>/<slug>.pdf"


def full_text(doc: Document):
    "Download text extracted from a single document to documents/<id>/<slug>.txt"


def text_json(doc: Document):
    "Download text JSON for a single document to documents/<id>/<slug>.txt.json"


def page_text(doc: Document):
    """
    Download page text for all pages in a document.
    Save results to documents/<id>/pages/<slug>-p<page number>.txt
    """


def page_positions(doc: Document):
    """
    Download page positions for all pages in a document.
    Save results to documents/<id>/pages/<slug>-p<page number>.position.json
    """


def images(doc: Document):
    """
    Download all imags of document pages.
    Save results to documents/<id>/pages/<slug>-p<page number>-<size>.gif
    """
