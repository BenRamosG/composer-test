import sys
import re

def get_dag_version(file_path, variable_name):

    try:

        with open(file_path, 'r') as f:
            content = f.read()

            pattern = rf'{variable_name} = "(.*?)"'  # Using raw f-string for regex
            match = re.search(pattern, content)

            if match:
                return match.group(1)
            else:
                return None

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
            

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python get_dag_version.py <filepath> <variablename>")
        sys.exit(1)

    file_path = sys.argv[1]
    name_var = sys.argv[2]

    result = get_dag_version(file_path, name_var)

    if result is not None:
        print(result)
