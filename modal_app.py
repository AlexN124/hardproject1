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
        "sqlalchemy>=2.0.52",
        "psycopg[binary]>=3.3.4",
        "python-dotenv>=1.2.3",
    )
    .add_local_file("app.py", remote_path="/root/app.py")
)

# Reads SUPABASE_DB_URL out of the local .env at deploy time so the
# connection string never has to live in code.
db_secret = modal.Secret.from_dotenv()


@app.function(image=image, timeout=3600, min_containers=1, secrets=[db_secret])
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
