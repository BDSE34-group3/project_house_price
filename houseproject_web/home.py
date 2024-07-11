""" ====== 引用套件 ========== """
from flask import Flask, render_template, request, jsonify, abort
# 與作業系統進行互動
import os # 新加的

# CORS 是一種瀏覽器安全功能，用於允許或限制不同來源之間的資源請求
from flask_cors import CORS # 新加的

# 與 Line Bot 相關的套件
# Line Bot SDK 提供，用於處理 Line Bot 相關的操作和事件
from linebot import (LineBotApi, WebhookHandler)
# 異常類別，用於處理簽名驗證失敗的情況
from linebot.exceptions import (InvalidSignatureError)
# 來自 Line Messaging API 的 Python SDK，用於創建和處理 LINE 機器人消息
from linebot.models import *

# 引用 Pinecone_flask.py 的重點函式 「generate_response」
# from pinecone_flask import generate_response
from clean_function_flask import function_call



# 從 .env 檔案中讀取環境變數並加載到運行環境中
from dotenv import load_dotenv # 新加的

# Load environment variables from .env file
load_dotenv()

""" Flask """
# 初始化 Flask 應用程式
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)  # Enable CORS for all routes and origins

# 防止中文變成 unicode 編碼
app.json.ensure_ascii = False

# Configure FLASK_DEBUG from environment variable
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

""" Line Bot """
# Line Bot 初始化
# Line Bot - 放上 Channel Access Token (在 Messaging API)
line_bot_api = LineBotApi('cmQza/w3HEukIwQkDnWHAZE91Z5jXtUz7iJliE1qNF7vFRBLdSGeGgRwOHIpd8LrZthj6DHKegPbp55P/MvRZeVhvPXSTJFslCmNf8miZ/+G+43h8VF0Rv808WXXNV36QIB6grG8wG6HMxTG0omb5gdB04t89/1O/w1cDnyilFU=')

# Line Bot - 放上 Channel secret (在 Basic settings)
handler = WebhookHandler('effcf596d1da798d55cf96d5dc5cca11')

# Line Bot - 放上 Your user ID (在 Basic settings)
line_bot_api.push_message('Ud2bf1e46315c04f519eff373640c4803', TextSendMessage(text='你可以開始了') )


# 首頁
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/home", methods=["GET"])
def home():
    return render_template("index.html")

# 迎避設施
@app.route("/map", methods=["GET", "POST"])
def map():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            question = data.get("question")
            messages = []
            # response = generate_response(question)
            response = function_call(question, messages)
            return jsonify({"response": response})
        else:
            message = request.form.get("message")
            # response = generate_response(message)
            messages = []
            response = function_call(message, messages)
            return render_template("map.html", response=response)
    return render_template("map.html")

# 趨勢分析
@app.route("/trend", methods=["GET"])
def trend():
    return render_template("map.html")

# 聯絡我們
@app.route("/contact", methods=["GET"])
def contactus():
    return render_template("contact.html")

# 登入
@app.route("/signin", methods=["GET"])
def login():
    return render_template("signin.html")

# chat bot
@app.route("/chatbot", methods=["GET"])
def chatbot():
    return render_template("chatbot.html")


""" Line Bot """
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    msg = str(event.message.text)
    messages = []
    # response = generate_response(msg)
    response = function_call(msg, messages)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(response))

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0", port=8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    
