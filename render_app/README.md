# Render App

To deploy on Render:

1. Push this folder to your GitHub repo.
2. Create a new Web Service on Render.
3. Set the Start Command to:
   ```
   uvicorn app:app --host 0.0.0.0 --port 10000
   ```
4. Add any required environment variables in the Render dashboard.
