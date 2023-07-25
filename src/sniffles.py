import subprocess
import re 

class sniffles: 
    def __init__(self, alignment, current, new): 
        self.alignment = alignment
        self.current = current 
        self.new = new
    
    def run(self): 
         # Run scripts to run both versions of sniffles being tested - Command 1
        job_ids_command1 = []  # To store the job IDs for command1
        for num in range(0, 2):
            snf_version = "current_snf" if num == 0 else "new_snf"
            snf_path = self.current if num == 0 else self.new

            # First command
            command1 = f'sbatch --chdir="/users/u251429/myscratch/mytests" --output="{snf_version}_log.out" --error="{snf_version}_log.err" sniffles220_01hg.sh {snf_path} {self.alignment} {snf_version}output'

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
        
        return job_ids_command1 