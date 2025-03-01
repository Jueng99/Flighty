import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import sys

# 设置 Streamlit 页面信息
st.set_page_config(page_title="My Flighty")

st.markdown("# My Flight Record")

# **函数：读取 JSON 文件**
def from_data_file(filename):
    try:
        return pd.read_json(filename)
    except Exception as e:
        st.error(f"Error reading {filename}: {e}")
        return pd.DataFrame()

# **加载数据**
flight_data = from_data_file("flight_data.json")
airport_data = from_data_file("airport_name.json")

# **检查 flight_data 是否包含 "year" 列**
if "year" not in flight_data.columns:
    st.error("Error: flight_data.json must have a 'year' column.")
    st.stop()

# **获取所有年份，并转换为整数**
years = sorted({int(year) for year in flight_data["year"] if str(year).isdigit()}, reverse=True)

# **检查年份数据是否为空**
if not years:
    st.error("No available years in flight data.")
    st.stop()

# **选择年份**
selected_year = st.slider("Select Year", min_value=min(years), max_value=max(years), value=max(years))

# **复选框：是否查看所有年份**
show_all_years = st.checkbox("Show All Years", False)

# **过滤航班数据**
if show_all_years:
    filtered_flight_data = flight_data
else:
    filtered_flight_data = flight_data[flight_data["year"] == selected_year]

# **如果没有航班数据，显示警告**
if filtered_flight_data.empty:
    st.warning(f"No flight data available for year {selected_year}.")
    filtered_airport_data = pd.DataFrame()
else:
    # **获取所有涉及机场的经纬度**
    departure_coords = set(zip(filtered_flight_data["departure_lon"], filtered_flight_data["departure_lat"]))
    arrival_coords = set(zip(filtered_flight_data["arrival_lon"], filtered_flight_data["arrival_lat"]))

    # **筛选出与航班匹配的机场**
    filtered_airport_data = airport_data[
        airport_data.apply(lambda row: (row["lon"], row["lat"]) in departure_coords or 
                                         (row["lon"], row["lat"]) in arrival_coords, axis=1)
    ]

# **定义地图图层**
ALL_LAYERS = {
    "Flight Paths": pdk.Layer(
        "ArcLayer",
        data=filtered_flight_data,
        get_source_position=["departure_lon", "departure_lat"],
        get_target_position=["arrival_lon", "arrival_lat"],
        get_source_color=[0, 128, 255, 160],  # 蓝色
        get_target_color=[255, 0, 0, 160],    # 红色
        auto_highlight=True,
        width_scale=0.0001,
        get_width=5,
        width_min_pixels=2,
        width_max_pixels=10,
    ),
    "Airport": pdk.Layer(
        "TextLayer",
        data=filtered_airport_data,
        get_position=["lon", "lat"],
        get_text="name",
        get_color=[255, 255, 255, 200],
        get_size=15,
        get_alignment_baseline="'bottom'",
        get_text_anchor="'end'",
    ),
}

# **侧边栏：选择显示的图层**
st.sidebar.markdown("### Map Layers")
selected_layers = [
    layer for layer_name, layer in ALL_LAYERS.items() if st.sidebar.checkbox(layer_name, True)
]

# **显示地图**
if selected_layers:
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v11",
            initial_view_state={
                "latitude": 20,
                "longitude": 110,
                "zoom": 3,
                "pitch": 50,
            },
            layers=selected_layers,
        )
    )
else:
    st.error("Please choose at least one layer above.")

# **读取 JSON 文件以展示航班信息**
with open('flight_data.json', 'r') as f:
    flights_data = json.load(f)

# **航班信息展示**
st.markdown("## Flight Information")
col1 = st.columns(1, vertical_alignment="center", border=True)[0]

with col1:
    for flight in flights_data:
        # **按年份筛选航班**
        if not show_all_years and int(flight["year"]) != selected_year:
            continue

        # **创建两列**
        sub_col1 = st.columns(1, border=True) [0]

        # **出发信息**
        with sub_col1:
            st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; width: 100%;">
                        <div>{flight['date']}</div>
                        <div>{flight['airline']} {flight['flight_number']}</div>
                        </div>
                        """, unsafe_allow_html=True)
            st.markdown(
                        f"<div style='text-align: left; font-size: 40px; font-weight: bold;'>"
                        f"{flight['departure_airport']} ➝ {flight['arrival_airport']}</div>",
                        unsafe_allow_html=True)
            st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; width: 100%;">
                        <div>{flight['departure_city']} → {flight['arrival_city']}</div>
                        <div>{flight['plane_mode']}</div>
                        </div>
                        """, unsafe_allow_html=True)
            st.write(" ")