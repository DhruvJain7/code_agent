import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_path = (
            os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        )
        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python3", target_path]

        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output_string = ""
        if result.returncode != 0:
            output_string += f"\nProcess exited with code {result.returncode}"
        if not result.stdout and not result.stderr:
            output_string += "\nNo Output produced"
        else:
            if result.stdout:
                output_string += f"STDOUT:\n {result.stdout}"
            if result.stderr:
                output_string += f"STDERR:\n {result.stderr}"
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
