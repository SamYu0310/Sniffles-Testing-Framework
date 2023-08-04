import subprocess
import re 
import os
import time

class mendelian: 
    def __init__(self, plugins, current, new, unqiue_id, snf_ids): 
        self.plugins = plugins
        self.current = current
        self.new = new
        self.unique_id = unqiue_id
        self.snf_ids = snf_ids
    
    def run(self): 
         # Run both versions of sniffles when merging the snf triplets 
        job_ids_command1 = []  # To store the job IDs for command1
        for number in range(0, 2): 
            snf_version = "current_snf" if number == 0 else "new_snf"
            snf_path = self.current if number == 0 else self.new
            job_ids = self.snf_ids[number]

            # Merge the given snf triplet 
            snf1 = f"{snf_version}_MOTHER{self.unique_id}output"
            snf2 = f"{snf_version}_FATHER{self.unique_id}output"
            snf3 = f"{snf_version}_PROBAND{self.unique_id}output"
            
            with open("merge_input.tsv", "w") as file: 
                file.write(snf1 + "\n")
                file.write(snf2 + "\n")
                file.write(snf3 + "\n")

            # First command
            command1 = f'sbatch --chdir="/users/u251429/myscratch/mytests" --output="{snf_version}_merge_log.out" \
            --error="{snf_version}_merge_log.err" --dependency afterok:{job_ids[0]}:{job_ids[1]}:{job_ids[2]} \
            snf_merge.sh {snf_path} merge_input.tsv {snf_version}merge{self.unique_id}_output'

            # Execute the first command
            process1 = subprocess.run(command1, shell=True, capture_output=True, text=True)

            # Get the job ID from the output of the first command
            output = process1.stdout.strip()
            match = re.search(r'\d+', output)
            job_id1 = ""
            if match:
                job_id1 = match.group()
                job_ids_command1.append(job_id1)
            else:
                raise ValueError("Failed to extract job ID for command1.")
            
            # Wait for the jobs sent by command1 to complete
            for job in job_ids_command1:
                while True:
                    check_status_command1 = f'scontrol show job {job}'
                    process_status1 = subprocess.run(check_status_command1, shell=True, capture_output=True, text=True)
                    status_output1 = process_status1.stdout

                    if 'JobState=COMPLETED' in status_output1:
                        break  # Job completed, move to the next job_id1

                    time.sleep(10)  # Wait for 10 seconds before checking again

            # Set the BCFTOOLS_PLUGINS environment variable
            os.environ["BCFTOOLS_PLUGINS"] = f"{self.plugins}"

            # Command to run bcftools +mendelian2
            mendelian_command = f'bcftools +mendelian2 {snf_version}merge{self.unique_id}_output.vcf.gz -p \
            {snf_version}_MOTHER{self.unique_id}output,{snf_version}_FATHER{self.unique_id},{snf_version}_PROBAND{self.unique_id}'


            # Run the mendelian command and capture the output
            completed_process = subprocess.run(mendelian_command, shell=True, check=True, capture_output=True, text=True)
            output = completed_process.stdout

            # Write the output to a file
            with open(f'mendelian{self.unique_id}_output.txt', 'w') as output_file:
                output_file.write(output)

        return 0