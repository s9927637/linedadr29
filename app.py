import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

AIRTABLE_API_URL = "https://api.airtable.com/v0/appaUWPkO0FfRkqTK/vaccinebooking"
AIRTABLE_API_KEY = "patxDzbKgz2SejSrT.c49168d0eeb6d48540d14ea6e7d04c6179b66c43d34fa23c83fc40f7bcfe672b"

@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.get_json()
    userID = data['userID']
    name = data['name']
    phone = data['phone']
    vaccineName = data['vaccineName']
    appointmentDate = data['appointmentDate']
    formSubmitTime = data['formSubmitTime']

    airtable_data = {
        "fields": {
            "姓名": name,
            "電話": phone,
            "疫苗名稱": vaccineName,
            "接種日期": appointmentDate,
            "userID": userID,
            "系統通知": False,  # 初始設為 False
            "填表時間": formSubmitTime
        }
    }

    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(AIRTABLE_API_URL, json=airtable_data, headers=headers)
    
    if response.status_code == 201:
        return jsonify({"message": "資料成功提交到 Airtable!"}), 200
    else:
        return jsonify({"message": "提交到 Airtable 失敗!"}), 500

if __name__ == '__main__':
    # 關閉調試模式，使用預設的 host 和 port
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
