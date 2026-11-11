import pandas as pd

def prepare_relative_window(file_path, event_date_str, start_offset=-10, end_offset=5):
    """
    Generalizes historical or live AQI data, mapping it to a relative T-day 
    index around any target event (T = 0).
    """
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    
    # Parse event date and extract its year dynamically
    event_date = pd.to_datetime(event_date_str)
    event_year = event_date.year
    
    # Dynamically append the correct year based on the event date argument
    df['Full_Date'] = pd.to_datetime(df['Date'].astype(str) + f' {event_year}', format='%b %d %Y')
    
    # Create universal relative day index (T-10, T+0, etc.)
    df['Days_From_Event'] = (df['Full_Date'] - event_date).dt.days
    
    # Filter to the comparative window
    window_df = df[(df['Days_From_Event'] >= start_offset) & (df['Days_From_Event'] <= end_offset)].copy()
    
    return window_df

if __name__ == "__main__":
    # 1. Process 2025 Historical Data around 2025
    file_path_2025 = r"C:\Users\admin\Downloads\AQI_Data\Oct2025.xlsx"
    event_2025 = "2025-10-20"
    
    df_2025_window = prepare_relative_window(file_path_2025, event_2025)
    
    print(f"--- 2025 Comparative Window (T-10 to T+5) ---")
    print(df_2025_window[['Full_Date', 'Days_From_Event', 'Daily AQI', 'AQI Category']])
    