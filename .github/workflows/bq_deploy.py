import os
import json
from google.cloud import bigquery
import argparse

# Global Variables
try:
    parser = argparse.ArgumentParser(description='Process some Branch name and configs for bq')
    parser.add_argument('--env', type=str, required=True, help='The branch name.')
    parser.add_argument('--configs', type=str, required=True, help='The configs variable.')
    parser.add_argument('--location', type=str, required=True, help='The location for running bq query.')
    parser.add_argument('--files', type=str, required=False, help='Deploy specific files.') #BDRJ
    args = parser.parse_args()
    env = args.env
    configs_str = args.configs
    query_location = args.location
    files = args.files
except Exception as e:
    print(e)

bq = bigquery.Client(location=query_location)

error_list = []


def string_to_dict(input_string):
    pairs = input_string.split(',')
    result_dict = {}
    for pair in pairs:
        key, value = pair.split('=')
        key = key.strip().lower()
        value = value.strip()
        result_dict[key] = value
    return result_dict


def run_query(sql, project_id, configs, file=None):
    """Runs a SQL query on the specified project.
    Args:
        sql: The SQL query to run.
        project_id: The project ID to run the query on.
        configs: A dictionary of configuration values to use in the query.
        file: The file name/path that is running, [Non-functional use only]
    Returns: The results of the query.
    """
    try:
        # sql_query = read_sql(sql).format(**configs)
        print(f"Project_id: {project_id}")
        print(f"Path: {file}") #BDRJ
        print(f"Running Query: {sql}")
        job_config = bigquery.QueryJobConfig(dry_run=False)
        job = bq.query(sql, project=project_id, job_config=job_config)
        result = job.result()
        print(f"Job ID: {job.job_id}")
        print(f"State: {job.state}")
        print(f"Errors: {job.errors}")
        print(f"Schema: {job.schema}")
        # Check if there were errors
        if job.errors:
            raise Exception(f"Query failed with errors: {job.errors}")
    except Exception as e:
        print(f"#### :x: Error: {e}") #BDRJ
        error = {"file" : f"{file}", "error": e, "query": f"{sql}" } if file else {f"{sql}": e} #BDRJ
        error_list.append(error) #BDRJ


def replace_placeholders(query, placeholders, project_id):
    """Replace placeholders in the SQL query with values from config."""

    # Replace {gcp_project_id} placeholder with the argument value
    if '{gcp_project_id}' in query:
        print(f"Replacing placeholder: {{gcp_project_id}} with value: {project_id}")  # Debug: print replacement info
        query = query.replace('{gcp_project_id}', project_id)

    # Replace other placeholders from the JSON file
    for key, value in placeholders.items():
        if key != 'project_id':  # Skip 'project_id' since it is handled separately
            placeholder = f'{{{key}}}'  # Single curly braces
            if placeholder in query:
                print(f"Replacing placeholder: {placeholder} with value: {value}")  # Debug: print replacement info
            query = query.replace(placeholder, value)

    return query


def process_sql_files(file_paths):
    """Process each SQL file from the list of file paths and replace placeholders."""
    configs = string_to_dict(configs_str)
    project_id = configs["project_id"]
    for file_path in file_paths:
        # Check if the SQL file exists
        if file_path.endswith('.sql') and os.path.exists(file_path):
            # Determine the path to the config.json file
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(file_path))))
            config_path = os.path.join(base_dir, 'config.json')

            if os.path.exists(config_path):
                # Load config.json
                with open(config_path, 'r') as f:
                    config = json.load(f)

                # Read SQL query
                with open(file_path, 'r') as f:
                    query = f.read()

                # Replace placeholders
                updated_query = replace_placeholders(query, config, project_id)

                print("-" * 80)
                run_query(updated_query, project_id, configs, file_path)
            else:
                print(f"Config file not found: {config_path}")
        else:
            print(f"SQL file not found: {file_path}")

    if len(error_list) > 0:
        return error_list

def read_file_paths(file_path):
    """Read file paths from a given file, handling multiple paths per line."""
    file_paths = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                # Split line by spaces and add paths to the list
                file_paths.extend(line.strip().split())
    else:
        print(f"File not found: {file_path}")
    return file_paths


if __name__ == "__main__":
    if files:
        print('Lleno')
    else
        print('Vacio')
    
    # Paths to the changed files and renamed files lists
    all_changed_files_path = 'changed_sql_files/all_changed_files.txt'
    renamed_files_path = 'changed_sql_files/renamed_files.txt'

    # Process all changed files
    changed_files = read_file_paths(all_changed_files_path)
    print("Processing changed SQL files:")
    output_query = process_sql_files(changed_files)

    if output_query is not None:
        print(output_query)

    # Process renamed files (if needed)
    renamed_files = read_file_paths(renamed_files_path)
    if renamed_files:
        print("\nProcessing renamed SQL files:")
        process_sql_files(renamed_files)
