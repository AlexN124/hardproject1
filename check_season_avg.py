import pandas as pd

df = pd.read_csv(r'C:\Users\alexa\OneDrive\Desktop\nbafinaldata\NBAALLSTATS.csv')
kd = df[df['PLAYER_NAME'] == 'Kevin Durant'].copy()

# Simulate what the app does
pdf = kd.copy()

season_avg = (
    pdf.groupby("SEASON")
    .agg(
        GP=("PTS", "count"),
        PPG=("PTS", "mean"),
        RPG=("REB", "mean"),
        APG=("AST", "mean"),
    )
    .reset_index()
    .sort_values("SEASON")
)

print("Seasons in season_avg DataFrame:")
print(season_avg["SEASON"].tolist())
print(f"\nTotal rows: {len(season_avg)}")
print("\nFirst 5 rows:")
print(season_avg.head())
print("\nLast 5 rows:")
print(season_avg.tail())
