import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
client = gspread.authorize(creds)
sheet = client.open("PAF").sheet1

def get_cell(nomCell):
    col = ord(nomCell[0])-ord('A')+1
    ligne = int(nomCell[1:])
    cell = sheet.cell(ligne,col).value
    return cell

print(get_cell('D4'))