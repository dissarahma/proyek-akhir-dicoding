import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_count_by_hour_df(hour_df):
  hour_count_df =  hour_df.groupby(by="hours").agg({"count_column": ["sum"]})
  return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('date >= "2011-01-01" and date < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="date").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df

def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="date").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order (hour_df):
    sum_order_items_df = hour_df.groupby("hours").count_column.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season (day_df):
    season_df = day_df.groupby(by="season").count_column.sum().reset_index()
    return season_df

def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_situation').agg({
        'count_column': 'sum'
    })
    return weather_rent_df

day_df = pd.read_csv("day_df.csv")
hours_df = pd.read_csv("hour_df.csv")

datetime_columns = ["date"]
day_df.sort_values(by="date", inplace=True)
day_df.reset_index(inplace=True)

hours_df.sort_values(by="date", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = day_df["date"].min()
max_date_days = day_df["date"].max()

min_date_hour = hours_df["date"].min()
max_date_hour = hours_df["date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")

        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])

main_df_days = day_df[(day_df["date"] >= str(start_date)) &
                       (day_df["date"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["date"] >= str(start_date)) &
                        (hours_df["date"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header(':sparkles: Bike-Sharing Dashboard :sparkles:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = day_df_count_2011.count_column.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("Tren penyewaan sepeda dalam beberapa tahun terakhir")

fig, ax = plt.subplots(figsize=(16, 10))
ax.plot(
    day_df["date"],
    day_df["count_column"],
    marker='o', 
    linewidth=2,
    color="#FFC0CB"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


st.subheader("Perbandingan antara Penyewa Registered dengan Penyewa Casual")

labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#D3D3D3", "#90CAF9"],
        shadow=True, startangle=90)
ax1.axis('equal')

st.pyplot(fig1)

weather_rent_df = create_weather_rent_df(day_df)
st.subheader("Penyewaan Sepeda berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(16, 8))

colors=["tab:blue", "tab:orange", "tab:green"]

sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df['count_column'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(weather_rent_df['count_column']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)
