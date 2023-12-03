import json
import os
import requests

FILTERS_REVIEW = ["additional", "local", "with_personal", "image", "all"]
STARTS_NUM_REVIEW = ["oneStarNum", "twoStarNum", "threeStarNum", "fourStarNum", "fiveStarNum"]
STARTS_RATE_REVIEW = ["oneStarRate", "twoStarRate", "threeStarRate", "fourStarRate", "fiveStarRate"]


def make_feedback_http_request(item_id):
    url = f'https://feedback.aliexpress.com/pc/searchEvaluation.do?productId={item_id}&lang=en_US&country=IL&page=1' \
          f'&pageSize=500&filter=all&sort=complex_default'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None


def save_feedback_to_json(item_id, item_data):
    folder_path = f'db/{item_id}/'
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    file_path = f'{folder_path}item_{item_id}_feedback_data.json'

    with open(file_path, 'w') as json_file:
        json.dump(item_data, json_file, indent=2)

    print(f"Data saved to {file_path}")


def fetch_feedback_and_save(item_id):
    folder_path = f'db/{item_id}/'
    existing_file_path = f'{folder_path}item_{item_id}_feedback_data.json'
    if os.path.exists(existing_file_path):
        with open(existing_file_path, 'r') as existing_file:
            response = json.load(existing_file)
    else:
        response = make_feedback_http_request(item_id)
        # print(response)
        if response:
            save_feedback_to_json(item_id, response)
        else:
            raise Exception(f"Item with ID {item_id} not found.")
    return response


def add_to_map(d, key):
    if not key:
        return d
    d[key] = d[key] + 1 if key in d else 1
    return d


class Feedback:
    def __init__(self, item_id):
        self.item_id = item_id
        self.response = fetch_feedback_and_save(item_id)
        data = self.response.get('data', {})
        filter_info = data.get('filterInfo', {})
        filters = filter_info.get('filterStatistic', [])
        filters_map = {item["filterCode"]: item["filterCount"] for item in filters}
        statistics = data.get('productEvaluationStatistic', {})
        impression_list = data.get('impressionDTOList', [])
        feedback_list = data.get('evaViewList', [])

        self.total_reviews = data.get('totalNum', 0)
        self.item_stars = statistics.get('evarageStar', 0)

        self.filters_review = dict()
        for filter_code in FILTERS_REVIEW:
            self.filters_review[filter_code] = filters_map.get(filter_code, 0)

        self.stars_num_review = dict()
        for stars in STARTS_NUM_REVIEW:
            self.stars_num_review[stars] = statistics.get(stars, 0)

        self.stars_rate_review = dict()
        for stars in STARTS_RATE_REVIEW:
            self.stars_rate_review[stars] = statistics.get(stars, 0)

        self.impression = {item["content"]: item["num"] for item in impression_list}
        self.comments = [feedback.get('buyerTranslationFeedback', '') for feedback in feedback_list if feedback.get('buyerTranslationFeedback', '') != '']
        self.feedback_dates = dict()
        self.feedback_countries = dict()
        for feedback in feedback_list:
            self.feedback_dates = add_to_map(self.feedback_dates, feedback.get('evalDate', ''))
            self.feedback_countries = add_to_map(self.feedback_countries, feedback.get('buyerCountry', ''))

        self.feedback_dates = dict(sorted(self.feedback_dates.items(), key=lambda item: item[1], reverse=True))
        self.feedback_countries = dict(sorted(self.feedback_countries.items(), key=lambda item: item[1], reverse=True))

    def __str__(self):
        return f"total_reviews: {self.total_reviews}\n" \
               f"item_stars: {self.item_stars}\n" \
               f"filters_review: {self.filters_review}\n" \
               f"stars_num_review: {self.stars_num_review}\n" \
               f"stars_rate_review: {self.stars_rate_review}\n" \
               f"comments: {self.comments}\n" \
               f"feedback_dates: {self.feedback_dates}\n" \
               f"feedback_countries: {self.feedback_countries}\n" \
               f"impression: {self.impression}"
