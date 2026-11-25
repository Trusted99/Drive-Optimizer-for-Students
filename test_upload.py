
from drive_uploader import GoogleDriveUploader

def main():

    print("=== GOOGLE DRIVE UPLOAD TEST ===")

    try:
        uploader = GoogleDriveUploader()

        file_path = input(
            "\nEnter the full path of the file to upload: "
        ).strip().strip('"')

        category = input(
            "Enter the file category (e.g. Documents): "
        ).strip()

        if not category:
            category = "Others"

        result = uploader.upload_file(
            file_path,
            category
        )

        print("\n=== UPLOAD RESULT ===")

        for key, value in result.items():
            print(f"{key}: {value}")

    except Exception as error:
        print(f"\nAn error occurred: {error}")


if __name__ == "__main__":
    main()
