# 使用官方 Python 映像
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製並安裝依賴
COPY requirements.txt .
RUN pip install -r requirements.txt

# 複製應用程式文件
COPY . /app

# 開放端口
EXPOSE 8080

# 啟動 Flask 應用
CMD ["python", "app.py"]