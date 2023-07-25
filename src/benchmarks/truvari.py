import subprocess
import re 
import sys
import os
import time
import json

class truvari: 
    def __init__(self, version, benchmark_vcf, benchmark_bed): 
        self.version = version
        self.benchmark_vcf = benchmark_vcf
        self.benchmark_bed = benchmark_bed
    
    def run(self): 
         # Run scripts to run both versions of sniffles being tested - Command 1
        job_ids_command1 = []  # To store the job IDs for command1
        for num in range(0, 2):
            snf_version = "current_snf" if num == 0 else "new_snf"

            # First command
            command1 = f'sbatch --chdir="/users/u251429/myscratch/mytests" --output="{snf_version}_log.out" --error="{snf_version}_log.err" sniffles220_01hg.sh {json_data[snf_version]} {json_data["alignment"]} {snf_version}output'

            # Execute the first command
            process1 = subprocess.run(command1, shell=True, capture_output=True, text=True)

            # Get the job ID from the output of the first command
            output1 = process1.stdout.strip()
            match1 = re.search(r'\d+', output1)
            job_id1 = ""
            if match1:
                job_id1 = match1.group()
                job_ids_command1.append(job_id1)
            else:
                raise ValueError("Failed to extract job ID for command1.")
        
        # Run scripts to run truvari on outputs of both sniffles versions - Command 2
        job_ids_command2 = []  # To store the job IDs for command2
        for num in range(0, 2):
            snf_version = "current_snf" if num == 0 else "new_snf"
            sniffles_output = f'{snf_version}output.vcf.gz'
            job_id = job_ids_command1[num]

            # Second command
            command2 = f'sbatch --chdir="/users/u251429/myscratch/mytests" --output="{snf_version}truvari_log.out" --error="{snf_version}truvari_log.err" --dependency afterok:{job_id} benchmark_job.sh {self.version} {self.benchmark_vcf} {self.benchmark_bed} {sniffles_output} truvari_{snf_version}'

            # Execute the second command
            process2 = subprocess.run(command2, shell=True, capture_output=True, text=True)

            # Get the job ID from the output of the second command
            output2 = process2.stdout.strip()
            match2 = re.search(r'\d+', output2)
            job_id2 = ""
            if match2:
                job_id2 = match2.group()
                job_ids_command2.append(job_id2)
            else:
                raise ValueError("Failed to extract job ID for command2.")

        """
        # Wait for the jobs sent by command2 to complete
        for job_id2 in job_ids_command2:
            while True:
                check_status_command2 = f'scontrol show job {job_id2}'
                process_status2 = subprocess.run(check_status_command2, shell=True, capture_output=True, text=True)
                status_output2 = process_status2.stdout

                if 'JobState=COMPLETED' in status_output2:
                    break  # Job completed, move to the next job_id2

                time.sleep(300)  # Wait for 5mins before checking again
        """
