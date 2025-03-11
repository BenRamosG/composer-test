import sys
import re

def modify_dag_version(file_path, new_version):
    """Modifies the dag_version in the given Python file."""

    try:

        with open(file_path, 'r') as f:
            content = f.read()

        updated_content = re.sub(r'dag_version = ".*?"', f'dag_version = "{new_version}"', content)


        with open(file_path, 'w') as f:
            f.write(updated_content)

            print(f"Successfully updated dag_version to {new_version} in {file_path}")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.stderr.write(f"Error: File not found at {file_path}")
        sys.stdout.flush()
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.stderr.write(f"Error: File not found at {file_path}")
        sys.stdout.flush()
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python modify_dag_version.py <filepath> <new_version>")
        sys.stderr.write(f"Error: File not found at {file_path}")
        sys.stdout.flush()
        sys.exit(1)

    file_path = sys.argv[1]
    new_version = sys.argv[2]

    modify_dag_version(file_path, new_version)
