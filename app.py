import pandas as pd
import plotly.express as px
import streamlit as st
import unicodedata

st.set_page_config(page_title="NBA Player Explorer", page_icon="🏀", layout="wide")

DATA_PATH = "nba_stats_2003_2010_combined.csv"

NUMERIC_COLS = [
    "MIN", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT",
    "FTM", "FTA", "FT_PCT", "OREB", "DREB", "REB", "AST", "STL",
    "BLK", "TO", "PF", "PTS", "PLUS_MINUS",
]


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        st.error(f" Data file not found: {path}")
        st.stop()
    except Exception as e:
        st.error(f" Error loading data: {e}")
        st.stop()
    
    # Validate required columns
    required_cols = ["PLAYER_NAME", "GAME_ID", "SEASON", "SEASON_TYPE", "TEAM_ABBREVIATION", "PTS", "MIN", "REB", "AST", "STL", "BLK"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f" Missing required columns: {', '.join(missing_cols)}")
        st.stop()
    
    # MIN comes in as "MM:SS" strings — convert to float minutes.
    def parse_min(v):
        if pd.isna(v):
            return None 
        s = str(v)
        if ":" in s:
            m, sec = s.split(":")
            return float(m) + float(sec) / 60
        try:
            return float(s)
        except ValueError:
            return None

    df["MIN"] = df["MIN"].apply(parse_min)
    for col in NUMERIC_COLS:
        if col != "MIN":
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Normalize player names: strip whitespace and normalize Unicode characters
    df["PLAYER_NAME"] = df["PLAYER_NAME"].str.strip()
    df["PLAYER_NAME"] = df["PLAYER_NAME"].apply(lambda x: unicodedata.normalize("NFC", x) if pd.notna(x) else x)
    
    return df


try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

st.title("🏀 NBA Player Explorer (2003–2010)")

tab_eda, tab_search = st.tabs(["📊 Dataset Overview (EDA)", "🔍 Player Search"])

