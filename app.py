import os
import logging
from flask import Flask, request, jsonify
from pyairtable import Api

app = Flask(__name__)

# 設置日誌輸出至標準輸出
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 從環境變數中獲取設置的值
AIRTABLE_PERSONAL_ACCESS_TOKEN = os.getenv('AIRTABLE_PERSONAL_ACCESS_TOKEN')
BASE_ID = os.getenv('BASE_ID')
TABLE_NAME = os.getenv('TABLE_NAME')
BASE_URL = os.getenv('BASE_URL')  # 可選項目，用於顯示在根路由

# 檢查必須的環境變數
if not AIRTABLE_PERSONAL_ACCESS_TOKEN:
    raise ValueError("AIRTABLE_PERSONAL_ACCESS_TOKEN is not set in the environment variables")

# 使用 Api.table 方法來初始化 Airtable 表
api = Api(AIRTABLE_PERSONAL_ACCESS_TOKEN)
table = api.table(BASE_ID, TABLE_NAME)

# 根路由，用於測試連線
@app.route('/', methods=['GET'])
def home():
    logger.info("根路由被訪問")
    return jsonify({'status': 'success', 'message': 'Welcome to the LIFF App API', 'base_url': BASE_URL}), 200

# Zeabur，用於健康檢查 URL
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

# 只處理 POST 請求
@app.route('/submit-form', methods=['POST'])
def submit_form():
    print(request.json) 
    data = request.json
    # 處理數據
    return jsonify({'status': 'success'})

    # 驗證傳入資料
    if 'userID' not in data:
        logger.warning("缺少 userID")
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
    logger.info(f"將要儲存到 Airtable 的紀錄: {new_record}")

    # 儲存到 Airtable
    try:
        response = table.create(new_record)
        logger.info(f"Airtable 回應: {response}")  # 紀錄 Airtable 的回應
        return jsonify({'status': 'success', 'message': 'Data saved successfully'})
    except Exception as e:
        logger.error(f"儲存至 Airtable 時出錯: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Failed to save data to Airtable'}), 500

if __name__ == '__main__':
    # 關閉調試模式，使用預設的 host 和 port
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
