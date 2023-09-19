#!/usr/bin/env python
"""
Fetch all assets required to embed a DocumentCloud viewer that can work offline.
"""
import shutil
from documentcloud.addon import AddOn

import fetch


class ExportViewer(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""

        for document in self.get_documents():
            # get_documents will iterate through all documents efficiently,
            # either selected or by query, dependeing on which is passed in
            self.set_message(f"Fetching assets for document: {document.title}")

            # fetch all the things, maybe someday this is async
            fetch.document(self.client, document.id)
            fetch.pdf(document)
            fetch.full_text(document)
            fetch.json_text(document)
            fetch.page_text(document)
            fetch.page_positions(document)
            fetch.images(document)

        self.set_message("Uploading archive")
        archive = shutil.make_archive("assets", "zip", base_dir="assets")

        with open(archive) as f:
            self.upload_file(f)


if __name__ == "__main__":
    ExportViewer().main()
