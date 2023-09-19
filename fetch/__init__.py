"""
Utilities for fetching assets and data for a single document. 
This is a directory module in case I need to split things into files later.

These should be saved in a pattern that matches the original API.
"""
import json
from pathlib import Path
from urllib.parse import urljoin

import httpx
from documentcloud import DocumentCloud, Document

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets"
DOCUMENTS = ASSETS / "documents"

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
    url = urljoin(client.base_uri, f"{client.documents.api_path}/{id}.json")
    params = {"expand": EXPAND}

    output = DOCUMENTS / f"{id}.json"
    resp = httpx.get(url, params=params)

    resp.raise_for_status()

    # save our data
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(resp.content)


def pdf(doc: Document):
    "Download the original PDF to documents/<id>/<slug>.pdf"
    output = DOCUMENTS / str(doc.id) / f"{doc.slug}.pdf"

    # save our data
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(doc.pdf)


def full_text(doc: Document):
    "Download text extracted from a single document to documents/<id>/<slug>.txt"
    output = DOCUMENTS / str(doc.id) / f"{doc.slug}.txt"

    # save our data
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(doc.full_text)


def json_text(doc: Document):
    "Download text JSON for a single document to documents/<id>/<slug>.txt.json"
    output = DOCUMENTS / str(doc.id) / f"{doc.slug}.txt.json"

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(doc.json_text, indent=2))


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
