import os

from config import CHAR_LIMIT


def get_files_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_dir_abs, file_path))
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_path = (
            os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        )
        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_path, "r") as f:
            content = f.read(CHAR_LIMIT)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {CHAR_LIMIT} characters]'
                )
            return content
    except Exception as e:
        return f"Error: {e}"
