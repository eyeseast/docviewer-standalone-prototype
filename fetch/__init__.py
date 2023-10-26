"""
Utilities for fetching assets and data for a single document. 
This is a directory module in case I need to split things into files later.

These should be saved in a pattern that matches the original API.
"""
import json
from itertools import chain
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

ASSET_URL = "http://localhost:5173/"


def all(client: DocumentCloud, document: Document):
    "Run all the functions below, in order"

    document_data(client, document.id)
    pdf(document)
    full_text(document)
    json_text(document)
    page_text(document)
    page_positions(document)
    images(document)


def document_list(client: DocumentCloud, ids: list):
    "Download JSON to list documents"
    path = f"{client.documents.api_path}.json"
    params = {"id__in": ",".join(map(str, ids))}
    output = ASSETS / "api" / path

    resp = client.get(path, params=params)
    resp.raise_for_status()

    docs = resp.json()
    for doc in docs["results"]:
        doc["asset_url"] = ASSET_URL

    # save our data
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w") as f:
        json.dump(docs, f, indent=2)


def document_data(client: DocumentCloud, id: int):
    "Download JSON data for a single document"
    print("Downloading document data")
    path = f"{client.documents.api_path}/{id}.json"
    params = {"expand": EXPAND}

    output = ASSETS / "api" / path

    resp = client.get(path, params=params)
    resp.raise_for_status()

    # fix asset URL for local hosting
    data = resp.json()
    data["asset_url"] = ASSET_URL

    # save our data
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w") as f:
        json.dump(data, f, indent=2)


def pdf(doc: Document):
    "Download the original PDF to documents/<id>/<slug>.pdf"
    print("Downloading PDF")
    output = DOCUMENTS / str(doc.id) / f"{doc.slug}.pdf"

    # save our data
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(doc.pdf)


def full_text(doc: Document):
    "Download text extracted from a single document to documents/<id>/<slug>.txt"
    print("Downloading full text")
    output = DOCUMENTS / str(doc.id) / f"{doc.slug}.txt"

    # save our data
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(doc.full_text)


def json_text(doc: Document):
    "Download text JSON for a single document to documents/<id>/<slug>.txt.json"
    print("Downloading JSON text.")
    output = DOCUMENTS / str(doc.id) / f"{doc.slug}.txt.json"

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(doc.json_text, indent=2))


def page_text(doc: Document):
    """
    Download page text for all pages in a document.
    Save results to documents/<id>/pages/<slug>-p<page number>.txt
    """
    print("Downloading page text.")
    output_dir = DOCUMENTS / str(doc.id) / "pages"
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in range(1, doc.pages + 1):
        output = output_dir / f"{doc.slug}-p{i}.txt"
        text = doc.get_page_text(i)
        output.write_text(text)


def page_positions(doc: Document):
    """
    Download page positions for all pages in a document.
    Save results to documents/<id>/pages/<slug>-p<page number>.position.json
    """
    print("Downloading page positions.")
    output_dir = DOCUMENTS / str(doc.id) / "pages"
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in range(1, doc.pages + 1):
        output = output_dir / f"{doc.slug}-p{i}.position.json"
        data = doc.get_page_position_json(i)
        output.write_text(json.dumps(data, indent=2))


def images(doc: Document):
    """
    Download all images of document pages.
    Save results to documents/<id>/pages/<slug>-p<page number>-<size>.gif
    """
    print("Downloading page images.")
    output_dir = DOCUMENTS / str(doc.id) / "pages"
    output_dir.mkdir(parents=True, exist_ok=True)

    thumbnail = doc.get_thumbnail_image_url_list()
    small = doc.get_small_image_url_list()
    normal = doc.get_normal_image_url_list()
    large = doc.get_large_image_url_list()

    # download all the images, one by one, optimize later
    with httpx.Client() as http:
        for url in chain(thumbnail, small, normal, large):
            resp = http.get(url)
            resp.raise_for_status()

            name = Path(url).name
            output = output_dir / name
            output.write_bytes(resp.content)
