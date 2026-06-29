from datetime import date
from datetime import datetime

from options import *
from durations import *

def calculate_age(birthdate_string):
    """function to calculate age from birthdate string in the format 'dd-mm-yyyy'"""
    birthdate = datetime.strptime(birthdate_string, "%d-%m-%Y").date()
    today = date.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age

def get_premium(plan_type, region=None, category=None, days=None):
    # --- Travel Protect ---
    if plan_type == "Travel Protect":
        durations = list(durations_travelprotect_map.values())
        if region in options_travelprotect["Travel Protect Plans"]:
            if region == "Worldwide":
                premiums = options_travelprotect["Travel Protect Plans"][region][category[0]][category[1]]
            else:
                premiums = options_travelprotect["Travel Protect Plans"][region][category]
            for max_days, price in zip(durations, premiums):
                if days <= max_days:
                    return price
    # --- Student Plan ---
    elif plan_type == "Student Plan":
        durations = list(durations_studentplan_map.values())
        premiums = options_studentplans[category]
        for max_days, price in zip(durations, premiums):
            if days <= max_days:
                return price
    # --- Inbound Travel ---
    elif plan_type == "Inbound Travel":
        for label, (low, high) in durations_inboundtravel_map.items():
            if low <= days <= high:
                idx = list(durations_inboundtravel_map.keys()).index(label)
                return options_inboundtravel["Premium"][idx]
    # --- Domestic Travel ---
    elif plan_type == "Domestic Travel":
        for label, (low, high) in durations_domestictravel_map.items():
            if low <= days <= high:
                idx = list(durations_domestictravel_map.keys()).index(label)
                return options_domestictravel["Individual per day"][idx]
    # --- Pilgrimage Travel ---
    elif plan_type == "Pilgrimage Travel":
        durations = [7, 15, 21]
        premiums = options_pilgrimagetravel[category]
        for max_days, price in zip(durations, premiums):
            if days <= max_days:
                return price
    # --- Corporate ---
    elif plan_type == "Corporate":
        return dict(zip(["Base", "Total"], options_corporate[category]))
    return None

def adjust_premium_for_age(base_premium, age, plan_type=None, region=None):
    """
    Adjusts premium based on age rules.
    Works for both numeric premiums and dicts (Corporate).
    """
    def apply_factor(premium, factor):
        return premium * factor

    # Rule: 3 months – 18 years → 50% reduction
    if 0.25 <= age <= 18:
        factor = 0.5

    # Rule: 66 – 75 years → 50% increase
    elif 66 <= age <= 75:
        factor = 1.5

    # Rule: 76 – 80 years → 100% increase
    elif 76 <= age <= 80:
        factor = 2.0

    # Rule: 81+ years → only Europe/Schengen, 300% increase
    elif age >= 81:
        if plan_type == "Travel Protect" and region == "Europe":
            factor = 4.0   # base + 300% increase
        else:
            return None    # not eligible for other plans/regions

    else:
        factor = 1.0  # default

    # Handle Corporate dict case
    if isinstance(base_premium, dict):
        return {k: apply_factor(v, factor) for k, v in base_premium.items()}
    else:
        return apply_factor(base_premium, factor)
