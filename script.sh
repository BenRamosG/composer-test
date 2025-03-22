dag_id="customersss_12345"
version="12345"

instance="instance2"


composer_dags=$(gcloud composer environments run $instance --location=us-central1 dags list -- --output=json | jq "[.[] | select(.dag_id == \"$dag_id\")] | length ")
echo $composer_dags

if [[ "$composer_dags" -eq 0 ]]; then
    compile_errors=$(gcloud composer environments run $instance --location=us-central1 dags list-import-errors -- --output=json 2>&1 || true)
    json_output=$(echo "$compile_errors" | grep -o '\[.*\]$')

    echo $json_output

    if [[ "$json_output" != "[]" ]]; then

        transformed_json=$(echo "$json_output" | jq -r ' map({(.filepath | split("/") | last | split(".")[0]): .error}) | add')
        search="${dag_id%_${version}}"
        get_value=$(echo "$transformed_json" | jq -r ".$search")

        if [ "$get_value" == "null" ]; then
            echo "Guardar valor"
        else
            echo "$dag_id with error: $get_value"
        fi

    else
        echo "Es vacio, guarda el valor"
    fi
else
    echo "$dag_id was deployed correctly"
fi



# texto="[{"file_path":"1234"}]"

# get_value=$(echo "$texto" | jq -r ".file_path")

# echo $get_value
