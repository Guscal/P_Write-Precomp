import nuke
import os
import subprocess

def open_script_directory_in_file_browser():
    
    script_path = nuke.root().name()

    
    if script_path:
       
        script_directory = os.path.dirname(script_path)

        # Open the script directory in a file browser based on the operating system
        if nuke.env['WIN32']:
            # Windows
            subprocess.Popen(['explorer', os.path.normpath(script_directory)])
        elif nuke.env['MACOS']:
            # macOS
            subprocess.Popen(['open', os.path.normpath(script_directory)])
        else:
            # Other platforms (Linux, etc.)
            print("File browser open not supported on this platform.")
    else:
        print("Script path is not available.")

# Call the function to open the script directory in a file browser
open_script_directory_in_file_browser()