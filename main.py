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

        fetch.document_list(self.client, self.documents)

        for document in self.get_documents():
            # get_documents will iterate through all documents efficiently,
            # either selected or by query, dependeing on which is passed in
            self.set_message(f"Fetching assets for document: {document.title}")
            fetch.all(self.client, document)

        # .env
        shutil.copyfile("assets/env.sample", "assets/.env")

        name = self.data.get("name", "assets")
        self.set_message(f"Uploading archive: {name}")
        archive = shutil.make_archive(name, "zip", base_dir="assets")

        with open(archive) as f:
            self.upload_file(f)


if __name__ == "__main__":
    ExportViewer().main()
