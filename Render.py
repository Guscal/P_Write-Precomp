import nuke
import os
import re

def create_assets_folder():
    script_path = nuke.root().name()

    if script_path:
        script_directory = os.path.dirname(script_path)
        assets_folder = "_Assets"

        assets_path = os.path.join(script_directory, assets_folder)
        if not os.path.exists(assets_path):
            os.makedirs(assets_path)

        file_name = os.path.splitext(os.path.basename(script_path))[0]
        current_node = nuke.thisNode()
        text_value = current_node.knob("precompName").value()

        # Check if the filename has a version part and split it
        version_regex = '(\\.v\\d+)'
        match = re.search(version_regex, file_name)
        if match:
            # Filename has a version part, replace it with precompName and the version
            base_name = re.sub(version_regex, '', file_name)
            new_file_name = "{}_{}{}.####".format(base_name, text_value, match.group())
            new_folder_name = "{}_{}{}".format(base_name, text_value, match.group())
        else:
            # Filename does not have a version part, append precompName at the end
            new_file_name = "{}_{}.####".format(file_name, text_value)
            new_folder_name = "{}_{}".format(file_name, text_value)

        new_folder_path = os.path.join(assets_path, new_folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        else:
            print("Folder already exists. Skipping folder creation.")

        write_node1 = current_node.node("PrecompWrite1")
        write_node2 = current_node.node("PrecompWrite2")

        new_file_name_exr = new_file_name + ".exr"
        new_path_with_extension_exr = os.path.join(new_folder_path, new_file_name_exr)
        new_path_with_extension_exr = new_path_with_extension_exr.replace("\\", "/")

        file_output_knob1 = write_node1.knob("file")
        file_output_knob1.setValue(new_path_with_extension_exr)

        # If RenderJpgs is checked, write jpgs with PrecompWrite2.
        if current_node.knob("RenderJpgs").value():
            new_file_name_jpg = new_file_name + ".jpg"
            new_path_with_extension_jpg = os.path.join(new_folder_path, new_file_name_jpg)
            new_path_with_extension_jpg = new_path_with_extension_jpg.replace("\\", "/")

            file_output_knob2 = write_node2.knob("file")
            file_output_knob2.setValue(new_path_with_extension_jpg)

        print("File output paths updated.")
    else:
        print("Script path is not available.")

create_assets_folder()

# If checkbox is ticked, write with PrecompWrite2. If not, write with PrecompWrite1.
if nuke.thisNode().knob("RenderJpgs").value():
    write_node = nuke.thisNode().node("PrecompWrite2")
else:
    write_node = nuke.thisNode().node("PrecompWrite1")

write_node.knob("Render").execute()
