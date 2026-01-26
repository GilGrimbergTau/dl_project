#!/bin/bash

# Define the loss functions
LOSS_FUNCTIONS=("Jaccard_Bce_Combined_0_3" "Jaccard")

# activate venv
source .venv/bin/activate

for LOSS in "${LOSS_FUNCTIONS[@]}"
do
    echo "================================================"
    echo "STARTING: Python training with Loss: $LOSS"
    echo "================================================"

    # Run python and pass the LOSS variable as the first argument
    python ./Cloud-Net-A-semantic-segmentation-CNN-for-cloud-detection/Cloud-Net/main_train.py "$LOSS"

    # Optional: Small delay to ensure hardware/drivers reset
    sleep 3

    # Kill any lingering python processes for the current user
    # -9 is a "force kill" to ensure GPU memory is freed
    pkill -u $(whoami) -9 python
    
    echo "Process for $LOSS terminated. Cleaning up..."
done

echo "Loop finished. All experiments complete."