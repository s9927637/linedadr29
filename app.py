import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 從環境變數中獲取Airtable的API資料
AIRTABLE_API_URL = f"https://api.airtable.com/v0/{os.getenv('BASE_ID')}/{os.getenv('TABLE_NAME')}"
AIRTABLE_API_KEY = os.getenv("AIRTABLE_PERSONAL_ACCESS_TOKEN")  # Airtable的個人存取令牌

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
        
        # 準備發送到Airtable的數據，移除系統通知欄位
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
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # 關閉調試模式，使用預設的 host 和 port
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
