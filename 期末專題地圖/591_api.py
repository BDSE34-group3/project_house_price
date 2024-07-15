from flask import Flask, request, jsonify, render_template
import json
import os
import map  # Assuming this is a module for handling the map-related functions

app = Flask(__name__, template_folder='templates')
app.json.ensure_ascii = False 

@app.route('/', methods=['GET'])
def index():
    return render_template('591_try2.html')  # Serve the HTML page

# @app.route('/result', methods=['GET'])
# def get_houseData():
#     # 提取查詢參數
#     city = request.args.get('city')
#     district = request.args.get('district')

#     json_file_path = os.path.join('/path/to/your/json/file', 'result.json')  # Ensure correct path
#     try:
#         with open(json_file_path, 'r', encoding='utf-8') as file:  # Ensure UTF-8 encoding for non-ASCII characters
#             result_json = json.load(file)
#         # 根據城市和地區過濾數據
#         filtered_data = [item for item in result_json if item.get('city') == city and item.get('district') == district]
#         return jsonify(filtered_data)  # Return JSON response with filtered data
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


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
            
            extracted_details = {
                'index': item.get('index', '未提供'),
                'longitude': item.get('longtitude', '未提供'),  # 修正拼寫
                'latitude': item.get('latitude', '未提供'),
                '地址': item.get('地址', '未提供'),
                '含車位': item.get('含車位', '未提供'),
                '權狀坪數': item.get('權狀坪數', '未提供'),
                '屋齡': item.get('屋齡', '未提供'),
                '售價總價': item.get('售價總價', '未提供'),
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



















    # Check if pine_cone_json is a list and not empty
    if isinstance(pine_cone_json, list) and len(pine_cone_json) > 0:
        # Extract details from each entry in the list
        extracted_data = []
        for item in pine_cone_json:
            house_images_string = item.get('房屋圖片', '[]')
        if house_images_string and house_images_string != "不詳":
            try:
                house_images_array = json.loads(house_images_string.replace("'", '"'))
            except json.JSONDecodeError:
                house_images_array = []
        else:
            house_images_array = []
                
            house_images_array = json.loads(house_images_string.replace("'", '"'))
            image_url = house_images_array[0] if house_images_array else '未提供'
                
            extracted_details = {
                'index': item.get('index', '未提供'),
                'longitude': item.get('longtitude', '未提供'),
                'latitude': item.get('latitude', '未提供'),
                '地址': item.get('地址', '未提供'),
                '含車位': item.get('含車位', '未提供'),
                '權狀坪數': item.get('權狀坪數', '未提供'),
                '屋齡': item.get('屋齡', '未提供'),
                '售價總價': item.get('售價總價', '未提供'),
                '每坪售價': item.get('每坪售價', '未提供'),
                '房屋圖片': image_url,
            }
            extracted_data.append(extracted_details)

        




        # Add extracted data to the response dictionary
        response['extracted_data'] = extracted_data
    else:
        response['message'] = 'No data found or data is not in expected format.'

    return jsonify(response)





if __name__ == '__main__':
    app.run(debug=True)
