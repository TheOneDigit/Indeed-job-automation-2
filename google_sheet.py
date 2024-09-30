import gspread
from google.oauth2 import service_account
import os 
from dotenv import load_dotenv
import json
load_dotenv()

# google_sheet_auth = json.loads(os.getenv('GOOGLE_SHEET_AUTH'))
# print(google_sheet_auth)
def insert_data_in_gsheet(data_list):
  
  google_sheet_auth = json.loads(os.getenv('GOOGLE_SHEET_AUTH'))

  scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
  creds = service_account.Credentials.from_service_account_info(google_sheet_auth, scopes=scope)
  client = gspread.authorize(creds)
  sheet_id = "165ItJWdThd2RvSDVbzz9ghLVe8pxIxEcdc4XDkF44Do"
  spreadsheet = client.open_by_key(sheet_id)
  worksheet = spreadsheet.get_worksheet(0)
  worksheet.append_rows(data_list)

  return f"https://docs.google.com/spreadsheets/d/{sheet_id}"


# dummy_data =[ ["Software Engineer", "Applied", "Full-time", "https://example.com/job1"] ]
# insert_data_in_gsheet(dummy_data)