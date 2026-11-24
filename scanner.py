
import os
from collections import defaultdict

from config import (
    SOURCE_DRIVE,
    FILE_CATEGORIES,
    EXCLUDED_DIRECTORIES,
    DESTINATION_ROOT
)


def scan_drive():

    print("\nStarting C: drive scan...")
    print("Please wait...\n")

    found_files = []

    inaccessible_directories = 0
    inaccessible_files = 0

    errors_by_directory = defaultdict(int)

    def handle_error(error):

        nonlocal inaccessible_directories

        inaccessible_directories += 1

        directory = os.path.dirname(
            error.filename or "Unknown"
        )

        errors_by_directory[directory] += 1

    for root, dirs, files in os.walk(
        SOURCE_DRIVE,
        topdown=True,
        onerror=handle_error
    ):

        # Exclude protected directories
        dirs[:] = [
            folder for folder in dirs
            if folder not in EXCLUDED_DIRECTORIES
            and os.path.commonpath([
                os.path.abspath(
                    os.path.join(root, folder)
                ).lower(),
                os.path.abspath(DESTINATION_ROOT).lower()
            ]) != os.path.abspath(DESTINATION_ROOT).lower()
        ]

        for filename in files:

            extension = os.path.splitext(filename)[1].lower()

            if extension not in FILE_CATEGORIES:
                continue

            file_path = os.path.join(root, filename)

            try:

                file_size = os.path.getsize(file_path)

                found_files.append({
                    "name": filename,
                    "path": file_path,
                    "extension": extension,
                    "size": file_size,
                    "category": FILE_CATEGORIES[extension]
                })

            except (PermissionError, OSError):

                inaccessible_files += 1

    print("\n========== SCAN SUMMARY ==========")

    print(f"Files identified: {len(found_files)}")
    print(f"Inaccessible directories: {inaccessible_directories}")
    print(f"Inaccessible files: {inaccessible_files}")

    print("\n========== FILE BREAKDOWN ==========")

    for extension, category in FILE_CATEGORIES.items():

        count = sum(
            1 for file in found_files
            if file["extension"] == extension
        )

        print(f"{extension}: {count} files")

    return found_files
