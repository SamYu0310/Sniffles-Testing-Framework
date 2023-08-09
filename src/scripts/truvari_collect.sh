#!/bin/bash
#SBATCH --job-name=sniffles_comparison
#SBATCH --tasks-per-node=2
#SBATCH --mem=2gb
#SBATCH --time=00:30:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0002

. /stornext/snfs4/next-gen/scratch/fritz/Yu_Sam/miniconda3/envs/python
conda activate python

TRUV_TYPE=$1
UNIQUE_ID=$2

# Retrieve summary.txt file after jobs are complete
truvari_summaries=()

for num in {1..2}; do
    if [ $num -eq 1 ]; then
        version=f"current_snf_${UNIQUE_ID}"
    else
        version=f"new_snf_${UNIQUE_ID}"
    fi

    # Retrieve summary.txt file from the directory
    summary_file_path="/users/u251429/myscratch/mytests/${TRUV_TYPE}truvari_${version}-GIABv0.6/summary.txt"

    if [ -f "$summary_file_path" ]; then
        truvari_summaries+=("$summary_file_path")
    else
        echo "Failed to find summary.txt for $version."
    fi
done

# Truvari parser
data1=$(cat "${truvari_summaries[0]}")
data2=$(cat "${truvari_summaries[1]}")

# Function to round floating-point numbers to the nearest ten thousandths place
round_to_ten_thousandths() {
    printf "%.4f" $1
}

# Function to format numbers without trailing zeros if they can be integers
format_number() {
    local number=$1
    if [[ "$number" == *".0000" ]]; then
        echo "${number%.*}"
    else
        echo "$number"
    fi
}

# Function to extract differences and format as JSON-like string
extract_difference() {
    local key=$1
    local value1=$2
    local value2=$3

    key=$(echo "$key" | sed 's/"//g')  # Remove double quotes from the key
    if [[ $key == *"FP"* || $key == *"FN"* ]]; then
        if (( $(echo "$value1 < $value2" | bc -l) )); then
            echo "\"$key\": +$(format_number "$(round_to_ten_thousandths "$(bc <<< "$value2 - $value1")")"), current_snf"
        elif (( $(echo "$value1 > $value2" | bc -l) )); then
            echo "\"$key\": +$(format_number "$(round_to_ten_thousandths "$(bc <<< "$value1 - $value2")")"), new_snf"
        else
            echo "\"$key\": 0, Equal"
        fi
    else
        if (( $(echo "$value1 > $value2" | bc -l) )); then
            echo "\"$key\": -$(format_number "$(round_to_ten_thousandths "$(bc <<< "$value1 - $value2")")"), current_snf"
        elif (( $(echo "$value1 < $value2" | bc -l) )); then
            echo "\"$key\": -$(format_number "$(round_to_ten_thousandths "$(bc <<< "$value2 - $value1")")"), new_snf"
        else
            echo "\"$key\": 0, Equal"
        fi
    fi
}

# Extract differences and write to the output file
echo "{" > "sniffles_comparison.txt"

while IFS= read -r line; do
    # Skip lines that start with "{" or "}"
    if [[ "$line" == "{"* || "$line" == "}"* ]]; then
        continue
    fi

    key=$(echo "$line" | awk -F':' '{print $1}' | sed 's/^[ \t]*//;s/[ \t]*$//')
    value1=$(echo "$data1" | jq -r ".$key")
    value2=$(echo "$data2" | jq -r ".$key")
    difference=$(extract_difference "$key" "$value1" "$value2")
    printf "    %s\n" "$difference" >> "sniffles_comparison.txt"
done < <(echo "$data1")

# Close the curly brace
echo "}" >> "sniffles_comparison.txt"