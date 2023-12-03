class EngineRegistry:
    engines = []

    @classmethod
    def register_engine(cls, engine_class):
        cls.engines.append(engine_class())
        return engine_class


class EngineTemplate:
    description = "No description provided."

    def validate(self, item):
        raise NotImplementedError("Subclasses must implement the validate method")


def get_sold_count(item):
    sold_count = item.general_info.sold_count
    if sold_count.endswith("+"):
        sold_count = sold_count[:-1]
    sold_count = sold_count.replace(",", "")
    return int(sold_count)


def get_total_reviews(item):
    return int(item.item_feedback.total_reviews)


@EngineRegistry.register_engine
class Engine1(EngineTemplate):
    description = "sold > 100 and reviews < 10 = False"

    def validate(self, item):
        sold_count = get_sold_count(item)
        total_reviews = get_total_reviews(item)
        if sold_count > 100 and total_reviews < 10:
            return False
        return True


@EngineRegistry.register_engine
class Engine2(EngineTemplate):
    description = "reviews > 10 and dates <= 3 = False"

    def validate(self, item):
        total_reviews = get_total_reviews(item)
        dates_count = len(item.item_feedback.feedback_dates)
        if total_reviews > 10 and dates_count <= 3:
            return False
        return True


@EngineRegistry.register_engine
class Engine3(EngineTemplate):
    description = "reviews > 10 and countries <= 2 = False"

    def validate(self, item):
        total_reviews = get_total_reviews(item)
        countries_count = len(item.item_feedback.feedback_countries)
        if total_reviews > 10 and countries_count <= 2:
            return False
        return True


@EngineRegistry.register_engine
class Engine4(EngineTemplate):
    description = "sellerPositiveNum < 101 = False"

    def validate(self, item):
        seller_positive_num = int(item.general_info.store_feedback['sellerPositiveNum'])
        if seller_positive_num < 101:
            return False
        return True


@EngineRegistry.register_engine
class Engine5(EngineTemplate):
    description = "sellerPositiveRate < 90 = False"

    def validate(self, item):
        seller_positive_rate = float(item.general_info.store_feedback['sellerPositiveRate'])
        if seller_positive_rate < 90:
            return False
        return True


@EngineRegistry.register_engine
class Engine6(EngineTemplate):
    description = "fiveStarNum < 10 = False"

    def validate(self, item):
        five_star_num = float(item.item_feedback.stars_num_review['fiveStarNum'])
        if five_star_num < 10:
            return False
        return True


@EngineRegistry.register_engine
class Engine7(EngineTemplate):
    description = "item_stars <= 3.5 = False"

    def validate(self, item):
        item_stars = float(item.item_feedback.item_stars)
        if item_stars <= 3.5:
            return False
        return True


@EngineRegistry.register_engine
class Engine8(EngineTemplate):
    description = "reviews > 10 and comments = [] = False"

    def validate(self, item):
        total_reviews = get_total_reviews(item)
        comments_count = len(item.item_feedback.comments)
        if total_reviews > 10 and comments_count == 0:
            return False
        return True


@EngineRegistry.register_engine
class Engine8(EngineTemplate):
    description = "reviews == 0 = False"

    def validate(self, item):
        total_reviews = get_total_reviews(item)
        if total_reviews == 0:
            return False
        return True
