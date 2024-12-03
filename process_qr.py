import json
import os
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from flask import Flask, request, jsonify

# Configurações
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "19OrQUbcWO5pNX62h7MXb5HIRLkBTcDgA3FgHRa72p4E"  # Insira o ID da planilha
RANGE_NAME = "ControleRefeitorio!A:D"  # Intervalo a ser atualizado na planilha

# Autenticação
credentials = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
service = build("sheets", "v4", credentials=credentials)

# Flask app
app = Flask(__name__)

@app.route("/process_qr.py", methods=["POST"])
def process_qr():
    try:
        data = request.json
        qrcode_data = json.loads(data.get("qrcode"))  # Decodifica os dados do QR Code
        user_id = qrcode_data["id"]
        user_name = qrcode_data["name"]

        # Adiciona os dados do QR Code à planilha
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = [[user_id, user_name, current_time, "Sim"]]
        body = {"values": values}

        # Envia os dados para a planilha
        sheet = service.spreadsheets()
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption="RAW",
            body=body
        ).execute()

        return jsonify({"success": True, "message": "Dados salvos com sucesso!"})

    except Exception as e:
        print(f"Erro ao processar QR Code: {e}")
        return jsonify({"success": False, "message": "Erro ao processar QR Code."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
