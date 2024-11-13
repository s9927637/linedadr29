import os
from flask import Flask, request, jsonify
from pyairtable import Api

app = Flask(__name__)

# 從環境變數中獲取設置的值
AIRTABLE_PERSONAL_ACCESS_TOKEN = os.getenv('AIRTABLE_PERSONAL_ACCESS_TOKEN')
BASE_ID = os.getenv('BASE_ID')
TABLE_NAME = os.getenv('TABLE_NAME')
BASE_URL = os.getenv('BASE_URL')  # 讀取 BASE_URL

# 檢查令牌是否設置
if not AIRTABLE_PERSONAL_ACCESS_TOKEN:
    raise ValueError("AIRTABLE_PERSONAL_ACCESS_TOKEN is not set in the environment variables")

# 初始化 Api 並使用 Api.table 方法創建 Table
api = Api(AIRTABLE_PERSONAL_ACCESS_TOKEN)
table = api.table(BASE_ID, TABLE_NAME)

# 根路由
@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'success', 'message': 'Welcome to the LIFF App API', 'base_url': BASE_URL}), 200

# 提交表單路由
@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.get_json()

    # 驗證傳入資料
    if 'userID' not in data:
        return jsonify({'status': 'error', 'message': 'userID missing'}), 400 

    user_id = data.get('userID')
    name = data.get('name')
    phone = data.get('phone')
    vaccine_name = data.get('vaccineName')
    appointment_date = data.get('appointmentDate')

    # 新紀錄
    new_record = {
        'userID': user_id,
        '姓名': name,
        '電話': phone,
        '疫苗名稱': vaccine_name,
        '接種日期': appointment_date
    }

    # 儲存到 Airtable
    try:
        response = table.create(new_record)
        return jsonify({'status': 'success', 'message': 'Data saved successfully'})
    except Exception as e:
        print(f"Error saving to Airtable: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Failed to save data to Airtable'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
