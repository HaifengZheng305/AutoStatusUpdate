from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os, json


class SpreadsheetClient:
    def __init__(
        self,
        spreadsheet_id: str | None = None,
        scopes: list[str] | None = None,
    ):
        load_dotenv()

        self.scopes = scopes or [
            "https://www.googleapis.com/auth/spreadsheets"
        ]

        # Load credentials from ENV (JSON)
        raw_json = os.environ.get("GOOGLE_SHEETS_JSON")
        if not raw_json:
            raise RuntimeError("GOOGLE_SHEETS_JSON not set")

        service_account_info = json.loads(raw_json)

        self.creds = Credentials.from_service_account_info(
            service_account_info,
            scopes=self.scopes,
        )

        self.service = build("sheets", "v4", credentials=self.creds)
        self.sheet = self.service.spreadsheets()

        self.spreadsheet_id = spreadsheet_id or os.getenv("SPREADSHEET_ID")
        if not self.spreadsheet_id:
            raise RuntimeError("SPREADSHEET_ID not set")

    # ---------- READ ----------
    def read(self, range_: str) -> list[list[str]]:
        result = self.sheet.values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_,
        ).execute()

        return result.get("values", [])

    # ---------- APPEND ----------
    def append(self, range_: str, values: list[list]):
        self.sheet.values().append(
            spreadsheetId=self.spreadsheet_id,
            range=range_,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": values},
        ).execute()

    # ---------- UPDATE ----------
    def update(self, range_: str, values: list[list]):
        self.sheet.values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_,
            valueInputOption="RAW",
            body={"values": values},
        ).execute()
