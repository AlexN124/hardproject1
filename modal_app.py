"""
Modal deployment for NBA Player Explorer Streamlit app.

Test locally against Modal (hot-reloads on save):
  modal serve modal_app.py

Deploy a persistent public endpoint:
  modal deploy modal_app.py
"""

import modal

app = modal.App("nba-player-explorer")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "streamlit>=1.62.0",
        "pandas>=3.0.5",
        "plotly>=6.9.0",
        "numpy>=2.4.6",
    )
    .add_local_file("app.py", remote_path="/root/app.py")
    .add_local_file(
        "nba_stats_2003_2010_combined.csv",
        remote_path="/root/nba_stats_2003_2010_combined.csv",
    )
)


@app.function(image=image, timeout=3600, min_containers=1)
@modal.web_server(port=8000, startup_timeout=60)
def run_streamlit():
    import subprocess

    subprocess.Popen(
        [
            "streamlit", "run", "/root/app.py",
            "--server.port=8000",
            "--server.address=0.0.0.0",
            "--server.headless=true",
            "--server.enableCORS=false",
            "--server.enableXsrfProtection=false",
        ],
        cwd="/root",
    )
