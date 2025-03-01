import streamlit as st
import json

st.markdown("# Add New Flight")

with st.form("add_flight_form"):
    date = st.text_input("Date (YYYY-MM-DD)")
    year = st.number_input("Year", min_value=1900, max_value=2100, value=2025)
    airline = st.text_input("Airline")
    flight_number = st.text_input("Flight Number")

    departure_airport = st.text_input("Departure Airport Code")
    departure_city = st.text_input("Departure City")
    departure_lat = st.number_input("Departure Latitude", format="%.6f")
    departure_lon = st.number_input("Departure Longitude", format="%.6f")

    arrival_airport = st.text_input("Arrival Airport Code")
    arrival_city = st.text_input("Arrival City")
    arrival_lat = st.number_input("Arrival Latitude", format="%.6f")
    arrival_lon = st.number_input("Arrival Longitude", format="%.6f")

    plane_mode = st.text_input("Aircraft Model")

    submitted = st.form_submit_button("Add Flight")

    if submitted:
        new_flight = {
            "date": date,
            "year": int(year),
            "airline": airline,
            "flight_number": flight_number,
            "departure_airport": departure_airport,
            "departure_city": departure_city,
            "departure_lat": float(departure_lat),
            "departure_lon": float(departure_lon),
            "arrival_airport": arrival_airport,
            "arrival_city": arrival_city,
            "arrival_lat": float(arrival_lat),
            "arrival_lon": float(arrival_lon),
            "plane_mode": plane_mode
        }

        # **1. 读取 flight_data.json**
        try:
            with open("flight_data.json", "r", encoding="utf-8") as file:
                flight_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            flight_data = []

        flight_data.append(new_flight)

        # **2. 读取 airport_name.json**
        try:
            with open("airport_name.json", "r", encoding="utf-8") as file:
                airport_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            airport_data = []

        # **3. 检查并添加新的机场数据**
        existing_airports = {(airport["lon"], airport["lat"]) for airport in airport_data}

        departure_entry = {
            "lon": float(departure_lon),
            "lat": float(departure_lat),
            "name": f"({departure_airport},{departure_city})"
        }
        arrival_entry = {
            "lon": float(arrival_lon),
            "lat": float(arrival_lat),
            "name": f"({arrival_airport},{arrival_city})"
        }

        if (departure_entry["lon"], departure_entry["lat"]) not in existing_airports:
            airport_data.append(departure_entry)

        if (arrival_entry["lon"], arrival_entry["lat"]) not in existing_airports:
            airport_data.append(arrival_entry)

        # **4. 保存更新后的数据**
        try:
            with open("flight_data.json", "w", encoding="utf-8") as file:
                json.dump(flight_data, file, indent=4)

            with open("airport_name.json", "w", encoding="utf-8") as file:
                json.dump(airport_data, file, indent=4)

            st.success("✅ Flight and airport data added successfully! Please refresh the page to see the update.")

        except Exception as e:
            st.error(f"Failed to save flight or airport data: {e}")
