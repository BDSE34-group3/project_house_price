from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__, template_folder="templates")
app.json.ensure_ascii = False  # 防止中文變成 unicode 編碼

# 首頁
@app.route("/", methods=["GET"])
def index():
    return render_template("houseprice.html")

@app.route("/home", methods=["GET"])
def home():
    return render_template("houseprice.html")

# 地圖
@app.route("/map", methods=["GET"])
def map():
    return render_template("map.html")

# 趨勢分析
@app.route("/trend", methods=["GET"])
def trend():
    return render_template("map.html")

# 聯絡我們
@app.route("/contactus", methods=["GET"])
def contactus():
    return render_template("map.html")

# 連接 tableau套件
@app.route("/tableau_embed.html")
def map_page():
    return render_template("tableau_embed.html")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
