import subprocess
import re 

class sniffles: 
    def __init__(self, alignment, current, new, unique_id): 
        self.alignment = alignment
        self.current = current 
        self.new = new
        self.unique_id = unique_id
    
    def run(self): 
         # Run scripts to run both versions of sniffles being tested - Command 1
        job_ids_command1 = []  # To store the job IDs for command1
        for num in range(0, 2):
            snf_version = f"current_snf_{self.unique_id}" if num == 0 else f"new_snf_{self.unique_id}"
            snf_path = self.current if num == 0 else self.new

            # First command
            command1 = f'sbatch --output="{snf_version}_log.out" \
            --error="{snf_version}_log.err" sniffles.sh {snf_path} {self.alignment} \
            {snf_version}output'

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

class sniffles_trio(sniffles):
    def __init__(self, current, new, unique_id, alignment1, alignment2, alignment3): 
        super().__init__(None, current, new, unique_id) 
        self.alignment1 = alignment1
        self.alignment2 = alignment2
        self.alignment3 = alignment3 

    def run(self): 
        # Run scripts to run both versions of sniffles being tested - Command 1
        job_id_lists = []   # To store the two lists with current snf and new snf job ids 

        # Run both versions of sniffles on the alignment trio 
        for number in range(0, 2): 
            snf_version = "current_snf" if number == 0 else "new_snf"
            snf_path = self.current if number == 0 else self.new
            job_ids = []

            # Run one of the versions on all three alignments 
            for num in range(0, 3):
                person = f"MOTHER{self.unique_id}" if num == 0 else f"FATHER{self.unique_id}" if num == 1 \
                else f"PROBAND{self.unique_id}"
                alignment = self.alignment1 if num == 0 else self.alignment2 if num == 1 else self.alignment3

                # First command
                command1 = f'sbatch --output="{snf_version}_{person}_log.out" \
                --error="{snf_version}_{person}_log.err" sniffles.sh {snf_path} {alignment} \
                {snf_version}_{person}output'

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
            job_id_lists.append(job_ids)    #add list of ids for one version to overall list 
            
        return job_id_lists 

class sniffles_extra(sniffles): 
    def __init__(self, alignment, current, new, unique_id, extra_param): 
        super().__init__(alignment, current, new, unique_id) 
        self.extra_param = extra_param
    
    def run(self): 
         # Run scripts to run both versions of sniffles being tested - Command 1
        for num in range(0, 2):
            snf_version = f"current_snf{self.unique_id}" if num == 0 else f"new_snf{self.unique_id}"
            snf_path = self.current if num == 0 else self.new

            # First command
            command1 = f'sbatch --output="{snf_version}_log.out" \
            --error="{snf_version}_log.err" sniffles.sh {snf_path} {self.alignment} \
            {snf_version}_extra_output {self.extra_param}'

            # Execute the first command
            subprocess.run(command1, shell=True, capture_output=True, text=True)
        
        return 0