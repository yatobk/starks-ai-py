class TokenCostCalculator:
    def __init__(self, model_price_input: float = 0.0015, model_price_output: float = 0.002):
        self.model_price_input = model_price_input
        self.model_price_output = model_price_output

    def input_cost(self, num_tokens: int) -> float:
        return self.model_price_input * (num_tokens / 1000)

    def output_cost(self, num_tokens: int) -> float:
        return self.model_price_output * (num_tokens / 1000)
