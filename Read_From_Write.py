import nuke
import os
import re

def get_image_sequence_frames(file_path):
    directory, base_filename = os.path.split(file_path)
    filename_without_ext, file_extension = os.path.splitext(base_filename)

    if file_extension.lower() in ['.exr', '.tiff', '.tif', '.hdr', '.jpg', '.png', '.dpx']:
        frame_pattern = re.compile(r'_?(\d+)$')
    else:
        frame_pattern = re.compile(r'_?(\d+)_?')

    frame_numbers = [int(num) for num in frame_pattern.findall(filename_without_ext)]

    if frame_numbers:
        first_frame = min(frame_numbers)
        last_frame = max(frame_numbers)
    else:
        first_frame = nuke.root().firstFrame()
        last_frame = nuke.root().lastFrame()

    return first_frame, last_frame

def get_frame_range_from_folder(directory):
    files = os.listdir(directory)

    frame_pattern = re.compile(r'_?(\d+)_?')

    frame_numbers = []
    for filename in files:
        base_filename, file_extension = os.path.splitext(filename)
        if file_extension.lower() in ['.exr', '.tiff', '.tif', '.hdr', '.jpg', '.png', '.dpx']:
            frame_numbers.extend([int(num) for num in frame_pattern.findall(base_filename)])

    if frame_numbers:
        first_frame = min(frame_numbers)
        last_frame = max(frame_numbers)
    else:
        first_frame = nuke.root().firstFrame()
        last_frame = nuke.root().lastFrame()

    return first_frame, last_frame

def nearest_frame(frame, frame_list):
    return min(frame_list, key=lambda x: abs(x - frame))

def create_read_node_with_sequence(file_path):
    directory, _ = os.path.split(file_path)
    files = os.listdir(directory)
    image_extensions = ['.exr', '.tiff', '.tif', '.hdr', '.jpg', '.png', '.dpx']

    for file_extension in image_extensions:
        files_with_extension = [file for file in files if file.endswith(file_extension)]
        if not files_with_extension:
            continue

        modified_file_path = os.path.splitext(file_path)[0] + file_extension
        first_frame, last_frame = get_image_sequence_frames(modified_file_path)
        read_node = nuke.createNode("Read")
        read_node["file"].setValue(modified_file_path)

        folder_first_frame, folder_last_frame = get_frame_range_from_folder(directory)

        read_node["first"].setValue(nearest_frame(first_frame, range(folder_first_frame, folder_last_frame + 1)))
        read_node["last"].setValue(nearest_frame(last_frame, range(folder_first_frame, folder_last_frame + 1)))

        read_node["origfirst"].setValue(folder_first_frame)
        read_node["origlast"].setValue(folder_last_frame)

def main():
    current_node = nuke.thisNode()
    file_path = current_node["file"].getValue()

    if file_path:
        try:
            with nuke.root():
                create_read_node_with_sequence(file_path)
        except ValueError:
            read_node = nuke.createNode("Read")
            read_node["file"].setValue(file_path)
            nuke.message("No image sequence found in the folder. Created Read node with the original file path.")
    else:
        nuke.message("File path is empty. Please set a valid file path.")

main()
