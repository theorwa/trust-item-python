from feedback import Feedback
from general import General


class Item:
    def __init__(self, item_id):
        self.item_id = item_id
        self.general_info = General(item_id)
        self.item_feedback = Feedback(item_id)

    def __str__(self):
        return f'\n>> Item Id: {self.item_id}\n' \
               f'Sold Count: {self.general_info.sold_count}\n' \
               f'Stars: {self.item_feedback.item_stars}/5.0\n' \
               f'Reviews: {self.item_feedback.total_reviews}\n' \
               f'\n>> Seller:\n' \
               f'Store: {self.general_info.seller_info["storeName"]}\n' \
               f'Rate: {self.general_info.store_feedback["sellerPositiveRate"]}/100\n' \
               f'Positive Feedbacks: {self.general_info.store_feedback["sellerPositiveNum"]}\n' \
               f'Opened Before: {self.general_info.seller_info["openedYear"]} Years\n' \
               f'Top Seller ? {self.general_info.seller_info["topRatedSeller"]}\n'
