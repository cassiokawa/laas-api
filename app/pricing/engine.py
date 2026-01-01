import math
from dataclasses import dataclass

@dataclass
class PricingEngine:
    # knobs you can evolve later into learned models
    peak_multiplier: float = 1.15
    vip_discount: float = 0.95
    floor: int = 1

    def quote_burn_price(self, user_id: str, reward_id: str, list_price_points: int) -> int:
        # placeholder segmentation (swap to real features later)
        is_vip = user_id.endswith("VIP")
        m = self.peak_multiplier * (self.vip_discount if is_vip else 1.0)

        price = math.ceil(list_price_points * m)
        return max(self.floor, price)
