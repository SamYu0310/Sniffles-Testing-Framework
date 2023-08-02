import subprocess
import re 

class mendelian: 
    def __init__(self, current, new, unqiue_id, snf_ids): 
        self.current = current
        self.new = new
        self.unique_id = unqiue_id
        self.snf_ids = snf_ids
    
    def run(self): 
         # Run both versions of sniffles when merging the snf triplets 
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
                job_ids.append(job_id1)
            else:
                raise ValueError("Failed to extract job ID for command1.")

        return 0