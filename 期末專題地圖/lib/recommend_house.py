#用langChain的方法查詢
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import json
import os
import requests

load_dotenv()
# 從環境變量中獲取API密鑰
openai_api_key = os.getenv('OPENAI_API_KEY')
pinecone_api_key = os.getenv('PINECONE_API_KEY')

#pinecone資料庫名稱
index_name = "final"

#Embeddings方法
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") #384維
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

def get_completion(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=1000,format_type=None):
    payload = { "model": model, "temperature": temperature, "messages": messages, "max_tokens": max_tokens }
    if format_type:
        payload["response_format"] =  { "type": format_type }
    headers = { "Authorization": f'Bearer {openai_api_key}', "Content-Type": "application/json" }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers = headers, data = json.dumps(payload) )
    obj = json.loads(response.text)
    if response.status_code == 200 :
        return obj["choices"][0]["message"]["content"]
    else :
        return obj["error"]
  
def extract_keyword(user_input):
    prompt = f"""
        從以下的房產查詢描述中提取關於價錢或地區的關鍵字，並將其他主題的關鍵字或形容詞分開列出，並整理成json格式給我：

        範例:
        描述:新北板橋區便宜套房，有電梯，新一點
        價錢關鍵字: 1000
        地區關鍵字: 板橋區
        其他關鍵字: 便宜套房, 有電梯, 新一點

        注意：地區關鍵字必須是新北或是台北的行政區 一定要加上區這個字，若用戶問句中無提行政區則選擇附近或最適合的行政區。
        價錢關鍵字必須符合INT格式，為純整數數字。
        

        現在請提取以下描述中的關鍵字：
        描述: {user_input}
        價錢關鍵字:
        地區關鍵字
        其他關鍵字:
        """
    messages=[
                {"role": "system", "content": "你是一個能夠從用戶輸入中把價錢、地區的關鍵字分為一類，其他關鍵字分另一類的助手。"},
                {"role": "user", "content": prompt},
            ]
    result1 = get_completion(messages,format_type='json_object')
    result = json.loads(result1)
    price = result.get("價錢關鍵字", "180000")
    location = result.get("地區關鍵字", "無")
    other = result.get("其他關鍵字", "無")

    return price, location, other

#問題轉成向量搜尋(5筆)
def pinecone_search(price, location, other, vectorstore):
    query = ' '.join(other)  # 將列表轉換為字符串
    filter = {}
    # print(f"priceType = {type(price)}")
    if not price:
        filter["總價"] = {"$lt": 18000}
    else:
        filter["總價"] = {"$lt": int(price)}
    if location is not None:
        filter["地區"] = {"$eq": location}
    print(filter)
    response=vectorstore.similarity_search(query,k=5,filter=filter)
    return response

def format_properties(response):
    formatted_list = []
    for doc in response:
        metadata = doc.metadata
        formatted_list.append(f"總價: {metadata['總價']}萬, 格局:{metadata.get('格局', '無')}, 地址: {metadata['地址']} ,生活機能:{metadata.get('生活機能', '無')},型態:{metadata.get('型態', '無')},交通:{metadata.get('附近交通', '無')}")
    return "\n".join(formatted_list)


def generate_response(user_input, formatted_response):

    prompt = f"""
    用戶的查詢描述: {user_input}

    以下是幾個符合用戶查詢的房產信息：

    請仔細閱讀用戶的查詢描述，請先印出{user_input}接著參考{formatted_response}內容，挑出三套適合的房產，列點呈現房產資訊及優點。限制回應在250字內。
    """

    response = get_completion([{ "role": "user", "content": prompt }], temperature=0)
    return response


def main(user_input):
    price, location, other = extract_keyword(user_input)
    print(f"price:{price}, location:{location}, other:{other}")
    pinecone_search_result = pinecone_search(price, location, other, vectorstore)
    # print(pinecone_search_result)
    formatted_response = format_properties(pinecone_search_result)
    # print(formatted_response) 
    response = generate_response(user_input, formatted_response)

    return response

# if __name__ == "__main__":
#     #用戶問題
#     user_input = "我想在林口找交通方便的房子"
#     response = main(user_input)
#     print(response)