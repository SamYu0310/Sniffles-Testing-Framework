#!/bin/bash
#SBATCH --job-name=truvari
#SBATCH --tasks-per-node=2
#SBATCH --mem=8gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0002


# conda from Moritz truvari env (clone)
. /users/sedlazec/mydir/sniffles2/moritz/miniconda3_4_10_1/etc/profile.d/conda.sh
conda activate truvari_clone

THUTHSET_VCF=$2
INCLUDE_BED=$3
INVCF=$4
OUTPUT=$5
GRCh37=$1

truvari bench \
    --base ${THUTHSET_VCF} \
    --comp ${INVCF} \
    --output ${OUTPUT}-GIABv0.6 \
    --passonly \
    --includebed ${INCLUDE_BED} \
    --refdist 2000 \
    --reference ${GRCh37} \
    --giabreport
