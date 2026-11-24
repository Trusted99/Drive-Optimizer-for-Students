
from scanner import scan_drive
from analyzer import analyze_files
from organizer import move_files


def main():

    print("=" * 50)
    print("       DRIVE FILE ORGANIZER")
    print("=" * 50)

    print("\n1. Scan C: drive")
    print("2. Exit")

    choice = input("\nSelect an option: ")

    if choice == "1":

        found_files = scan_drive()

        if not found_files:
            print("\nNo matching files were found.")
            return

        analyze_files(found_files)

        move_files(found_files)

    elif choice == "2":

        print("Exiting application.")

    else:

        print("Invalid selection.")


if __name__ == "__main__":
    main()
