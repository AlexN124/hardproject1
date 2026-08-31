import pandas as pd

df = pd.read_csv(r'C:\Users\alexa\OneDrive\Desktop\nbafinaldata\NBAALLSTATS.csv')
kd = df[df['PLAYER_NAME'] == 'Kevin Durant']

print('KD seasons in data:', sorted(kd['SEASON'].unique()))
print('\nKD games per season:')
for season in sorted(kd['SEASON'].unique()):
    count = len(kd[kd['SEASON'] == season])
    print(f'  {season}: {count} games')
