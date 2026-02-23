import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def conectar():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    cliente = gspread.authorize(creds)
    sheet = cliente.open_by_key(os.getenv("SHEET_ID")).sheet1
    return sheet

def inicializar_sheet():
    sheet = conectar()
    if sheet.row_count == 0 or sheet.cell(1, 1).value != "ID":
        sheet.clear()
        sheet.append_row(["ID", "Nombre", "IP", "Version", "Tipo", "Estado", "Fecha Registro"])

def obtener_nuevo_id(sheet):
    filas = sheet.get_all_values()
    return len(filas)  # encabezado cuenta como fila 1, entonces len = siguiente ID

def agregar_servidor(nombre, ip, version, tipo):
    sheet = conectar()
    nuevo_id = obtener_nuevo_id(sheet)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    sheet.append_row([nuevo_id, nombre, ip, version, tipo, "Offline", fecha])
    return nuevo_id

def obtener_servidores():
    sheet = conectar()
    filas = sheet.get_all_values()
    return filas[1:]  # saltar encabezado

def actualizar_estado(server_id, nuevo_estado):
    sheet = conectar()
    filas = sheet.get_all_values()
    for i, fila in enumerate(filas[1:], start=2):
        if str(fila[0]) == str(server_id):
            sheet.update_cell(i, 6, nuevo_estado)
            return True
    return False

def obtener_estadisticas():
    servidores = obtener_servidores()
    total = len(servidores)
    online = sum(1 for s in servidores if "Online" in str(s[5]))
    offline = total - online
    versiones = {}
    for s in servidores:
        v = s[3]
        versiones[v] = versiones.get(v, 0) + 1
    return total, online, offline, versiones