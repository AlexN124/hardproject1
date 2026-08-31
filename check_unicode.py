import pandas as pd
import unicodedata

df = pd.read_csv(r'C:\Users\alexa\OneDrive\Desktop\nbafinaldata\NBAALLSTATS.csv')

# Check for non-ASCII characters
print("Players with non-ASCII characters:")
for name in df['PLAYER_NAME'].unique():
    if pd.isna(name):
        continue
    # Check if any character is non-ASCII
    has_non_ascii = any(ord(c) > 127 for c in name)
    if has_non_ascii:
        print(f"  {name}: {[f'{c}(U+{ord(c):04X})' for c in name if ord(c) > 127]}")

# Check for duplicate players after Unicode normalization
print("\n\nChecking for Unicode normalization issues:")
nfc_names = {}
nfd_names = {}

for name in df['PLAYER_NAME'].unique():
    if pd.isna(name):
        continue
    nfc = unicodedata.normalize('NFC', name)
    nfd = unicodedata.normalize('NFD', name)
    
    if nfc != name or nfd != name:
        print(f"  {name} has Unicode variations")
        print(f"    NFC: {nfc}")
        print(f"    NFD: {nfd}")

print("\n\nDone!")
