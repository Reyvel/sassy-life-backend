RISK_BY_TIME = {
    0: 30,
    1: 10,
    2: 15,
    3: 20,
    4: 5,
    5: 5,
    6: 25,
    7: 100,
    8: 145,
    9: 80,
    10: 100,
    11: 95,
    12: 95,
    13: 120,
    14: 130,
    15: 140,
    16: 150,
    17: 225,
    18: 150,
    19: 100,
    20: 120,
    21: 80,
    22: 60,
}

TOTAL_RISK_BY_TIME = sum(RISK_BY_TIME.keys())
FATALITY_COST = 30000
INJURY_COST = 150000
FIX_COST = 50000


def risk_by_distance(dist, age):
    if age < 25:
        return 1/((1/500 + 1/25) * dist) + 4
    elif age < 36:
        return 1(1/160 * dist)
    elif age < 65:
        return 1/(1/60 * dist)
    else:
        return 1/(1/20 * dist)

for hour, n_accidents in RISK_BY_TIME.items():
    RISK_BY_TIME[hour] /= TOTAL_RISK_BY_TIME

def risk_by_time(now):
    return RISK_BY_TIME[now.hour]

def treatment_cost(speed,
                   fatality_cost=FATALITY_COST,
                   injury_cost=INJURY_COST,
                   fix_cost=FIX_COST):
    if speed < 21:
        return (4 * fatality_cost + 39 * injury_cost + 229 * fix_cost) / 229
    elif speed < 40:
        return (22 * fatality_cost + 182 * injury_cost + 788 * fix_cost) / 788
    elif speed < 60:
        return (28 * fatality_cost + 165 * injury_cost + 611 * fix_cost) / 611
    elif speed < 80:
        return (17 * fatality_cost + 71 * injury_cost + 209 * fix_cost) / 209
    else:
        return (5 * fatality_cost + 17 * injury_cost + 52 * fix_cost) / 52


def calculate_point(now, speed, dist, age):
    utpc = 10**6 / risk_by_distance(dist, age) / dist
    cput = 1 / utpc
    tc = treatment_cost(speed)
    dpdkt = tc * cput
    dpt = dpdkt * (1 - risk_by_time(dist, age))

    return int(dpt)
