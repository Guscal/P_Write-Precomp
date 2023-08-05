import os
import subprocess
import nuke

current_node = nuke.thisNode()

file_path = current_node["file"].getValue()

if file_path:
    print("File Path:", file_path)

    folder_path = os.path.dirname(file_path)

    # Open file browser based on the platform
    if folder_path:
        script_directory = os.path.normpath(folder_path)
        if nuke.env['WIN32']:
            # Windows
            subprocess.Popen(['explorer', script_directory])
        elif nuke.env['MACOS']:
            # macOS
            subprocess.Popen(['open', script_directory])
        else:
            # Other platforms (Linux, etc.)
            nuke.message("File browser open not supported on this platform.")
    else:
        nuke.message("Folder path is not available.")

    print("Updated Folder Path:", folder_path)
else:
    nuke.message("Please render something first.")
