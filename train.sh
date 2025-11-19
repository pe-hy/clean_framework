#!/bin/bash
#SBATCH --job-name=llm-train
#SBATCH --account=OPEN-34-14
#SBATCH --partition=qgpu
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --output=logs/train/train_%j.out
#SBATCH --error=logs/train/train_%j.err

set -e

# Set your WandB API key here
export WANDB_API_KEY="WANDB-KEY-HERE"
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

module --force purge
module load apptainer

unset SINGULARITY_BINDPATH

SCRIPT_DIR="${SLURM_SUBMIT_DIR}"
SIF_FILE="${SCRIPT_DIR}/container.sif"

cd "$SCRIPT_DIR"

# Bind mount system CA certificates for SSL verification
BIND_OPTS="--bind /etc/pki/tls:/etc/pki/tls:ro"

# Run training
apptainer exec --nv --cleanenv --env WANDB_API_KEY="$WANDB_API_KEY" --env SSL_CERT_FILE="$SSL_CERT_FILE" "$SIF_FILE" python train.py