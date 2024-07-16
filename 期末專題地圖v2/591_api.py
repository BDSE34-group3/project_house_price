from flask import Flask, request, jsonify, render_template
import json
import os
import map  # Assuming this is a module for handling the map-related functions

app = Flask(__name__, template_folder='templates')
app.json.ensure_ascii = False 

@app.route('/', methods=['GET'])
def index():
    return render_template('591_try2.html')  # Serve the HTML page


@app.route('/submit', methods=['GET'])
def submit_data():

     # Retrieve data from the query parameters
    city = request.args.get('city')
    district = request.args.get('district')
    total_ping = request.args.get('total_ping')
    total_price= request.args.get('total_price')
    property_type = request.args.get('property_type')
    
    full_url = request.url

    # Combine all data into one response dictionary
    response = {
        'city': city,
        'district': district,
        'total_ping': total_ping,
        'total_price': total_price,
        'property_type' : property_type,
        'message': 'Data received successfully!'
    }
    
    pine_cone_json = json.loads(map.main(full_url))
    print("pine_cone_json type:", type(pine_cone_json))
    print("pine_cone_json sample:", pine_cone_json[:2] if isinstance(pine_cone_json, list) else pine_cone_json)

    # Check if pine_cone_json is a list and not empty
    if isinstance(pine_cone_json, list) and len(pine_cone_json) > 0:
        # Extract details from each entry in the list
        extracted_data = []
        for item in pine_cone_json:
            house_images_string = item.get('房屋圖片', '[]')
            try:
                house_images_array = json.loads(house_images_string.replace("'", '"'))
                image_url = house_images_array[0] if house_images_array else '未提供'
            except json.JSONDecodeError:
                image_url = '未提供'

        for item in pine_cone_json:
            parkinglot_string = item.get('含車位', '[]')
    
            # 檢查 parkinglot_string 是否為字符串類型，並是否為 '1' 或 '0'
            if isinstance(parkinglot_string, str):
                if parkinglot_string == '1':
                    item['含車位'] = '含車位'
                elif parkinglot_string == '0':
                    item['含車位'] = '無車位'
            # 如果 parkinglot_string 是整數類型
            elif isinstance(parkinglot_string, int):
                if parkinglot_string == 1:
                    item['含車位'] = '含車位'
                elif parkinglot_string == 0:
                    item['含車位'] = '無車位'
            # 如果值不是 '1' 或 '0'，或者不是整數 1 或 0，保持原值
            else:
                item['含車位'] = str(parkinglot_string)

# 如果你需要在處理後使用更新的 pine_cone_json，它現在包含了修改後的值
            
            extracted_details = {
                'index': item.get('index', '未提供'),
                'longitude': item.get('longtitude', '未提供'),  # 修正拼寫
                'latitude': item.get('latitude', '未提供'),
                '地址': item.get('地址', '未提供'),
                '含車位': item.get('含車位', '未提供'),
                '權狀坪數': item.get('權狀坪數', '未提供'),
                '屋齡': item.get('屋齡', '未提供'),
                '售價總價': item.get('售價總價', '未提供'),
                '模型_實際價格': item.get('模型_實際價格', '未提供'),
                '每坪售價': item.get('每坪售價', '未提供'),
                '房屋圖片': image_url,
            }
            extracted_data.append(extracted_details)

        # Add extracted data to the response dictionary
        response['extracted_data'] = extracted_data
    else:
        response['message'] = 'No data found or data is not in expected format.'
        response['extracted_data'] = []

    print("Final response:", json.dumps(response, ensure_ascii=False, indent=2))
    return jsonify(response)

@app.route('/initial_data', methods=['GET'])
def get_initial_data():
    # 這裡你可以返回一些默認的或隨機的數據
    # 例如，你可以返回所有數據的一個子集，或者某個特定區域的數據
    
    # 示例：返回前100條數據
    initial_data = get_sample_data(100)  # 你需要實現這個函數
    
    response = {
        'message': 'Initial data loaded successfully!',
        'extracted_data': initial_data
    }
    
    return jsonify(response)

def get_sample_data(n):
    # 實現這個函數來返回一個包含n條數據的列表
    # 這可能涉及從數據庫或文件中讀取數據
    # 返回的數據格式應該與 submit_data 路由返回的格式相同
    pass





if __name__ == '__main__':
    app.run(debug=True)
