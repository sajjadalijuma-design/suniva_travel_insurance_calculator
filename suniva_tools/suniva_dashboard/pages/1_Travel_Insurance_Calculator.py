import streamlit as st
from datetime import date

from functions import *

# Initialize login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Initialize username
if "username" not in st.session_state:
    st.session_state.username = ""


if st.session_state.logged_in == False:
    st.write("Please log in to access the calculator.")

else:
    st.title("Travel Insurance Premium Calculator")

    plan_type = st.selectbox("Select Plan Type", 
        ["Travel Protect", "Student Plan", "Inbound Travel", "Domestic Travel", "Pilgrimage Travel", "Corporate"])

    region, category = None, None

    input_age = st.date_input("Enter Birthdate", date.today(), min_value=date(1900, 1, 1), max_value=date.today())
    birthdate_string = input_age.strftime("%d-%m-%Y")
    age = calculate_age(birthdate_string)


    if plan_type == "Travel Protect":
        region = st.selectbox("Select Region", list(options_travelprotect["Travel Protect Plans"].keys()))
        if region == "Worldwide":
            category = (st.selectbox("Select Person Type", ["Individual", "Family"]),
                        st.selectbox("Select Coverage", ["Basic", "Plus", "Extra"]))
        else:
            category = st.selectbox("Select Category", list(options_travelprotect["Travel Protect Plans"][region].keys()))

    elif plan_type == "Student Plan":
        category = st.selectbox("Select Category", list(options_studentplans.keys()))

    elif plan_type == "Pilgrimage Travel":
        category = st.selectbox("Select Category", list(options_pilgrimagetravel.keys()))

    elif plan_type == "Corporate":
        category = st.selectbox("Select Category", list(options_corporate.keys()))

    days = st.number_input("Enter number of days", min_value=1, step=1)

    if st.button("Calculate Premium"):
        premium = get_premium(plan_type, region, category, days)
        
        if category == "Family":
            if isinstance(premium, dict):  # Corporate case
                    st.success(f"{plan_type} → {category}")
                    st.success(f"Base Premium (Family): TZS {premium['Base']:,.2f}\n")
            else:
                st.success(f"{plan_type} → {region or ''} {category or ''}\n")
                st.success(f"Duration: {days} days\nAge: {age}\n")
                st.success(f"Base Premium (Family): TZS {premium:,.2f}")      

        elif category == "Individual":
            adjusted_premium = adjust_premium_for_age(premium, age, plan_type, region)
            if adjusted_premium is None:
                st.error("For persons aged 81+, only Europe/Schengen policy is available.")
            else:
                if isinstance(adjusted_premium, dict):  # Corporate case
                    st.success(f"{plan_type} → {category}")
                    st.success(f"Base Premium: TZS {adjusted_premium['Base']:,.2f}\n")
                    st.success(f"Total Premium adjusted according to age: TZS {adjusted_premium['Total']:,.2f}\n")
                    st.success(f"Age: {age}")
                else:
                    st.success(f"{plan_type} → {region or ''} {category or ''}\n")
                    st.success(f"Duration: {days} days\nAge: {age}\n")
                    st.success(f"Total Premium adjusted according to age: TZS {adjusted_premium:,.2f}")
        else:
            st.error("No premium found for the given input.")
