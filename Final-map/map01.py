import os
import json
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
pinecone_api_key = os.getenv('PINECONE_API_KEY')

# pinecone資料庫
index_name = "final"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") # 384維
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

#英中字典

def extract_keywords(url):
    query_params = parse_qs(urlparse(url).query)
    print(query_params)
    city_mapping = {
        "Taipei": "台北市",
        "NewTaipei": "新北市",
    }
    district_mapping = {
        "Songshan": "松山區",
        "Xinyi": "信義區",
        "Daan": "大安區",
        "Zhongshan": "中山區",
        "Zhongzheng": "中正區",
        "Datong": "大同區",
        "Wanhua": "萬華區",
        "Wenshan": "文山區",
        "Nangang": "南港區",
        "Neihu": "內湖區",
        "Shilin": "士林區",
        "Beitou": "北投區",
        "Banqiao": "板橋區",
        "Sanchong": "三重區",
        "Zhonghe": "中和區",
        "Yonghe": "永和區",
        "Xinzhuang": "新莊區",
        "Xindian": "新店區",
        "Tucheng": "土城區",
        "Luzhou": "蘆洲區",
        "Shulin": "樹林區",
        "Tamsui": "淡水區",
        "Xizhi": "汐止區",
        "Sanxia": "三峽區",
        "Ruifang": "瑞芳區",
        "Wugu": "五股區",
        "Taishan": "泰山區",
        "Linkou": "林口區",
        "Shenkeng": "深坑區",
        "Shiding": "石碇區",
        "Pinglin": "坪林區",
        "Sanzhi": "三芝區",
        "Shimen": "石門區",
        "Bali": "八里區",
        "Pingxi": "平溪區",
        "Wanli": "萬里區",
        "Wulai": "烏來區",
        "Shuangxi": "雙溪區",
        "Gongliao": "貢寮區",
        "Jinshan": "金山區",
        "Yingge": "鶯歌區"
    }
    property_type_mapping = {
        "apartment": "公寓",
        "villa": "別墅",
        "duplex": "透天厝",
        "elevator_building": "電梯大樓"
    }

    city = query_params.get('city', [None])[0]
    district = query_params.get('district', [None])[0]
    property_type = query_params.get('property_type', [None])[0]
    total_ping_min = int(query_params.get('total_ping_min', [-1])[0])
    total_ping_max = int(query_params.get('total_ping_max', [1000000])[0])
    total_price_min = int(query_params.get('total_price_min', [-1])[0])
    total_price_max = int(query_params.get('total_price_max', [3000])[0])
   
    
    # 提取並轉換區域名稱
    city = city_mapping[city]
    district = district_mapping[district]
    property_type = property_type_mapping[property_type]
    key_word_result = [city, district, property_type, total_price_min, total_price_max, total_ping_min, total_ping_max]

    return key_word_result

def pinecone_search(key_word_result, vectorstore, n=5):
    filter = {}

    if key_word_result[0] is not None:
        filter["縣市"] = {"$eq": key_word_result[0]}

    if key_word_result[1] is not None:
        filter["地區"] = {"$eq": key_word_result[1]}

    if key_word_result[2] is not None:
        filter["型態"] = {"$eq": key_word_result[2]}

    if key_word_result[3] is not None:
        filter["售價總價"] = {"$gte": key_word_result[3]}

    if key_word_result[4] is not None:
        filter["售價總價"] = {"$lte": key_word_result[4]}

    if key_word_result[5] is not None:
        filter["權狀坪數"] = {"$gte": key_word_result[5]}

    if key_word_result[6] is not None:
        filter["權狀坪數"] = {"$lte": key_word_result[6]}

    # print(filter)
    query = "0"
    response = vectorstore.similarity_search(query, k=n, filter=filter)
    return response

def get_result(search_results):
    result = []
    for doc in search_results:
        result.append(doc.metadata)
    result_json = json.dumps(result, ensure_ascii=False, indent=4)    
    return result_json

def main(url):
    list_key_word = extract_keywords(url)
    search_results = pinecone_search(list_key_word, vectorstore)
    search_json = get_result(search_results)
    return search_json

if __name__ == "__main__":
    url= "http://127.0.0.1:5000/?city=Taipei&district=Xinyi&total_price_min=100&total_price_max=5000&property_type=apartment&total_ping_min=10&total_ping_max=100"
    print(main(url))