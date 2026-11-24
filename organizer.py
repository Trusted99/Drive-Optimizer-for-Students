
import os
import shutil
import logging

from config import DESTINATION_ROOT, LOG_FILE, EXCLUDED_DIRECTORIES


def setup_logging():

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        force=True
    )


def is_safe_to_move(file_path):

    absolute_path = os.path.abspath(file_path)

    drive_root = os.path.abspath(os.path.splitdrive(absolute_path)[0] + os.sep)

    relative_path = os.path.relpath(absolute_path, drive_root)

    top_level_folder = relative_path.split(os.sep)[0]

    return top_level_folder not in EXCLUDED_DIRECTORIES


def get_unique_path(destination):

    if not os.path.exists(destination):
        return destination

    folder = os.path.dirname(destination)
    filename = os.path.basename(destination)

    name, extension = os.path.splitext(filename)

    counter = 1

    while True:

        new_name = f"{name}_{counter}{extension}"

        new_path = os.path.join(folder, new_name)

        if not os.path.exists(new_path):
            return new_path

        counter += 1


def move_files(found_files):

    setup_logging()

    print("\n========== FILE MOVEMENT ==========")

    approval = input(
        "\nDo you want to move the identified files? (yes/no): "
    ).strip().lower()

    if approval != "yes":

        print("Movement cancelled.")
        return

    moved = 0
    failed = 0

    for file in found_files:

        source = file["path"]

        if not is_safe_to_move(source):
            logging.warning("Skipped protected location: %s", source)
            continue

        destination_folder = os.path.join(
            DESTINATION_ROOT,
            file["category"]
        )

        os.makedirs(destination_folder, exist_ok=True)

        destination = os.path.join(
            destination_folder,
            file["name"]
        )

        destination = get_unique_path(destination)

        try:

            shutil.move(source, destination)

            logging.info(
                "MOVED | FROM: %s | TO: %s",
                source,
                destination
            )

            moved += 1

        except (OSError, shutil.Error) as error:

            logging.error(
                "FAILED | FILE: %s | ERROR: %s",
                source,
                error
            )

            failed += 1

    print("\n========== MOVEMENT SUMMARY ==========")

    print(f"Successfully moved: {moved}")
    print(f"Failed movements: {failed}")

    print(f"Movement log: {LOG_FILE}")
