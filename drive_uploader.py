
import os
import hashlib
import mimetypes

from googleapiclient.http import MediaFileUpload
from drive_auth import authenticate_google_drive


class GoogleDriveUploader:

    def __init__(self):
        self.service = authenticate_google_drive()
        self.root_folder_id = self.get_or_create_folder(
            "Python File Organizer"
        )

    def get_or_create_folder(self, folder_name, parent_id=None):

        # Escape characters for Google Drive query syntax.
        safe_name = folder_name.replace("\\", "\\\\").replace(
            "'", "\\'"
        )

        query = (
            f"name = '{safe_name}' "
            "and mimeType = 'application/vnd.google-apps.folder' "
            "and trashed = false"
        )

        if parent_id:
            query += f" and '{parent_id}' in parents"

        results = self.service.files().list(
            q=query,
            spaces="drive",
            fields="files(id, name)",
            pageSize=100
        ).execute()

        folders = results.get("files", [])

        if folders:
            print(f"Folder already exists: {folder_name}")
            return folders[0]["id"]

        # Create the folder if it doesn't exist.
        metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder"
        }

        if parent_id:
            metadata["parents"] = [parent_id]

        folder = self.service.files().create(
            body=metadata,
            fields="id"
        ).execute()

        print(f"Created folder: {folder_name}")

        return folder["id"]

    @staticmethod
    def calculate_md5(file_path):

        md5 = hashlib.md5()

        with open(file_path, "rb") as file:

            for chunk in iter(
                lambda: file.read(1024 * 1024), b""
            ):
                md5.update(chunk)

        return md5.hexdigest()

    def upload_file(self, file_path, category):

        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        file_name = os.path.basename(file_path)

        print(f"\nPreparing upload: {file_name}")

        # Create or retrieve the category folder.
        category_folder_id = self.get_or_create_folder(
            category,
            self.root_folder_id
        )

        # Calculate local file checksum.
        local_md5 = self.calculate_md5(file_path)

        # Check whether an identical file already exists.
        safe_name = file_name.replace("\\", "\\\\").replace(
            "'", "\\'"
        )

        query = (
            f"name = '{safe_name}' "
            f"and '{category_folder_id}' in parents "
            "and trashed = false"
        )

        existing = self.service.files().list(
            q=query,
            spaces="drive",
            fields="files(id, name, md5Checksum)",
            pageSize=100
        ).execute().get("files", [])

        for item in existing:

            if item.get("md5Checksum") == local_md5:
                print("Identical file already exists in Drive.")
                print("Skipping duplicate upload.")

                return {
                    "status": "skipped",
                    "file_id": item["id"],
                    "file_name": file_name,
                    "verified": True
                }

        # Detect file MIME type.
        mime_type, _ = mimetypes.guess_type(file_path)

        if not mime_type:
            mime_type = "application/octet-stream"

        # Prepare upload metadata.
        file_metadata = {
            "name": file_name,
            "parents": [category_folder_id]
        }

        media = MediaFileUpload(
            file_path,
            mimetype=mime_type,
            resumable=True
        )

        # Upload file.
        uploaded_file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, name, size, md5Checksum"
        ).execute()

        print("Upload completed.")

        # Verify uploaded file.
        remote_file = self.service.files().get(
            fileId=uploaded_file["id"],
            fields="id, name, size, md5Checksum"
        ).execute()

        remote_md5 = remote_file.get("md5Checksum")

        verified = remote_md5 == local_md5

        if verified:
            print("Upload verification successful!")
        else:
            print("WARNING: Checksum verification failed!")

        return {
            "status": "uploaded" if verified else "verification_failed",
            "file_id": remote_file["id"],
            "file_name": file_name,
            "size": remote_file.get("size"),
            "verified": verified
        }
