import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import plotly.express as px # type: ignore

# 读取 JSON 数据
try:
    with open("flight_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except Exception as e:
    st.error(f"Error reading JSON file: {e}")
    st.stop()

# 转换为 DataFrame
df = pd.DataFrame(data)

# 确保数据非空
if df.empty:
    st.error("Flight data is empty!")
    st.stop()

# 确保所需列存在
required_columns = {'departure_city', 'arrival_city', 'airline', 'departure_airport', 'arrival_airport', 'date'}
if not required_columns.issubset(df.columns):
    st.error(f"Missing required columns: {required_columns - set(df.columns)}")
    st.stop()

# 计算数据
total_flights = len(df)

# 将 flight_date 转换为日期格式，提取年份
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year

# 统计每年的飞行次数
flights_per_year = df['year'].value_counts().sort_index(ascending=True)

# 统计访问过的城市（起飞 + 到达），确保排序正确
city_counts = pd.concat([df['departure_city'], df['arrival_city']]).value_counts().astype(int)
top_cities = city_counts.sort_values(ascending=False).head(5)  # 取前 5，确保排序

# 统计访问过的机场（起飞 + 到达），确保排序正确
airport_counts = pd.concat([df['departure_airport'], df['arrival_airport']]).value_counts().astype(int)
top_airports = airport_counts.sort_values(ascending=False).head(5)  # 取前 5，确保排序

# 统计前 5 航空公司
top_airlines = df['airline'].value_counts().sort_values(ascending=False).head(5).astype(int)

# 统计唯一访问的城市数量
unique_cities = len(city_counts)

# Streamlit UI
st.title("Statistics")

# 显示统计数据
col1, col2 = st.columns(2,border=True)
with col1:
    st.metric(label="Total Flights", value=total_flights)
    
with col2:
    st.metric(label="Total Cities Visited", value=unique_cities)

# 读取 flight_data.json 文件
with open('flight_data.json', 'r') as f:
    flight_data = json.load(f)

# 将数据转换为 DataFrame
flights_df = pd.DataFrame(flight_data)

# 将 'year' 列转换为整数类型，以确保数据正确处理
flights_df['year'] = pd.to_numeric(flights_df['year'], errors='coerce')

# Flights Per Year 图表
flights_per_year = flights_df.groupby('year').size()

# 使用 Plotly 生成 Flights Per Year 图表
st.subheader("Flights Per Year")
fig1 = px.bar(flights_per_year, x=flights_per_year.index, y=flights_per_year.values, 
              labels={'x': 'Year', 'y': 'Flight Count'}, 
              color=flights_per_year.index, color_continuous_scale='Viridis')

col3 = st.columns (1,border=True)[0]

with col3 :
    st.plotly_chart(fig1)

# Top 5 Airlines Used 图表
top_airlines = flights_df['airline'].value_counts().head(5)

# 使用 Plotly 生成 Top 5 Airlines Used 图表
st.subheader("Top 5 Airlines Used")
fig2 = px.bar(top_airlines, x=top_airlines.index, y=top_airlines.values, 
              labels={'x': 'Airline', 'y': 'Flight Count'}, 
              color=top_airlines.index, color_continuous_scale='Blues')

col4 = st.columns (1,border=True)[0]

with col4 :
    st.plotly_chart(fig2)

# Top Cities Visited (Departure + Arrival) - Treemapping
st.subheader("Cities Visited")
city_data = city_counts.reset_index()
city_data.columns = ['City', 'Visit Count']

# 创建 treemap，使用 color 参数来表示渐变颜色，但不显示 Visit Count
fig = px.treemap(city_data, 
                 path=['City'], 
                 values='Visit Count', 
                 color='Visit Count', 
                 color_continuous_scale='Viridis',  # 设置渐变颜色
                 hover_data={'City': True},  # 显示城市名
                 )

# 显示treemap图表
col5 = st.columns (1,border=True)[0]

with col5 :
    st.plotly_chart(fig)




