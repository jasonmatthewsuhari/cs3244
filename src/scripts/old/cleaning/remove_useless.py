import pandas as pd

def filter_emoji_map(input_path, output_path):
    useful_columns = [
        "emoji","category", "title", "keywords"
    ]
    
    df = pd.read_csv(input_path, encoding="utf-8")
    df_filtered = df[useful_columns]
    df_filtered.to_csv(output_path, index=False, encoding="utf-8")

if __name__ == "__main__":
    input_csv = "../../data/emoji_map.csv"  # Change this path if needed
    output_csv = "../../data/filtered_emoji_map.csv"
    filter_emoji_map(input_csv, output_csv)
