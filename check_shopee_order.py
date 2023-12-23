import requests
import json
from datetime import datetime

headers = {
    'authority': 'gmerchant.deliverynow.vn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'origin': 'https://partner.shopee.vn',
    'pragma': 'no-cache',
    'referer': 'https://partner.shopee.vn/',
    'sec-ch-ua': '\\\"Not_A Brand\\\";v=\\\"8\\\", \\\"Chromium\\\";v=\\\"120\\\", \\\"Google Chrome\\\";v=\\\"120\\\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\\\"Windows\\\"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-foody-access-token': 'B:yA2Bah2geFhLJPogqirV0/JDhoWWuwLqbr7+lAn9HZloOrvLh65S9stnaPsJChQH/5RZ+aborHAXoJe6rZ6Xgq6cWrBnpvbDUoucqIXmpCI=',
    'x-foody-api-version': '1',
    'x-foody-app-type': '1025',
    'x-foody-client-id': 'ffffffff-c9a4-034c-ffff-ffffc2e834d9',
    'x-foody-client-language': 'vi',
    'x-foody-client-type': '1',
    'x-foody-client-version': '3.0.0',
    'x-foody-entity-id': '10275361',
    'x-sap-ri': '485d8565eab34347f867f33e01014d9f45d1113d05b76495d6dd',
    'x-sap-sec': 'LiUiKXrXgTX9iTX9j4XqiTj9j4X9iTj9iTX8iTX9yTA9iuj9iTXTiTX9jt/3edr9iT8diTX9LTX9iT7zzqe/Na00mSmvv8MBNqH4L0jHEBEW43k0yXauBCUU14KNMNHdHAgEL6fMOovGEshIsNdr6KPFU+vODrdvFHg/Mjfnx7Wz4h1C/4G4NK9nRyrD9kJcr4X3M6xCRnRQLNY5WohAmuSHbpzNzEum17AIEq87X79nWXgRlEXIXVqeAoWlq1eBaTXMCJUEE9FO2amFb1F4FKiXmSzllO59HAhMVfzOdUhnZ5yQNtzqiTX9amAQaJ9PxmV9iTX94t/3edr9iTXaiTX9zTX9i9HX9BHbpXPYJa4/EjwxI1ztM5d0jdX9iFjcbByrbfj9fTX1iTr9jTXqiTX9fTX9iAN9iTXyiTX93/eTo2eBM3kjz5pxxC7W7BO1DgwFiTX9bFj+aFjNuyW=',
}

# params = {
#     'from_date': '2023-12-01',
#     'restaurant_ids': '1192464',
#     'to_date': '2023-12-22',
# }

class ShopeeFoodDataTracking:
    def __init__(self) -> None:
        self.data = None
    
    def get_item_histories(self):
        params = {
            'from_date': datetime.now().date().strftime("%Y-%m-%d"),
            'restaurant_ids': '1192464',
            'to_date': datetime.now().date().strftime("%Y-%m-%d"),
        }
        response = requests.get('https://gmerchant.deliverynow.vn/api/v5/seller/store/report/get_by_menu', headers=headers, params=params)
        return response.json()['data']

    def load_data(self):
        data = {}
        with open('histories.json', 'r') as f:
            data = json.load(f)
        return data
    
    def get_order(self, new_data, old_data):
        order = []
        for item in new_data['dish_reports']:
            previous_number = 0
            # print(old_data)
            filter_result = list(filter(lambda _item: _item['id'] == item['id'], old_data['dish_reports']))
            if len(filter_result) > 0:
                previous_number = filter_result[0]['dish_sum']
            if previous_number < item['dish_sum']:
                order_item:dict = item.copy()
                order_item['quantity'] = item['dish_sum'] - previous_number
                order_item.pop("dish_sum")
                order.append(order_item)
        return order
    
    def update_histories(self, data):
        updated_data = data.copy()
        updated_data['last_update_time'] = datetime.now().date().strftime("%Y-%m-%d")
        with open('histories.json', 'w') as f:
            json.dump(updated_data, f, indent=4)
        return None
    
    def process(self):
        current_data = self.get_item_histories()
        histories = self.load_data()
        
        if current_data.get('dish_sum_total', 0) == histories.get('dish_sum_total', 0):
            return {'order': []}
        
        order = self.get_order(current_data, histories)
        return {'order': order}