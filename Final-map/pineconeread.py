import json
import requests as req


 # Combine all data into one response dictionary
response = {
        'city': city,
        'district': district,
        'total_ping': total_ping,
        'price_ping': price_ping,
        'property_type' : property_type,
        'message': 'Data received successfully!'
    }
pine_cone_json = json.loads(map.main(full_url))

# Check if pine_cone_json is a list and not empty
if isinstance(pine_cone_json, list) and len(pine_cone_json) > 0:
        # Extract details from each entry in the list
        extracted_data = []
        for item in pine_cone_json:
            house_images_string = item.get('房屋圖片', '[]')
            house_images_array = json.loads(house_images_string.replace("'", '"'))
            image_url = house_images_array[0] if house_images_array else '未提供'

            extracted_details = {
                'index' :item.get('index', '未提供'),
                'latitude': item.get('latitude', '未提供'),
                'longitude': item.get('longtitude', '未提供'),
                '地址': item.get('地址', '未提供'),
                '含車位': item.get('含車位', '未提供'),
                '權狀坪數': item.get('權狀坪數', '未提供'),
                '屋齡': item.get('屋齡', '未提供'),
                '實際價格': item.get('模型_實際價格', '未提供'),
                '每坪售價': item.get('每坪售價', '未提供'),
                '房屋圖片': image_url,
            }
            extracted_data.append(extracted_details)

        # Add extracted data to the response dictionary
        response['extracted_data'] = extracted_data
else:
        response['message'] = 'No data found or data is not in expected format.'