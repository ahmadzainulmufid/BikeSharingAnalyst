import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
sns.set(style='darkgrid')

# Load data
all_df = pd.read_csv("./data/all_data.csv")
hour_df = pd.read_csv("./data/hour.csv")

# Preprocessing date
all_df['dteday'] = pd.to_datetime(all_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Sidebar
with st.sidebar:
    st.title("Bike Sharing Dashboard")
    st.image("dashboard/img_streamlit.png")

    min_date = all_df['dteday'].min().date()
    max_date = all_df['dteday'].max().date()

    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Filter data
filtered_df = all_df[(all_df['dteday'] >= pd.to_datetime(start_date)) & (all_df['dteday'] <= pd.to_datetime(end_date))]

# Main Title
st.header("Bike Sharing Analysis Dashboard")

# 1. Tren penyewaan sepeda harian
st.subheader("1. Tren Penyewaan Sepeda Harian")
st.line_chart(filtered_df.set_index('dteday')['cnt'])

# 2. Pengaruh Musim
st.subheader("2. Pengaruh Musim terhadap Penyewaan")
st.bar_chart(filtered_df.groupby('season')['cnt'].mean())

# 3. Hari Kerja vs Hari Libur
st.subheader("3. Hari Kerja vs Hari Libur")
st.bar_chart(filtered_df.groupby('workingday')['cnt'].mean())

# 4. Casual vs Registered
st.subheader("4. Pengguna Casual vs Registered")
st.bar_chart({
    'Casual': filtered_df['casual'].sum(),
    'Registered': filtered_df['registered'].sum()
})

# 5. Cuaca dan Kelembaban
st.subheader("5. Pengaruh Cuaca dan Kelembaban")
st.bar_chart(filtered_df.groupby('weathersit')['cnt'].mean())

# 6. Jam Paling Sibuk (from hour_df)
st.subheader("6. Jam Paling Sibuk")
st.line_chart(hour_df.groupby('hr')['cnt'].mean())

# 7. Weekday vs Weekend (pola jam)
st.subheader("7. Pola Jam Sibuk Weekday vs Weekend")
hour_df['is_weekend'] = hour_df['weekday'].isin([0, 6])
avg_hour = hour_df.groupby(['hr', 'is_weekend'])['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=avg_hour, x='hr', y='cnt', hue='is_weekend', ax=ax)
st.pyplot(fig)

# 8. Casual vs Registered per Jam
st.subheader("8. Casual vs Registered per Jam")
avg_casual_registered = hour_df.groupby('hr')[['casual', 'registered']].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=avg_casual_registered, x='hr', y='casual', label='Casual', ax=ax2)
sns.lineplot(data=avg_casual_registered, x='hr', y='registered', label='Registered', ax=ax2)
st.pyplot(fig2)

# 9. Humidity & Windspeed Effect
st.subheader("9. Pengaruh Kelembaban dan Angin terhadap Penyewaan")
fig3, ax3 = plt.subplots(1, 2, figsize=(14, 5))
sns.scatterplot(data=hour_df, x='hum', y='cnt', alpha=0.3, ax=ax3[0])
ax3[0].set_title("Humidity vs Count")
sns.scatterplot(data=hour_df, x='windspeed', y='cnt', alpha=0.3, ax=ax3[1])
ax3[1].set_title("Windspeed vs Count")
st.pyplot(fig3)

# 10. Hurricane Sandy Impact
st.subheader("10. Dampak Hurricane Sandy (30 Okt 2012)")
sandy_dates = ['2012-10-29', '2012-10-30', '2012-10-31']
sandy_plot = hour_df[hour_df['dteday'].isin(pd.to_datetime(sandy_dates))]
sandy_plot['event'] = sandy_plot['dteday'].astype(str)
fig4, ax4 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=sandy_plot, x='hr', y='cnt', hue='event', ax=ax4)
st.pyplot(fig4)
