import os
import zipfile
import sys

# Colors
BACKGROUND = (30, 30, 46)
FOREGROUND = (205, 214, 244)
COLOR0 = (108, 112, 134)
COLOR1 = (243, 139, 168)
COLOR2 = (166, 227, 161)
COLOR3 = (249, 226, 175)
COLOR4 = (137, 180, 250)
COLOR5 = (203, 166, 247)
COLOR6 = (137, 220, 235)
COLOR7 = (205, 214, 244)

def convert_skin_folder_to_osk(skin_folder_path, destination_path):
    """
    Converts a skin folder into a `.osk` file.

    Args:
        skin_folder_path (str): Path to the skin folder.
        destination_path (str): Path to the destination folder.

    Returns:
        str: Path to the created `.osk` file.
    """
    # Read Skin.ini to get the skin name
    skin_ini_path = os.path.join(skin_folder_path, 'Skin.ini')
    with open(skin_ini_path, 'r') as f:
        for line in f:
            if line.lstrip().startswith('Name: '):
                skin_name = line.split(': ', 1)[1].strip()
                break

    # Create the .osk file
    osk_file_name = f'{skin_name}.osk'
    osk_file_path = os.path.join(destination_path, osk_file_name)

    # Create a ZIP archive of the skin folder
    with zipfile.ZipFile(osk_file_path, 'w') as zip_file:
        for root, _, files in os.walk(skin_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, skin_folder_path)
                zip_file.write(file_path, relative_path)

    return osk_file_path

def list_folders(path):
    """
    Lists the folders in the given path.

    Args:
        path (str): Path to list folders from.

    Returns:
        list: List of folders.
    """
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

def get_user_input(prompt, min_value, max_value):
    """
    Gets user input and validates it.

    Args:
        prompt (str): Prompt to display to the user.
        min_value (int): Minimum allowed value.
        max_value (int): Maximum allowed value.

    Returns:
        int: User input.
    """
    while True:
        try:
            value = input(prompt)
            if value.lower() == 'q':
                print("Exiting program.")
                sys.exit(0)
            value = int(value)
            if min_value <= value <= max_value:
                return value
            else:
                print(f"\033[38;2;{COLOR6[0]};{COLOR6[1]};{COLOR6[2]}mInvalid input. Please try again.\033[0m")
        except ValueError:
            print(f"\033[38;2;{COLOR6[0]};{COLOR6[1]};{COLOR6[2]}mInvalid input. Please enter a number or 'q' to exit.\033[0m")

def main():
    try:
        # Get the current working directory
        cwd = os.getcwd()

        # List the folders in the current working directory
        folders = list_folders(cwd)

        # Print the folders with numbers
        print(f"\033[38;2;{COLOR0[0]};{COLOR0[1]};{COLOR0[2]}m\033[0m")
        print(f"\033[38;2;{COLOR3[0]};{COLOR3[1]};{COLOR3[2]}mSelect one or more skin folders (separate with commas):\033[0m")
        for i, folder in enumerate(folders):
            print(f"\033[38;2;{COLOR4[0]};{COLOR4[1]};{COLOR4[2]}m{i+1}. {folder}\033[0m")

        # Get the selected folder numbers
        folder_numbers = input(f"\033[38;2;{COLOR2[0]};{COLOR2[1]};{COLOR2[2]}mEnter the numbers of the folders (or 'q' to exit): \033[0m")
        if folder_numbers.lower() == 'q':
            print("Exiting program.")
            sys.exit(0)
        folder_numbers = [int(num) - 1 for num in folder_numbers.split(',')]
        skin_folder_paths = [os.path.join(cwd, folders[num]) for num in folder_numbers]

        # List the possible destination folders
        destination_folders = ['Desktop', 'Documents', 'Downloads', 'Current Directory']

        # Print the destination folders with numbers
        print(f"\033[38;2;{COLOR3[0]};{COLOR3[1]};{COLOR3[2]}mSelect a destination folder:\033[0m")
        for i, folder in enumerate(destination_folders):
            print(f"\033[38;2;{COLOR4[0]};{COLOR4[1]};{COLOR4[2]}m{i+1}. {folder}\033[0m")

        # Get the selected destination folder number
        destination_number = get_user_input(f"\033[38;2;{COLOR5[0]};{COLOR5[1]};{COLOR5[2]}mEnter the number of the destination folder (or 'q' to exit): \033[0m", 1, len(destination_folders))

        # Get the destination path
        if destination_folders[destination_number - 1] == 'Current Directory':
            destination_path = cwd
        else:
            destination_path = os.path.join(os.path.expanduser('~'), destination_folders[destination_number - 1])

        # Convert the skin folders to .osk files
        for skin_folder_path in skin_folder_paths:
            osk_file_path = convert_skin_folder_to_osk(skin_folder_path, destination_path)
            print(f"\033[38;2;{COLOR7[0]};{COLOR7[1]};{COLOR7[2]}mCreated {osk_file_path}\033[0m")

    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit(0)

if __name__ == '__main__':
    main()
