# Modal Deployment Setup for NBA Player Explorer

## Prerequisites
1. Install Modal: `pip install modal`
2. Authenticate: `python -m modal setup`
3. Install dependencies: `pip install -r requirements.txt`

## Deploy to Modal
Test locally against Modal (hot-reloads on save, endpoint stops when you Ctrl+C):
```
modal serve modal_app.py
```

Deploy a persistent public endpoint:
```
modal deploy modal_app.py
```

## Access the App
Once deployed, Modal will provide a public URL where your Streamlit app is running.
The app will be accessible at that URL with all your NBA player data.

## Local Testing
Before deploying to Modal, test locally:
```
streamlit run app.py
```
