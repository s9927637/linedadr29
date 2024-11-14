import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # 引入CORS模塊以支持跨域請求

app = Flask(__name__)
CORS(app)  # 開啟CORS支持

# 從環境變數中獲取Airtable的API資料
BASE_ID = os.getenv('BASE_ID')
TABLE_NAME = os.getenv('TABLE_NAME')
AIRTABLE_API_KEY = os.getenv('AIRTABLE_PERSONAL_ACCESS_TOKEN')

# 確認必要的環境變數是否設置
if not all([BASE_ID, TABLE_NAME, AIRTABLE_API_KEY]):
    raise ValueError("環境變數未正確設置")

AIRTABLE_API_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

# 提交表單到Airtable
@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        # 獲取表單提交的數據 (假設是JSON格式)
        data = request.get_json()

        # 從表單數據中提取必要的欄位
        userID = data.get('userID')
        name = data.get('name')
        phone = data.get('phone')
        vaccineName = data.get('vaccineName')
        appointmentDate = data.get('appointmentDate')
        formSubmitTime = data.get('formSubmitTime')

        # 檢查所有欄位是否都已提供
        if not all([userID, name, phone, vaccineName, appointmentDate, formSubmitTime]):
            return jsonify({"status": "error", "message": "缺少必要欄位"}), 400

        # 準備發送到Airtable的數據
        airtable_data = {
            "fields": {
                "姓名": name,
                "電話": phone,
                "疫苗名稱": vaccineName,
                "接種日期": appointmentDate,
                "userID": userID,
                "填表時間": formSubmitTime
            }
        }

        # 發送POST請求到Airtable
        response = requests.post(
            AIRTABLE_API_URL,
            headers={
                "Authorization": f"Bearer {AIRTABLE_API_KEY}",
                "Content-Type": "application/json"
            },
            json=airtable_data
        )

        # 檢查Airtable的API請求是否成功
        if response.status_code == 201:
            return jsonify({"status": "success", "message": "表單資料成功提交到Airtable!"}), 201
        else:
            return jsonify({"status": "error", "message": response.json()}), response.status_code

    except Exception as e:
        # 捕獲任何錯誤並返回錯誤信息
        print(f"錯誤訊息: {str(e)}")  # 記錄錯誤信息以便調試
        return jsonify({"status": "error", "message": "提交資料失敗，請稍後再試！"}), 500

if __name__ == '__main__':
    # 關閉調試模式，使用預設的 host 和 port
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
