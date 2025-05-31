from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/calendar"]

flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES)
creds = flow.run_local_server(port=0)          # opens browser
Path("token.json").write_text(creds.to_json())
print("✅  token.json written with Calendar scope")


