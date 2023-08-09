#!/bin/bash
#SBATCH --job-name=snffles2
#SBATCH --tasks-per-node=8
#SBATCH --mem=16gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0002


#conda envs
. /users/sedlazec/mydir/sniffles2/moritz/miniconda3_4_10_1/etc/profile.d/conda.sh
conda activate sniffles2.2


PROGRAM_PATH=$1
INPUT_LIST=$2
OUTPUT=$3

NTASKS=8

${PROGRAM_PATH} \
    --input "${INPUT_LIST[*]}" \
    --vcf ${OUTPUT}.vcf.gz \
    --minsvlen 50 \
    --threads ${NTASKS} \