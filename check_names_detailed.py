import pandas as pd

df = pd.read_csv(r'C:\Users\alexa\OneDrive\Desktop\nbafinaldata\NBAALLSTATS.csv')

# Check for Ray Allen specifically
print("Ray Allen entries:")
ray = df[df['PLAYER_NAME'].str.strip() == 'Ray Allen']
print(f"Total rows: {len(ray)}")
print(f"Unique PLAYER_NAME values: {ray['PLAYER_NAME'].unique()}")
print(f"Byte representation: {[repr(x) for x in ray['PLAYER_NAME'].unique()]}")

print("\n" + "="*50 + "\n")

# Check for LaMelo Ball specifically  
print("LaMelo Ball entries:")
lamelo = df[df['PLAYER_NAME'].str.strip().str.lower() == 'lamelo ball']
print(f"Total rows: {len(lamelo)}")
print(f"Unique PLAYER_NAME values: {lamelo['PLAYER_NAME'].unique()}")
print(f"Byte representation: {[repr(x) for x in lamelo['PLAYER_NAME'].unique()]}")

print("\n" + "="*50 + "\n")

# Look for any duplicate player names with different formatting
print("Checking for case/whitespace variations:")
player_counts = {}
for name in df['PLAYER_NAME'].unique():
    normalized = name.strip().lower() if pd.notna(name) else name
    if normalized not in player_counts:
        player_counts[normalized] = []
    player_counts[normalized].append(name)

# Find players with multiple variations
duplicates = {k: v for k, v in player_counts.items() if len(v) > 1}
if duplicates:
    print(f"Found {len(duplicates)} players with naming variations:")
    for norm_name, variations in list(duplicates.items())[:10]:
        print(f"  {norm_name}: {variations}")
else:
    print("No naming variations found!")
