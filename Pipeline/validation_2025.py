import pandas as pd
import numpy as np

def validate_october_2025_aqi(file_path):
    """
    Loads the uploaded October 2025 AQI Excel sheet and computes descriptive statistics.
    """
    try:
        # Load Sheet1 from the uploaded Excel file
        df = pd.read_excel(file_path, sheet_name='Sheet1')
        print(f"Successfully loaded file: {file_path}")
        print(f"Total Days Tracked: {len(df)}")
        print(f"Columns detected: {list(df.columns)}\n")
        
        # Target column based on your file structure
        aqi_col = 'Daily AQI'
        
        if aqi_col not in df.columns:
            print(f"Error: '{aqi_col}' column not found in the file.")
            return df

        # Compute core statistical parameters
        mean_val = df[aqi_col].mean()
        std_val = df[aqi_col].std()
        median_val = df[aqi_col].median()
        mode_val = df[aqi_col].mode().tolist()
        min_val = df[aqi_col].min()
        max_val = df[aqi_col].max()

        # Display formatted statistical summary
        print("========================================")
        print("    OCTOBER 2025 AIR QUALITY SUMMARY    ")
        print("========================================")
        print(f"Mean AQI:    {mean_val:.2f}")
        print(f"Std Dev:     {std_val:.2f}")
        print(f"Median AQI:  {median_val:.2f}")
        print(f"Mode AQI:    {mode_val}")
        print(f"Min / Max:   {min_val} / {max_val}")
        print("========================================\n")
        
        # Optional: Print category breakdown
        print("AQI Category Distribution:")
        print(df['AQI Category'].value_counts())
        print("----------------------------------------")
        
        return df

    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
        return None

if __name__ == "__main__":
    # Pointing directly to your uploaded file
    file_path = r"C:\Users\admin\Downloads\AQI_Data\Oct2025.xlsx"
    validate_october_2025_aqi(file_path)