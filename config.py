import dataclasses

vel_small = 1
vel_medium = 3
vel_large = 6

period_small = 1
period_medium = 3
period_large = 6

capacity_small = 25
capacity_medium = 100
capacity_large = 400

km_price_small = 1
km_price_medium = 5
km_price_large = 12


@dataclasses.dataclass
class Info:
    vel: float
    period: float
    capacity: float
    km_price: float


type_info = {0: Info(vel_small, period_small, capacity_small, km_price_small),
             1: Info(vel_medium, period_medium, capacity_medium, km_price_medium),
             2: Info(vel_large, period_large, capacity_large, km_price_large)}

k_shortest = 20
