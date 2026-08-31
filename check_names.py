import pandas as pd

df = pd.read_csv(r'C:\Users\alexa\OneDrive\Desktop\nbafinaldata\NBAALLSTATS.csv')

# Check for variations in player names (case sensitivity, spaces, etc.)
print("Sample of player names:")
print(df['PLAYER_NAME'].value_counts().head(20))

print("\n\nLooking for Ray Allen variations:")
ray_variations = df[df['PLAYER_NAME'].str.contains('ray', case=False, na=False)]['PLAYER_NAME'].unique()
print(ray_variations)

print("\n\nLooking for LaMelo variations:")
lamelo_variations = df[df['PLAYER_NAME'].str.contains('lamelo', case=False, na=False)]['PLAYER_NAME'].unique()
print(lamelo_variations)

print("\n\nLooking for any whitespace/formatting issues:")
# Check for leading/trailing spaces
has_spaces = df[df['PLAYER_NAME'] != df['PLAYER_NAME'].str.strip()]['PLAYER_NAME'].unique()
print(f"Players with leading/trailing spaces: {len(has_spaces)}")
if len(has_spaces) > 0:
    print(has_spaces[:5])
