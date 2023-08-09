import sys 
import json 
import os
from sniffles import sniffles 
from sniffles import sniffles_trio
from sniffles import sniffles_extra
from benchmarks.truvari import truvari 
from benchmarks.mendelian import mendelian 

def main(): 
    # Check number of given arguments (should be one JSON file) 
    if len(sys.argv) < 2:
        print("Incorrect number of arguments.")
        sys.exit(1)

    # Read contents of input JSON file with all the paths 
    with open(sys.argv[1], 'r') as file:
        json_data = json.load(file)

    # Set the working directory 
    os.chdir(json_data["directory"])

    # Check if the truvari benchmark needs to be tested 
    if len(json_data["truvari_versions"]) > 0: 

        snfjob_ids = []

        # Test the version of truvari on all the given test data sets
        # First run all sniffles jobs first so those jobs can run concurrenlty 
        for data_set in range(0, len(json_data["truvari_data"])): 
            alignment = json_data["truvari_data"][data_set][0]

            # Run sniffles jobs 
            snf_job = sniffles(alignment, json_data["current_snf"], json_data["new_snf"], data_set)
            snfjob_ids.append(snf_job.run())

        # Make sure to test all the different truvari versions
        for truv_type in range(0, len(json_data["truvari_versions"])): 

            # Now run all truvari jobs and collect results to compare the snf versions' performances 
            for id in range(0, len(snfjob_ids)): 
                bench_vcf = json_data["truvari_data"][id][1]
                bench_bed = json_data["truvari_data"][id][2]

                truvari_job = truvari(truv_type, json_data["truvari_versions"][truv_type], bench_vcf, bench_bed, snfjob_ids[id], id)
                truvari_job.run() 

    # Check if the mendelian benchmark needs to be tested 
    if len(json_data["mendelian_data"]) > 0: 
        mendelian_snf_ids = []

        # Make sure to test mendelian on all the given test data sets 
        for data_set in range(0, len(json_data["mendelian_data"])):
            alignment1 = json_data["mendelian_data"][data_set][0]

            # Run both verisons of sniffles on the given data set
            mendelian_sniffles = sniffles_trio(json_data["current_snf"], json_data["new_snf"], data_set, alignment1, alignment2, alignment3)
            job_ids = mendelian_sniffles.run()
            mendelian_snf_ids.append(job_ids)
            
        # Run mendelian jobs with correct respective snf job dependencies 
        for id_trio in range(0, len(mendelian_snf_ids)): 
            alignment2 = json_data["mendelian_data"][id_trio][1]
            alignment3 = json_data["mendelian_data"][id_trio][2]

            mendelian_job = mendelian(json_data["bcftools_plugin"], json_data["current_snf"], \
                          json_data["new_snf"], id_trio, mendelian_snf_ids[id_trio])
            mendelian_job.run()

    # Check if sniffles needs to be tested with extra parameters 
    if len(json_data["extra_param"]) != "": 

        # Run sniffles jobs with extra parameters on the alignment data provided 
        for data_set in range(0, len(json_data["truvari_data"])): 
            alignment = json_data["truvari_data"][data_set][0]

            snf_extra_job = sniffles_extra(alignment, json_data["current_snf"], json_data["new_snf"], data_set, json_data["extra_param"])
            snf_extra_job.run()

    return 0

if __name__ == "__main__": 
    main()