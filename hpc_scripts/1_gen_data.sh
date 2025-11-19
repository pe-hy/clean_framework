#!/bin/bash
#SBATCH --job-name=gen_data
#SBATCH --output=logs/gen_data/gen_data_%j.out
#SBATCH --error=logs/gen_data/gen_data_%j.err
#SBATCH --time=01:00:00
#SBATCH --account=project_465001424
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64GB
#SBATCH --partition=small-g

set -e

module --force purge
module load apptainer

SCRIPT_DIR="${SLURM_SUBMIT_DIR}"
SIF_FILE="container.sif"

cd "$SCRIPT_DIR"

# Run data generation
apptainer exec --nv \
    "$SIF_FILE" \
    python data_generation/generate_data.py