from engines.engines import EngineRegistry


def combine_results(results):
    return all(results)


class EnginesChain:
    def __init__(self):
        self.engines = EngineRegistry.engines

    def add_engine(self, engine):
        self.engines.append(engine)

    def validate_item(self, item):
        results = [engine.validate(item) for engine in self.engines]
        final_result = combine_results(results)
        false_indicators = [engine.description for engine, result in zip(self.engines, results) if not result]
        return final_result, false_indicators
