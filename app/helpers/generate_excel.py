import pandas as pd
from datetime import datetime

def save_processed_data(processed_data, output_columns, file_prefix="processed"):
    """
    Saves processed data to an Excel file with a timestamped filename.

    Args:
        processed_data (list): List of dictionaries or rows to write to the Excel file.
        output_columns (list): Column headers for the output file.
        file_prefix (str): Prefix for the output file name (default is 'processed').

    Returns:
        str: The name of the saved Excel file.
    """
    output_df = pd.DataFrame(processed_data, columns=output_columns)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{file_prefix}_{timestamp}.xlsx"
    output_df.to_excel(output_file, index=False)
    print(f"✅ Processed file saved to: {output_file}")
    return output_file