with tab_eda:
    st.subheader("Dataset overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Unique players", f"{df['PLAYER_NAME'].nunique():,}")
    c3.metric("Unique games", f"{df['GAME_ID'].nunique():,}")
    c4.metric("Seasons", f"{df['SEASON'].nunique()}")

    st.caption("Each row is one player's box score line for one game, 2003-04 through 2009-10.")

    with st.expander("Raw sample & summary statistics"):
        st.dataframe(df.head(20), use_container_width=True)
        st.write("Summary statistics (numeric columns):")
        st.dataframe(df[NUMERIC_COLS].describe().T, use_container_width=True)
        st.write("Missing values per column:")
        missing = df.isna().sum()
        st.dataframe(missing[missing > 0].rename("missing_count"), use_container_width=True)

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        fig_pts_hist = px.histogram(
            df, x="PTS", nbins=40, title="Distribution of points scored per game"
        )
        fig_pts_hist.update_layout(xaxis_title="Points", yaxis_title="Count of player-games")
        st.plotly_chart(fig_pts_hist, use_container_width=True)

    with col_b:
        rows_per_season = df.groupby("SEASON").size().reset_index(name="Rows")
        fig_season_bar = px.bar(
            rows_per_season, x="SEASON", y="Rows", title="Player-game rows per season"
        )
        fig_season_bar.update_xaxes(type="category")
        st.plotly_chart(fig_season_bar, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        fig_min_pts = px.scatter(
            df.sample(min(5000, len(df)), random_state=42),
            x="MIN", y="PTS", opacity=0.35,
            title="Minutes played vs. points (5,000-row sample)",
        )
        fig_min_pts.update_layout(xaxis_title="Minutes", yaxis_title="Points")
        st.plotly_chart(fig_min_pts, use_container_width=True)

    with col_d:
        corr_cols = ["MIN", "PTS", "REB", "AST", "STL", "BLK", "TO", "FG_PCT"]
        corr = df[corr_cols].corr()
        fig_corr = px.imshow(
            corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
            title="Correlation between box score stats",
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    st.divider()
    st.subheader("Top scorers (min. 200 games played, regular season)")
    reg = df[df["SEASON_TYPE"] == "Regular Season"]
    per_player = reg.groupby("PLAYER_NAME").agg(GP=("PTS", "count"), PPG=("PTS", "mean"))
    top_scorers = per_player[per_player["GP"] >= 200].sort_values("PPG", ascending=False).head(15).reset_index()
    fig_top = px.bar(
        top_scorers.sort_values("PPG"), x="PPG", y="PLAYER_NAME", orientation="h",
        title="Top 15 career PPG (min. 200 games, 2003-2010)",
    )
    fig_top.update_layout(xaxis_title="Points per game", yaxis_title="")
    st.plotly_chart(fig_top, use_container_width=True)

with tab_search:
    players = sorted(df["PLAYER_NAME"].dropna().unique())
    if len(players) == 0:
        st.error("❌ No player data available in the dataset.")
        st.stop()
    default_idx = players.index("Ray Allen") if "Ray Allen" in players else 0
    player = st.selectbox("Search for a player", players, index=default_idx)

    season_type = st.radio("Season type", ["Regular Season", "Playoffs", "Both"], horizontal=True)

    pdf = df[df["PLAYER_NAME"] == player].copy()
    if season_type != "Both":
        pdf = pdf[pdf["SEASON_TYPE"] == season_type]

    if pdf.empty:
        st.warning("No games found for this player with the selected filters.")
        st.stop()

    pdf = pdf.sort_values("SEASON")

    # ---------- BANS (Big Ass Numbers) ----------
    games_played = len(pdf)
    career_ppg = pdf["PTS"].mean()
    career_rpg = pdf["REB"].mean()
    career_apg = pdf["AST"].mean()
    career_spg = pdf["STL"].mean()
    career_bpg = pdf["BLK"].mean()
    career_mpg = pdf["MIN"].mean()
    career_fg_pct = pdf["FGM"].sum() / pdf["FGA"].sum() if pdf["FGA"].sum() else 0
    career_fg3_pct = pdf["FG3M"].sum() / pdf["FG3A"].sum() if pdf["FG3A"].sum() else 0
    career_ft_pct = pdf["FTM"].sum() / pdf["FTA"].sum() if pdf["FTA"].sum() else 0

    teams = ", ".join(sorted(pdf["TEAM_ABBREVIATION"].dropna().unique()))
    seasons_span = f"{pdf['SEASON'].min()} – {pdf['SEASON'].max()}"

    st.subheader(player)
    st.caption(f"Team(s): {teams}  |  Seasons: {seasons_span}  |  Games: {games_played}")

    ban_style = """
    <div style="text-align:center;">
        <div style="font-size:2.6rem; font-weight:800; line-height:1;">{value}</div>
        <div style="font-size:0.85rem; color:gray; text-transform:uppercase; letter-spacing:0.05em;">{label}</div>
    </div>
    """

    row1 = st.columns(5)
    row1_data = [
        ("PPG", f"{career_ppg:.1f}"),
        ("RPG", f"{career_rpg:.1f}"),
        ("APG", f"{career_apg:.1f}"),
        ("SPG", f"{career_spg:.1f}"),
        ("BPG", f"{career_bpg:.1f}"),
    ]
    for col, (label, value) in zip(row1, row1_data):
        col.markdown(ban_style.format(value=value, label=label), unsafe_allow_html=True)

    row2 = st.columns(5)
    row2_data = [
        ("MPG", f"{career_mpg:.1f}"),
        ("FG%", f"{career_fg_pct*100:.1f}%"),
        ("3P%", f"{career_fg3_pct*100:.1f}%"),
        ("FT%", f"{career_ft_pct*100:.1f}%"),
        ("Games", f"{games_played}"),
    ]
    for col, (label, value) in zip(row2, row2_data):
        col.markdown(ban_style.format(value=value, label=label), unsafe_allow_html=True)

    st.divider()

    # ---------- Progression over time ----------
    st.subheader("Progression over time")

    season_avg = (
        pdf.groupby("SEASON")
        .agg(
            GP=("PTS", "count"),
            PPG=("PTS", "mean"),
            RPG=("REB", "mean"),
            APG=("AST", "mean"),
            SPG=("STL", "mean"),
            BPG=("BLK", "mean"),
            MPG=("MIN", "mean"),
            FGM=("FGM", "sum"),
            FGA=("FGA", "sum"),
            FG3M=("FG3M", "sum"),
            FG3A=("FG3A", "sum"),
            FTM=("FTM", "sum"),
            FTA=("FTA", "sum"),
        )
        .reset_index()
    )
    # Properly sort seasons (handles both regular format and edge cases)
    season_avg["SEASON"] = pd.Categorical(
        season_avg["SEASON"], 
        categories=sorted(season_avg["SEASON"].unique()), 
        ordered=True
    )
    season_avg = season_avg.sort_values("SEASON").reset_index(drop=True)
    
    season_avg["FG_PCT"] = season_avg["FGM"] / season_avg["FGA"].replace(0, pd.NA)
    season_avg["FG3_PCT"] = season_avg["FG3M"] / season_avg["FG3A"].replace(0, pd.NA)
    season_avg["FT_PCT"] = season_avg["FTM"] / season_avg["FTA"].replace(0, pd.NA)

    metric_choice = st.multiselect(
        "Stats to chart",
        ["PPG", "RPG", "APG", "SPG", "BPG", "MPG"],
        default=["PPG", "RPG", "APG"],
    )

    if metric_choice:
        chart_df = season_avg.melt(
            id_vars="SEASON", value_vars=metric_choice, var_name="Stat", value_name="Value"
        )
        fig = px.line(
            chart_df, x="SEASON", y="Value", color="Stat", markers=True,
            title=f"{player} — per-game averages by season",
        )
        fig.update_layout(
            xaxis_title="Season",
            yaxis_title="Per-game average",
            xaxis=dict(tickangle=-45)
        )
        fig.update_xaxes(type="category")
        st.plotly_chart(fig, use_container_width=True)

    shooting_choice = st.multiselect(
        "Shooting splits to chart", ["FG_PCT", "FG3_PCT", "FT_PCT"], default=["FG_PCT", "FG3_PCT", "FT_PCT"]
    )
    if shooting_choice:
        shoot_df = season_avg.melt(
            id_vars="SEASON", value_vars=shooting_choice, var_name="Split", value_name="Pct"
        )
        fig2 = px.line(
            shoot_df, x="SEASON", y="Pct", color="Split", markers=True,
            title=f"{player} — shooting percentages by season",
        )
        fig2.update_layout(
            xaxis_title="Season",
            yaxis_title="Percentage",
            yaxis_tickformat=".0%",
            xaxis=dict(tickangle=-45)
        )
        fig2.update_xaxes(type="category")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Season-by-season table")
    display_cols = ["SEASON", "GP", "PPG", "RPG", "APG", "SPG", "BPG", "MPG", "FG_PCT", "FG3_PCT", "FT_PCT"]
    fmt = {c: "{:.1f}" for c in ["PPG", "RPG", "APG", "SPG", "BPG", "MPG"]}
    fmt.update({c: "{:.1%}" for c in ["FG_PCT", "FG3_PCT", "FT_PCT"]})
    st.dataframe(
        season_avg[display_cols].style.format(fmt),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.subheader("Full game log")
    st.dataframe(
        pdf[["SEASON", "SEASON_TYPE", "TEAM_ABBREVIATION", "MIN", "PTS", "REB", "AST", "STL", "BLK", "TO", "FG_PCT", "FG3_PCT", "FT_PCT"]]
        .sort_values("SEASON"),
        use_container_width=True,
        hide_index=True,
    )
