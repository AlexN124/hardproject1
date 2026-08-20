NBA PLAYER EXPLORER (2003-2010)
================================

A Streamlit app for exploring NBA player box score stats from the
2003-04 through 2009-10 seasons. Search any player to see career
stat callouts and season-by-season progression, or browse the
dataset-wide EDA tab for distributions, correlations, and top
scorers.


PROJECT SETUP
-------------
1. Create a local project folder.
2. Open a terminal in that folder and launch Claude Code.
3. Use uv to manage the environment and packages:

     uv init --no-readme .
     uv add streamlit pandas plotly numpy

   (This repo already has a pyproject.toml / uv.lock with the
   dependencies pinned, so a fresh clone just needs `uv sync`.)


HOW TO RUN
----------
    uv sync
    uv run streamlit run app.py

The app opens at http://localhost:8501 by default.


DATA
----
File: nba_stats_2003_2010_combined.csv
- 217,589 rows, one row per player per game
- 892 unique players, 9,044 unique games
- 7 seasons: 2003-04 through 2009-10
- Columns include game/team identifiers, player identity, minutes,
  full shooting splits (FG/3P/FT), rebounds, assists, steals,
  blocks, turnovers, fouls, points, plus/minus, season, and season
  type (Regular Season / Playoffs)


INITIAL EDA + GRAPHICS (Dataset Overview tab)
----------------------------------------------
- Row/player/game/season summary metrics
- Raw sample + describe() summary statistics + missing value check
- Histogram: distribution of points scored per game
- Bar chart: player-game rows per season
- Scatter plot: minutes played vs. points (sampled)
- Correlation heatmap across MIN, PTS, REB, AST, STL, BLK, TO, FG_PCT
- Horizontal bar chart: top 15 career PPG (min. 200 games played)


PLAYER SEARCH TAB
------------------
- Player dropdown search + season type filter (Regular Season /
  Playoffs / Both)
- "BAN" (Big-Ass-Number) stat cards: career PPG, RPG, APG, SPG,
  BPG, MPG, FG%, 3P%, FT%, and total games played
- Line charts of per-game stats and shooting percentages by season
  (progression over time)
- Season-by-season summary table
- Full game log table


SCREENSHOTS
-----------
screenshots/eda_overview.jpg   - Dataset Overview (EDA) tab
screenshots/player_search.jpg  - Player Search tab (Ray Allen, BAN cards)


REPOSITORY
----------
https://github.com/AlexN124/hardproject1
