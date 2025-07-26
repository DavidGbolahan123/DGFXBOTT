import pandas as pd

def get_support_resistance_levels(data):
    support_levels = []
    resistance_levels = []
    
    for i in range(2, len(data)-2):
        # Support
        if data['low'][i] < data['low'][i-1] and data['low'][i] < data['low'][i+1] and \
           data['low'][i+1] < data['low'][i+2] and data['low'][i-1] < data['low'][i-2]:
            support_levels.append((i, data['low'][i]))
        # Resistance
        if data['high'][i] > data['high'][i-1] and data['high'][i] > data['high'][i+1] and \
           data['high'][i+1] > data['high'][i+2] and data['high'][i-1] > data['high'][i-2]:
            resistance_levels.append((i, data['high'][i]))

    return support_levels, resistance_levels


def is_near_support_or_resistance(price, support_levels, resistance_levels, threshold=0.001):
    for _, level in support_levels:
        if abs(price - level) / price < threshold:
            return "support"
    for _, level in resistance_levels:
        if abs(price - level) / price < threshold:
            return "resistance"
    return None
