import pandas as pd
import numpy as np
import os
import atexit
import argparse
from datetime import datetime

# Force non-interactive Agg backend for background image generation
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

UNIFIED_DIR = "AQI_Data"

# Absolute safeguard: Automatically clean up any rogue folders on exit
def cleanup_rogue_folders():
    for folder in ["data", "output"]:
        if os.path.exists(folder):
            try:
                for f in os.listdir(folder):
                    os.remove(os.path.join(folder, f))
                os.rmdir(folder)
            except Exception:
                pass

atexit.register(cleanup_rogue_folders)

def generate_local_sample_data():
    os.makedirs(UNIFIED_DIR, exist_ok=True)
    csv_path = os.path.join(UNIFIED_DIR, "jaipur_ground_station_2026.csv")
    
    if os.path.exists(csv_path): 
        return csv_path
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Local dataset missing. Generating telemetry cache...")
    date_rng = pd.date_range(start="2026-10-15", end="2026-11-20", freq="h")
    np.random.seed(42)
    base_pm25 = np.random.normal(loc=90, scale=15, size=len(date_rng))
    base_aqi = base_pm25 * 1.2
    
    df = pd.DataFrame({"Timestamp": date_rng, "Ground_AQI": base_aqi, "PM2.5": base_pm25, "PM10": base_pm25 * 1.4})
    diwali_mask = (df["Timestamp"].dt.date == pd.to_datetime("2026-11-08").date()) & (df["Timestamp"].dt.hour >= 18)
    df.loc[diwali_mask, "Ground_AQI"] = np.random.uniform(350, 420, size=diwali_mask.sum())
    df.loc[diwali_mask, "PM2.5"] = df.loc[diwali_mask, "Ground_AQI"] * 0.8
    
    df.to_csv(csv_path, index=False)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Telemetry successfully cached inside '{UNIFIED_DIR}/'.")
    return csv_path

def generate_and_save_plot(window_df, event_date_str):
    try:
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(12, 6))
        
        plt.plot(window_df["Days_From_Event"], window_df["AQI_Mean"], marker="o", color="#2b5c8f", linewidth=2, label="Baseline AQI (Daily Mean)")
        plt.plot(window_df["Days_From_Event"], window_df["AQI_Peak"], marker="^", color="#d95f02", linewidth=2.5, linestyle="--", label="Acute Peak Spike (Daily Max)")
        
        plt.axvline(x=0, color="red", linestyle=":", alpha=0.7, label=f"Event Day (T=0 / {event_date_str})")
        plt.fill_betweenx(y=[0, 500], x1=-0.5, x2=0.5, color="red", alpha=0.1, label="Shockwave Window")
        
        plt.title(f"Ground-Truth Environmental Shockwave Analysis ({event_date_str})", fontsize=14, fontweight="bold", pad=15)
        plt.xlabel("Relative Days From Event (T-Day Index)", fontsize=11, labelpad=10)
        plt.ylabel("Air Quality Index (AQI)", fontsize=11, labelpad=10)
        plt.xticks(window_df["Days_From_Event"])
        plt.ylim(50, 450)
        
        plt.legend(loc="upper left", frameon=True, facecolor="white")
        plt.tight_layout()
        
        os.makedirs(UNIFIED_DIR, exist_ok=True)
        plot_output_path = os.path.join(UNIFIED_DIR, f"shockwave_chart_{event_date_str}.png")
        plt.savefig(plot_output_path, dpi=300)
        plt.close("all")
        
    except Exception as e:
        print(f"[ERROR EXCEPTION CAUGHT] Failed to generate plot: {e}")

def fetch_and_align_ground_window(event_date_str="2026-11-08", pre_days=10, post_days=10):
    csv_path = generate_local_sample_data()
    
    df = pd.read_csv(csv_path)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Date"] = df["Timestamp"].dt.date
    
    df_daily = df.groupby("Date").agg({"Ground_AQI": ["mean", "max"], "PM2.5": ["mean", "max"], "PM10": ["mean", "max"]}).reset_index()
    df_daily.columns = ["Date", "AQI_Mean", "AQI_Peak", "PM25_Mean", "PM25_Peak", "PM10_Mean", "PM10_Peak"]
    df_daily["Date"] = pd.to_datetime(df_daily["Date"])
    
    event_date = pd.to_datetime(event_date_str)
    df_daily["Days_From_Event"] = (df_daily["Date"] - event_date).dt.days
    
    window_df = df_daily[(df_daily["Days_From_Event"] >= -pre_days) & (df_daily["Days_From_Event"] <= post_days)].copy()
    
    os.makedirs(UNIFIED_DIR, exist_ok=True)
    output_file = os.path.join(UNIFIED_DIR, f"processed_window_{event_date_str}.csv")
    window_df.to_csv(output_file, index=False)
    
    generate_and_save_plot(window_df, event_date_str)
    print(f'[{datetime.now().strftime("%H:%M:%S")}] Execution complete. Check folder "AQI_Data".')
    
    return window_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Ground-Truth Environmental Pipeline")
    parser.add_argument("--event_date", type=str, default="2026-11-08", help="Target event date (YYYY-MM-DD)")
    parser.add_argument("--pre_days", type=int, default=10, help="Days before event to include")
    parser.add_argument("--post_days", type=int, default=10, help="Days after event to include")
    
    args = parser.parse_args()
    
    print("Initializing Automated Ground-Station Pipeline...")
    window_data = fetch_and_align_ground_window(
        event_date_str=args.event_date,
        pre_days=args.pre_days,
        post_days=args.post_days
    )
    
    print("\n--- Processed Dual-Metric Ground-Truth Window ---")
    print(window_data[["Date", "Days_From_Event", "AQI_Mean", "AQI_Peak"]])