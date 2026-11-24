
import os

# Source drive
SOURCE_DRIVE = r"C:\\"

# Destination folder
DESTINATION_ROOT = r"C:\Drive_Organizer"

# File extensions and destination folders
FILE_CATEGORIES = {
    ".pdf": "PDF_Files",
    ".ppt": "PPT_Files",
    ".pptx": "PPT_Files",
    ".docx": "DOCX_Files"
}

# Directories excluded from file movement
EXCLUDED_DIRECTORIES = {
    "Windows",
    "$Recycle.Bin",
    "System Volume Information",
    "Program Files",
    "Program Files (x86)",
    "ProgramData",
    "$WinREAgent",
    "Drive_Organizer"
}

# Logging configuration
LOG_DIRECTORY = os.path.join(
    DESTINATION_ROOT, "Logs"
)

LOG_FILE = os.path.join(
    LOG_DIRECTORY, "movement_log.txt"
)

# File movement settings
PRESERVE_DUPLICATES = True
