import pandas as pd
import glob
import os

def combine_files(prefix, data_dir="../../data"):
    files = sorted(glob.glob(os.path.join(data_dir, f"{prefix}_text_emoji_*.csv")))
    
    
    combined_df = pd.concat([pd.read_csv(f, encoding="utf-8") for f in files], ignore_index=True)
    output_file = os.path.join(data_dir, f"{prefix}.csv")
    combined_df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Successfully combined {len(files)} files into {output_file}")

if __name__ == "__main__":
    combine_files("test")
    combine_files("train")
    combine_files("valid")
