import sys 
import json 
from sniffles import sniffles 
from sniffles import sniffles_trio
from benchmarks.truvari import truvari 

def main(): 
    # Check number of given arguments (should be one JSON file) 
    if len(sys.argv) < 2:
        print("Incorrect number of arguments.")
        sys.exit(1)

    # Read contents of input JSON file with all the paths 
    with open(sys.argv[1], 'r') as file:
        json_data = json.load(file)

    # Check if the truvari benchmark needs to be tested 
    if len(json_data["truvari_versions"]) > 0: 

        # Make sure to test all the different truvari versions
        for version in json_data["truvari_versions"]: 

            # Test the version of truvari on all the given test data sets 
            for data_set in json_data["truvari_data"]: 
                alignment = data_set[0]
                bench_vcf = data_set[1]
                bench_bed = data_set[2]

                # Run sniffles jobs 
                _ = sniffles(alignment, json_data["current_snf"], json_data["new_snf"])
                snfjob_ids = sniffles.run() 

                # Run truvari jobs and collect results to compare the snf versions' performances 
                _ = truvari(version, bench_vcf, bench_bed, snfjob_ids)
                truvari.run() 

    # Check if the mendelian benchmark needs to be tested 
    if len(json_data["mendelian_data"]) > 0: 

        # Make sure to test mendelian on all the given test data sets 
        for data_set in json_data["mendelian_data"]:
            alignment1 = data_set[0]
            alignment2 = data_set[1]
            alignment3 = data_set[2]

            # Run both verisons of sniffles on the given alignment triplet 
            _ = sniffles_trio(json_data["current_snf"], json_data["new_snf"], alignment1, alignment2, alignment3)
            job_ids = sniffles_trio.run()
            current_snf_ids = job_ids[0]
            new_snf_ids = job_ids[1]
            
            # Run mendelian jobs with correct respective snf job dependencies 
            

    return 0

if __name__ == "__main__": 
    main()