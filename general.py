import json
import os
import requests
from bs4 import BeautifulSoup

STORE_FEEDBACK = ['sellerScore', 'sellerTotalNum', 'sellerPositiveRate', 'sellerPositiveNum']
SELLER_INFO = ['topRatedSeller', 'formatOpenTime', 'openedYear', 'storeURL', 'storeFeedbackURL', 'storeName',
               'hasStore', 'openTime', 'countryCompleteName', 'payPalAccount']
META_DATA = ['title', 'description', 'keywords']


def make_general_http_request(item_id):
    try:
        url = f'https://www.aliexpress.com/item/{item_id}.html'
        response = requests.get(url, headers={'Accept-Language': 'en-US'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', text=lambda text: 'window.runParams' in text)
            script_content = script_tag.text if script_tag else None
            if script_content:
                start_index = script_content.find('{')
                end_index = script_content.rfind('}') + 1
                data_object_str = script_content[start_index+1:end_index-1]

                start_index = data_object_str.find('{')
                end_index = data_object_str.rfind('}') + 1
                data_object_str = data_object_str[start_index:end_index]

                data_object = json.loads(data_object_str)

                return data_object
            else:
                return None
        else:
            return None
    except Exception as e:
        raise Exception('http request failed to get general info')


def save_general_to_json(item_id, item_data):
    folder_path = f'db/{item_id}/'
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    file_path = f'{folder_path}item_{item_id}_general_data.json'

    with open(file_path, 'w') as json_file:
        json.dump(item_data, json_file, indent=2)

    print(f"Data saved to {file_path}")


def fetch_general_and_save(item_id):
    folder_path = f'db/{item_id}/'
    existing_file_path = f'{folder_path}item_{item_id}_general_data.json'
    if os.path.exists(existing_file_path):
        with open(existing_file_path, 'r') as existing_file:
            response = json.load(existing_file)
    else:
        response = make_general_http_request(item_id)
        if response:
            save_general_to_json(item_id, response)
        else:
            raise Exception(f"Item with ID {item_id} not found.")
    return response


class General:
    def __init__(self, item_id):
        self.item_id = item_id
        self.response = fetch_general_and_save(item_id)
        self.store_feedback = self.response.get('storeFeedbackComponent', {})

        trade = self.response.get('tradeComponent', {})
        self.sold_count = trade.get('formatTradeCount', 0)
        self.store_feedback = self.response.get('storeFeedbackComponent', {})

        seller_info = self.response.get('sellerComponent', {})
        self.seller_info = dict()
        for key in SELLER_INFO:
            self.seller_info[key] = seller_info.get(key, 0)

        meta_data = self.response.get('metaDataComponent', {})
        self.meta_data = dict()
        for key in META_DATA:
            self.meta_data[key] = meta_data.get(key, 0)

    def __str__(self):
        return f"sold_count: {self.sold_count}\n" \
               f"meta_data: {self.meta_data}\n" \
               f"seller_info: {self.seller_info}\n" \
               f"store_feedback: {self.store_feedback}"
