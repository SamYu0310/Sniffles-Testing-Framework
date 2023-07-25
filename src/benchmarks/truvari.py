import subprocess
import re 

class truvari: 
    def __init__(self, version, benchmark_vcf, benchmark_bed, snfjob_ids): 
        self.version = version
        self.benchmark_vcf = benchmark_vcf
        self.benchmark_bed = benchmark_bed
        self.snfjob_ids = snfjob_ids
    
    def run(self): 
        # Run scripts to run truvari on outputs of both sniffles versions - Command 1
        job_ids_command1 = []  # To store the job IDs for command1
        for num in range(0, 2):
            snf_version = "current_snf" if num == 0 else "new_snf"
            sniffles_output = f'{snf_version}output.vcf.gz'
            job_id = self.snfjob_ids[num]

            # Second command
            command1 = f'sbatch --chdir="/users/u251429/myscratch/mytests" --output="{snf_version}truvari_log.out" --error="{snf_version}truvari_log.err" --dependency afterok:{job_id} benchmark_job.sh {self.version} {self.benchmark_vcf} {self.benchmark_bed} {sniffles_output} truvari_{snf_version}'

            # Execute the second command
            process1 = subprocess.run(command1, shell=True, capture_output=True, text=True)

            # Get the job ID from the output of the second command
            output = process1.stdout.strip()
            match = re.search(r'\d+', output)
            job_id1 = ""
            if match:
                job_id1 = match.group()
                job_ids_command1.append(job_id1)
            else:
                raise ValueError("Failed to extract job ID for command2.")
        
        # Run scripts to run job to collect summaries of the truvari jobs and compare results - Command 2
        truvari_job1 = job_ids_command1[0]
        truvari_job2 = job_ids_command1[1]

        # Second command
        command2 = f'sbatch --chdir="/users/u251429/myscratch/mytests" --output="truvari_collect_log.out" --error="truvari_collect_log.err" --dependency afterok:{truvari_job1}:{truvari_job2} truvari_collect4.sh'

        # Execute the second command
        subprocess.run(command2, shell=True, capture_output=True, text=True)

        return 0