"""
One-time (or re-runnable) loader: pushes nba_stats_2003_2010_combined.csv
into the `nba_stats` table in Supabase Postgres.

Usage:
  uv run python load_to_supabase.py
"""

import os

import pandas as pd
import psycopg
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = "nba_stats_2003_2010_combined.csv"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS nba_stats (
    game_id             bigint NOT NULL,
    team_id             bigint NOT NULL,
    team_abbreviation   text NOT NULL,
    team_city           text NOT NULL,
    player_id           bigint NOT NULL,
    player_name         text,
    nickname            text,
    start_position      text,
    comment             text,
    min                 text,
    fgm                 double precision,
    fga                 double precision,
    fg_pct              double precision,
    fg3m                double precision,
    fg3a                double precision,
    fg3_pct             double precision,
    ftm                 double precision,
    fta                 double precision,
    ft_pct              double precision,
    oreb                double precision,
    dreb                double precision,
    reb                 double precision,
    ast                 double precision,
    stl                 double precision,
    blk                 double precision,
    "to"                double precision,
    pf                  double precision,
    pts                 double precision,
    plus_minus          double precision,
    season              text NOT NULL,
    season_type         text NOT NULL,
    PRIMARY KEY (game_id, player_id)
);
CREATE INDEX IF NOT EXISTS idx_nba_stats_player_name ON nba_stats (player_name);
CREATE INDEX IF NOT EXISTS idx_nba_stats_season ON nba_stats (season);
"""

COLUMNS = [
    "GAME_ID", "TEAM_ID", "TEAM_ABBREVIATION", "TEAM_CITY", "PLAYER_ID",
    "PLAYER_NAME", "NICKNAME", "START_POSITION", "COMMENT", "MIN",
    "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT",
    "OREB", "DREB", "REB", "AST", "STL", "BLK", "TO", "PF", "PTS",
    "PLUS_MINUS", "SEASON", "SEASON_TYPE",
]


def main():
    df = pd.read_csv(CSV_PATH)
    df = df[COLUMNS]

    db_url = os.environ["SUPABASE_DB_URL"]
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(SCHEMA_SQL)
            cur.execute("TRUNCATE TABLE nba_stats;")

            with cur.copy(
                "COPY nba_stats ("
                + ", ".join(c.lower() if c != "TO" else '"to"' for c in COLUMNS)
                + ") FROM STDIN"
            ) as copy:
                for row in df.itertuples(index=False, name=None):
                    copy.write_row(
                        tuple(None if pd.isna(v) else v for v in row)
                    )
        conn.commit()

        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM nba_stats;")
            print(f"Loaded {cur.fetchone()[0]:,} rows into nba_stats.")


if __name__ == "__main__":
    main()
