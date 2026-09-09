import os
from pathlib import Path

import pymupdf  # PyMuPDF
from docx import Document


# =============================================================
# DOCUMENT LOCATIONS
# =============================================================

SEARCH_DIRECTORIES = [
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path.home() / "Downloads",
]


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


# =============================================================
# FIND DOCUMENT
# =============================================================

def find_document(query):
    """
    Find documents in common user folders.

    Searches Desktop, Documents, and Downloads.
    """

    query = query.lower().strip()

    if not query:
        return "Please provide a document name or search term."

    results = []

    for directory in SEARCH_DIRECTORIES:

        if not directory.exists():
            continue

        try:
            for root, dirs, files in os.walk(directory):

                # Skip unnecessary/system directories
                dirs[:] = [
                    d for d in dirs
                    if d not in {
                        ".git",
                        ".venv",
                        "__pycache__",
                        "node_modules"
                    }
                ]

                for filename in files:

                    path = Path(root) / filename

                    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                        continue

                    if query in filename.lower():
                        results.append(path)

                        if len(results) >= 10:
                            break

                if len(results) >= 10:
                    break

        except (PermissionError, OSError):
            continue

        if len(results) >= 10:
            break

    if not results:
        return f"No documents matching '{query}' were found."

    output = [f"Found {len(results)} document(s):"]

    for path in results:
        output.append(str(path))

    return "\n".join(output)


# =============================================================
# READ PDF
# =============================================================

def read_pdf(path):
    """
    Extract text from a PDF document.
    """

    path = Path(path)

    if not path.exists():
        return "The specified document does not exist."

    if path.suffix.lower() != ".pdf":
        return "The specified file is not a PDF."

    try:
        document = pymupdf.open(path)

        pages = []

        for page_number, page in enumerate(document, start=1):

            text = page.get_text().strip()

            if text:
                pages.append(
                    f"\n--- Page {page_number} ---\n{text}"
                )

        document.close()

        if not pages:
            return (
                "The PDF does not contain extractable text. "
                "It may be a scanned document."
            )

        return "\n".join(pages)

    except Exception as e:
        return f"Unable to read the PDF: {e}"


# =============================================================
# READ DOCX
# =============================================================

def read_docx(path):
    """
    Extract text from a Word document.
    """

    path = Path(path)

    if not path.exists():
        return "The specified document does not exist."

    if path.suffix.lower() != ".docx":
        return "The specified file is not a DOCX document."

    try:
        document = Document(path)

        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        if not paragraphs:
            return "The Word document does not contain readable text."

        return "\n".join(paragraphs)

    except Exception as e:
        return f"Unable to read the Word document: {e}"


# =============================================================
# READ TEXT FILE
# =============================================================

def read_txt(path):
    """
    Read a plain text document.
    """

    path = Path(path)

    if not path.exists():
        return "The specified document does not exist."

    if path.suffix.lower() != ".txt":
        return "The specified file is not a TXT document."

    try:
        return path.read_text(
            encoding="utf-8",
            errors="replace"
        )

    except Exception as e:
        return f"Unable to read the text file: {e}"


# =============================================================
# READ DOCUMENT
# =============================================================

def read_document(path):
    """
    Read a supported document based on its file type.
    """

    path = Path(path)

    if not path.exists():
        return "The specified document does not exist."

    extension = path.suffix.lower()

    if extension == ".pdf":
        return read_pdf(path)

    if extension == ".docx":
        return read_docx(path)

    if extension == ".txt":
        return read_txt(path)

    return (
        f"Unsupported document type: {extension}. "
        "Supported types are PDF, DOCX, and TXT."
    )