from flask import Flask, request, jsonify, send_from_directory
from google.oauth2.service_account import Credentials
import gspread
import os

app = Flask(__name__)

# Cấu hình Google Sheet
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
SHEET_ID = "1kONybfI9j8-el6u1KnCPXcF2arJ1s2uteqghsbfu2Uk"

def get_sheet_data():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID)
    worksheet = sheet.get_worksheet(0)
    return worksheet.get_all_records()

def tra_cuu_thu_tuc(query):
    query = query.lower()
    data = get_sheet_data()
    for row in data:
        if query in row['Tên thủ tục'].lower():
            return (
                f"🔎 **{row['Tên thủ tục']}**\n"
                f"- Lĩnh vực: {row['Lĩnh vực']}\n"
                f"- Hồ sơ: {row['Hồ sơ cần chuẩn bị']}\n"
                f"- Cơ quan tiếp nhận: {row['Cơ quan tiếp nhận']}\n"
                f"- Lệ phí: {row['Lệ phí']}\n"
                f"- Thời gian giải quyết: {row['Thời gian giải quyết']}\n"
                f"- Biểu mẫu: {row['Biểu mẫu đính kèm']}\n"
                f"- Link nộp online: {row['Link nộp online']}"
            )
    return "❌ Không tìm thấy thủ tục bạn cần. Vui lòng kiểm tra lại tên hoặc từ khoá rõ hơn."

@app.route('/')
def home():
    return "✅ Chatbot TTHC đang hoạt động!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    user_msg = data.get('message', {}).get('text', '')
    reply = tra_cuu_thu_tuc(user_msg)
    return jsonify({"message": {"text": reply}})

# ✅ Route xác minh Zalo
@app.route('/zalo_verifierSEIcBFgJAmiEaxygzPyGB22Bn3lC_HHWE3Wt.html')
def serve_verification_file():
    return send_from_directory(directory='.', path='zalo_verifierSEIcBFgJAmiEaxygzPyGB22Bn3lC_HHWE3Wt.html')

if __name__ == '__main__':
    app.run(debug=True)
