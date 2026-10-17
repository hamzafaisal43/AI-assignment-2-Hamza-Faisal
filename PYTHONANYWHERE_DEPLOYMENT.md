# PythonAnywhere deployment guide

1. Create/sign in to https://www.pythonanywhere.com/
2. Upload this project folder (or upload and extract its ZIP) into `/home/YOURUSERNAME/churn_app`.
3. Open **Consoles → Bash** and run:
   ```
   cd /home/YOURUSERNAME/churn_app
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Open **Web → Add a new web app**. Select **Manual configuration** and the Python version available for your account.
5. Set the source code / working directory to:
   `/home/YOURUSERNAME/churn_app`
6. In the Web tab, open the WSGI configuration file and replace its contents with the following, changing `YOURUSERNAME`:
   ```
   import sys
   project_home = "/home/YOURUSERNAME/churn_app"
   if project_home not in sys.path:
       sys.path.insert(0, project_home)

   from app import app as application
   ```
7. In the Web tab, set the virtualenv path to:
   `/home/YOURUSERNAME/churn_app/venv`
8. Ensure the static files mapping is `/static/` → `/home/YOURUSERNAME/churn_app/static/`.
9. Click **Reload** in the Web tab.
10. Open `https://YOURUSERNAME.pythonanywhere.com/` and test the form. Also open `/health`, which should return `{"status":"ok","model":"Logistic Regression pipeline"}`.

Troubleshooting:
- Read the error log linked from the Web tab first.
- Verify `model.joblib` is in the project root and the WSGI project path matches your actual username/path.
- If the web app Python version differs from your virtualenv, recreate the virtualenv with the same Python version.
- Do not use `app.run()` in the WSGI file; the WSGI file should import `application`.
