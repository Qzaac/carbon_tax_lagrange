import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
client = gspread.authorize(creds)
sheet = client.open("PAF").sheet1

def get_cell(nomCell):
    col = ord(nomCell[0])-ord('A')+1
    ligne = int(nomCell[1:])
    cell = sheet.cell(ligne,col).value
    return cell

def toFloat(arr):
    retour = []
    for i in arr:
        try:
            if(len(i.split(","))==2):
                retour.append(float(i.split(",")[0]+"."+i.split(",")[1]))
            else:
                retour.append(float(i))
        except:
            retour.append(i)
            print('texte trouvé')
            print(i)
    return retour

def update():
    doses = toFloat(sheet.col_values(16)[3:])
    #print(doses)
    prix = toFloat(sheet.col_values(6)[3:])
    carbone = toFloat(sheet.col_values(5)[3:])

    r = []
    for i in range(4):
        r.append(toFloat(sheet.col_values(8+2*i)[3:]))
    b = []
    for i in range(4):
        b.append(toFloat(sheet.col_values(9+2*i)[3:]))
    np.save('./data/prix.npy',prix)
    np.save('./data/carbone.npy', carbone)
    np.save('./data/r.npy', r)
    np.save('./data/b.npy', b)

def get_data():
    prix = np.load("./data/prix.npy")
    carbone = np.load("./data/carbone.npy")
    r = np.load("./data/r.npy")
    b = np.load("./data/b.npy")
    return prix, carbone, r, b

update()