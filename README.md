# Standalone Document Viewer

This is a prototype document viewer for DocumentCloud. It should create a version of a DocumentCloud embed that will work without an internet connection.

## Getting started

To run locally, install a [recent version of Python](https://chrisamico.com/blog/2023-01-14/python-setup/) and [Poetry](https://python-poetry.org/).

### Clone and install dependencies

```sh
git clone https://github.com/eyeseast/docviewer-standalone-prototype && cd docviewer-standalone-prototype
poetry install
```

This will create a virtual environment and install the required Python dependencies. You can now run the add-on locally to download assets for documents.

### Fetch assets

First, store your DocumentCloud login credentials in your environment. The easiest way is to create a `.env` file in the root of this directory, and set your username and password, like this:

```sh
# .env

export DC_USERNAME="you@example.com"
export DC_PASSWORD="password12345"
```

Run `source .env` to load the `DC_USERNAME` and `DC_PASSWORD` into your environment.

Now, run the script, passing in the ID of a document you want to export:

```sh
poetry run ./main.py --documents 23781130
```

This uses `poetry` to run the `main.py` script inside a virtual environment and will fetch assets for [a single document](https://www.documentcloud.org/documents/23781130-boston_ghg_inventory_2005-2015). Everything will be downloaded into a folder called `assets`, as well as an archive called `assets.zip`.
