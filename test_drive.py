from drive_auth import authenticate_google_drive

try:
    service = authenticate_google_drive()

    about = service.about().get(
        fields="user"
    ).execute()

    print("Connected Google Account:")
    print(about["user"]["emailAddress"])

except Exception as e:
    print("Authentication failed:")
    print(e)