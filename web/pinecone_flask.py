import requests
import json
from dotenv import load_dotenv
from pprint import pp
import os
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

load_dotenv()

# 初始化Pinecone
pinecone_api_key = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=pinecone_api_key)

# 初始化 OpenAI
openai_api_key = os.getenv('OPENAI_API_KEY')

index_name = 'property'
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name, 
        dimension=384,  # all-MiniLM-L6-v2的向量維度是384
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1' 
        )
    )

index = pc.Index(index_name)

def get_completion(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=1000,format_type=None):
    
    payload = { 
        "model": model, 
        "temperature": temperature, 
        "messages": messages, 
        "max_tokens": max_tokens
    }

    if format_type:
        payload["response_format"] =  { "type": format_type }
        
    headers = {
        "Authorization": f'Bearer {openai_api_key}',
        "Content-Type": "application/json"
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers = headers, data = json.dumps(payload) )

    obj = json.loads(response.text)
    
    if response.status_code == 200 :
        return obj["choices"][0]["message"]["content"]
    else :
        return obj["error"]
  
def extract_keyword(user_input):
    prompt = f"""
        從以下的房產查詢描述中提取關於價錢或地區的關鍵字，並將其他主題的關鍵字或形容詞分開列出，並整理成json格式給我：

        範例2:
        描述:新北板橋區便宜套房，有電梯，新一點
        價錢關鍵字: 1000
        地區關鍵字: 板橋區
        其他關鍵字: 便宜套房, 有電梯, 新一點

        注意：地區關鍵字必須是新北或是台北的行政區 要加上區這個字，若用戶問句中無提行政區則選擇附近或最適合的行政區；
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
    # print(result1)
    result = json.loads(result1)
    # print(result)
    price = result.get("價錢關鍵字", "無")
    location = result.get("地區關鍵字", "無")
    other = result.get("其他關鍵字", "無")
    # print(f"price:{price}\nlocation:{location}\nother:{other}\n")

    return price, location, other

def keywords_to_vector(keywords):
    # 將關鍵字轉換為向量
    keyword_list = keywords.split(', ')
    keyword_embeddings = model.encode(keyword_list)
    # 平均嵌入向量
    combined_embedding = keyword_embeddings.mean(axis=0)
    return combined_embedding

def get_property_details(user_input, top_k=3):
    # 提取關鍵字
    price, location, others = extract_keyword(user_input)
    print(extract_keyword(user_input))

    # 將提取的關鍵字轉換為向量
    others_vector = keywords_to_vector(others)
    # 設置metadata filter
    filters = {
        "總價": {"$lt": int(price)},
        "地區": {"$eq": location}
    }

    # 進行檢索
    results = index.query(vector=others_vector.tolist(), top_k=top_k, filter=filters, include_metadata=True)
    print(f"檢索結果: {len(results['matches'])}")

    # 提取搜索結果的詳細信息
    properties = [result['metadata'] for result in results['matches']]
    
    return properties


def generate_response(user_input, top_k=3):
    properties = get_property_details(user_input, top_k)

    # 將屬性信息構造成描述
    property_descriptions = "\n".join([f"總價: {prop['總價']}萬, 格局: {prop['格局']}, 地址: {prop['地址']}" for prop in properties])

    prompt = f"""
    用戶的查詢描述: {user_input}

    以下是幾個符合用戶查詢的房產信息：

    {property_descriptions}
    請仔細閱讀用戶的查詢描述，請先印出{user_input}接著條列出三套適合的房產資訊，每條房產資訊下都附上一行優點陳述。最後一段總結你的推薦。限制回應在100字內。
    """

    response = get_completion([{ "role": "user", "content": prompt }], temperature=0)
    return response

# 使用示例
# user_input = "我想找林口1000萬兩房一廳交通方便的房子"
# response = generate_response(user_input, top_k=15)  # 修改top_k值以返回更多結果
# print(response)
