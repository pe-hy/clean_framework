#!/bin/bash
#SBATCH --job-name=llm-train
#SBATCH --account=OPEN-34-14
#SBATCH --partition=qgpu
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --output=train/train_%A_%a.out
#SBATCH --error=train/train_%A_%a.err
#SBATCH --array=0-2

set -e

export WANDB_API_KEY="INSERT_YOUR_WANDB_API_K"
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

module --force purge
module load apptainer

unset SINGULARITY_BINDPATH

SCRIPT_DIR="${SLURM_SUBMIT_DIR}"
SIF_FILE="${SCRIPT_DIR}/container.sif"

cd "$SCRIPT_DIR"

# Define learning rates for each job
LRS=(1e-4 5e-4 1e-3)
LR=${LRS[$SLURM_ARRAY_TASK_ID]}

BIND_OPTS="--bind /etc/pki/tls:/etc/pki/tls:ro"

apptainer exec --nv --cleanenv \
    --env WANDB_API_KEY="$WANDB_API_KEY" \
    --env SSL_CERT_FILE="$SSL_CERT_FILE" \
    "$SIF_FILE" \
    python train.py optimizer.lr=$LR