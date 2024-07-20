FROM ubuntu:22.04

RUN DEBIAN_FRONTEND=noninteractive && apt-get update

# 設定環境變數並更新套件列表
RUN apt-get update && \
    apt-get install -qy python3-pip nano sudo

# 安裝 Python 套件
RUN pip3 install flask line-bot-sdk

# 將 Web 資料夾中的內容複製到容器內的根目錄
ADD web /web

# 設定啟動命令
CMD ["python3", "/web/houseprice.py"]

