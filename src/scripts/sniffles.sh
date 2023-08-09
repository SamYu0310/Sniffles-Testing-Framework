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
INPUT=$2
OUTPUT=$3
REFERENCE="/stornext/snfs4/next-gen/scratch/luis/references/human-grch37-mainchr.fasta"

USE_TANDEM_REP="--tandem-repeats /users/sedlazec/mydir/sniffles2/data/pbsv_tandem_annotations/human_hs37d5.trf.bed"


NTASKS=8

${PROGRAM_PATH} \
    --input ${INPUT} \
    --vcf ${OUTPUT}.vcf.gz \
    --threads ${NTASKS} \
    --reference ${REFERENCE} \
    --minsvlen 50  \
    --sample-id ${OUTPUT} \
    --snf ${OUTPUT}.snf \
    ${USE_TANDEM_REP}
