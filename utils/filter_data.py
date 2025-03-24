import json
import os
from tokenizers import Tokenizer
import hydra
from omegaconf import DictConfig
from tqdm import tqdm
from data_pythia import get_tokenizer


def filter_by_length(data: list, tokenizer: Tokenizer, max_length: int) -> list:
    """Filter examples that exceed max token length."""
    filtered_data = []
    removed_count = 0
    max_found_length = 0

    print(f"\nFiltering examples longer than {max_length} tokens...")
    for example in tqdm(data):
        tokens = tokenizer(example["text"])["input_ids"]
        token_length = len(tokens)
        max_found_length = max(max_found_length, token_length)

        if token_length <= max_length:
            filtered_data.append(example)
        else:
            removed_count += 1

    return filtered_data, removed_count, max_found_length


def process_and_save_file(file_path: str, tokenizer: Tokenizer, max_length: int, sample_limit: int = None):
    """Process a single JSON file and overwrite with filtered data."""
    print(f"\nProcessing {file_path}")

    # Load data
    with open(file_path, "r") as f:
        data = json.load(f)
    
    # Apply sample limit if specified
    if sample_limit is not None:
        data = data[:sample_limit]
        
    original_count = len(data)
    print(f"Original example count: {original_count}")

    # Filter data
    filtered_data, removed_count, max_length_found = filter_by_length(
        data, tokenizer, max_length
    )

    # Save filtered data back to original file (replacing it)
    with open(file_path, "w") as f:
        json.dump(filtered_data, f, indent=2)

    print(f"Results for {os.path.basename(file_path)}:")
    print(f"- Examples removed: {removed_count}")
    print(f"- Maximum token length found: {max_length_found}")
    print(f"- Final example count: {len(filtered_data)}")
    print(f"- Removal percentage: {(removed_count/original_count)*100:.2f}%")

    return removed_count, max_length_found


@hydra.main(
    config_path="../config", config_name="config_base", version_base=None
)
def main(cfg: DictConfig):
    # Create tokenizer config that matches what get_tokenizer expects
    tokenizer_config = {
        "tokenizer_path": cfg.data.tokenizer_path
    }
    
    # Load tokenizer
    tokenizer = get_tokenizer(tokenizer_config, for_filter=False)

    # Get max token length from config or use default
    # Check if filter section exists
    if hasattr(cfg.data, 'filter'):
        max_token_length = cfg.data.filter.get('max_token_length', 2048)
        sample_limit = cfg.data.filter.get('sample_limit', None)
    else:
        max_token_length = 2048
        sample_limit = None
    
    print(f"Using maximum token length: {max_token_length}")
    if sample_limit:
        print(f"Sample limit per file: {sample_limit}")

    # Process all splits
    total_removed = 0
    overall_max_length = 0

    # Only process train and test files (no val)
    files_to_process = []
    if hasattr(cfg.data, 'train_file') and cfg.data.train_file:
        files_to_process.append(cfg.data.train_file)
    if hasattr(cfg.data, 'test_file') and cfg.data.test_file:
        files_to_process.append(cfg.data.test_file)

    if not files_to_process:
        print("No data files specified in configuration.")
        return

    for file_path in files_to_process:
        if not os.path.exists(file_path):
            print(f"Warning: File {file_path} does not exist. Skipping.")
            continue
            
        removed, max_length = process_and_save_file(
            file_path, tokenizer, max_length=max_token_length, sample_limit=sample_limit
        )
        total_removed += removed
        overall_max_length = max(overall_max_length, max_length)

    print("\nOverall Statistics:")
    print(f"Total examples removed: {total_removed}")
    print(f"Maximum token length found across all splits: {overall_max_length}")


if __name__ == "__main__":
    main()