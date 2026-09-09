import shutil
from pathlib import Path


# =============================================================
# FILE CATEGORIES
# =============================================================

FILE_CATEGORIES = {
    "Documents": {
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        ".rtf",
        ".odt",
    },

    "Images": {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".svg",
        ".tiff",
    },

    "Videos": {
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".wmv",
        ".webm",
    },

    "Audio": {
        ".mp3",
        ".wav",
        ".flac",
        ".aac",
        ".m4a",
        ".ogg",
    },

    "Archives": {
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
    },
}


# =============================================================
# GET CATEGORY
# =============================================================

def get_file_category(path):
    """
    Determine the category of a file based on its extension.
    """

    extension = path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():

        if extension in extensions:
            return category

    return "Others"


# =============================================================
# ORGANIZE FOLDER
# =============================================================

def organize_folder(folder, confirmed=False):
    """
    Preview or perform file organization.

    By default, only shows the proposed changes.
    Files are moved only when confirmed=True.
    """

    folder = Path(folder).expanduser()

    if not folder.exists():
        return f"The folder does not exist: {folder}"

    if not folder.is_dir():
        return f"The specified path is not a folder: {folder}"

    # ---------------------------------------------------------
    # Find files directly inside the folder
    # ---------------------------------------------------------

    files = [
        path
        for path in folder.iterdir()
        if path.is_file()
    ]

    if not files:
        return f"There are no files to organize in {folder}."

    # ---------------------------------------------------------
    # Build organization plan
    # ---------------------------------------------------------

    plan = {}

    for file_path in files:

        category = get_file_category(file_path)

        if category not in plan:
            plan[category] = []

        plan[category].append(file_path)

    # ---------------------------------------------------------
    # PREVIEW MODE
    # ---------------------------------------------------------

    if not confirmed:

        output = [
            f"I found {len(files)} file(s) in {folder}.",
            "",
            "Proposed organization:"
        ]

        for category, category_files in plan.items():

            output.append(
                f"\n{category}/ ({len(category_files)} file(s))"
            )

            for file_path in category_files:
                output.append(
                    f"  {file_path.name}"
                )

        output.append("")
        output.append(
            "No files have been moved. "
            "Ask me to proceed if you want me to apply this organization."
        )

        return "\n".join(output)

    # ---------------------------------------------------------
    # EXECUTION MODE
    # ---------------------------------------------------------

    moved = []
    failed = []

    for category, category_files in plan.items():

        destination = folder / category

        try:
            destination.mkdir(exist_ok=True)

        except OSError as e:

            failed.append(
                f"Could not create {destination}: {e}"
            )

            continue

        for file_path in category_files:

            destination_path = destination / file_path.name

            # -------------------------------------------------
            # Avoid overwriting existing files
            # -------------------------------------------------

            if destination_path.exists():

                stem = destination_path.stem
                suffix = destination_path.suffix

                counter = 1

                while destination_path.exists():

                    destination_path = (
                        destination
                        / f"{stem}_{counter}{suffix}"
                    )

                    counter += 1

            try:

                shutil.move(
                    str(file_path),
                    str(destination_path)
                )

                moved.append(
                    f"{file_path.name} → {category}/"
                )

            except (OSError, shutil.Error) as e:

                failed.append(
                    f"{file_path.name}: {e}"
                )

    # ---------------------------------------------------------
    # RESULT
    # ---------------------------------------------------------

    output = [
        f"Organization complete.",
        f"Moved {len(moved)} file(s)."
    ]

    if moved:

        output.append("\nMoved files:")

        for item in moved:
            output.append(f"  {item}")

    if failed:

        output.append("\nFiles that could not be moved:")

        for item in failed:
            output.append(f"  {item}")

    return "\n".join(output)