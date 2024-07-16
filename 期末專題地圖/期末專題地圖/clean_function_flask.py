import requests
import os
import json
from dotenv import load_dotenv
import lib.recommend_house as recommend
import lib.newmortgage as mort

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

def get_completion(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=1000, tools=None, tool_choice=None):
  payload = { "model": model, "temperature": temperature, "messages": messages, "max_tokens": max_tokens }
  if tools:
    payload["tools"] = tools
  if tool_choice:
    payload["tool_choice"] = tool_choice

  headers = { "Authorization": f'Bearer {openai_api_key}', "Content-Type": "application/json" }
  response = requests.post('https://api.openai.com/v1/chat/completions', headers = headers, data = json.dumps(payload) )
  obj = json.loads(response.text)

  if response.status_code == 200 :
    return obj["choices"][0]["message"] 
  else :
    return obj["error"]
  
def get_real_price_site():
    url = 'https://lvr.land.moi.gov.tw/'
    return url

available_tools = {
  "get_real_price_site": get_real_price_site,
  "generate_response": recommend.main,
  "mortgage_calculator":mort.calculate_loan_payments,
}

def get_completion_with_function_execution(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=800, tools=None, tool_choice=None):

  response = get_completion(messages, model=model, temperature=temperature, max_tokens=max_tokens, tools=tools,tool_choice=tool_choice)
  print(f"get_completion response:{response}")
  messages.append(response)

  if response.get("tool_calls"): 

    for tool_call in response["tool_calls"]:
      function_name = tool_call["function"]["name"]
      function_args = json.loads(tool_call["function"]["arguments"])
      function_to_call = available_tools[function_name]

      print(f"   called function {function_name} with {function_args}")
      function_response = function_to_call(**function_args)
      messages.append(
          {
              "tool_call_id": tool_call["id"], 
              "role": "tool",
              "name": function_name,
              "content": function_response,
          }
      )

    return get_completion_with_function_execution(messages, model=model, temperature=temperature, max_tokens=max_tokens, tools=tools,tool_choice=tool_choice)

  else:
    return response

def function_call(user_input, messages):
    system_input= "你是房屋智能客服，嚴禁回答問句、不相關的問題，確認回覆有完整回答到用戶問題，數字單位為萬或元"
    if len(messages) == 0:
        messages.append({"role": "system", "content": system_input})
    
    messages.append({"role": "user", "content": user_input})

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_real_price_site",
                "description": "顯示內政部實價登錄網站",
                "parameters": {
                    "type": "object",
                    "properties": {
                    },
                    "required": ["實價登錄"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "generate_response",
                "description": "根據使用者偏好提供房屋推薦",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_input": {
                            "type": "string",
                            "description": "keep original user_input",
                        }
                    },
                    "required": ["房屋、推薦"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "mortgage_calculator",
                "description": "計算房屋貸款，若無提及利率則預設為2.18%，",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "principal": {
                            "type": "integer",
                            "description": "貸款總額多少萬",
                        },
                        "years": {
                            "type": "integer",
                            "description": "還款年限",
                        },
                        "annual_rate": {
                            "type": "number",
                            "description": "利率",
                        }
                    },
                    "required": ["貸款、房貸"],
                },
            },
        }
    ]
    
    response = get_completion_with_function_execution(messages, tools=tools)
    return response["content"]

# if __name__ == "__main__":
#     messages = []
#     user_input = "我想找三重區3000萬以下的房子"
#     response = function_call(user_input, messages)
#     print(response)