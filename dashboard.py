import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style="dark")


def create_Q1_df(df):
    Q1_df = (
        df.groupby("product_category_name_english")
        .payment_value.sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return Q1_df


def create_Q1_df(df):
    Q1_df = (
        df.groupby("product_category_name_english_y")
        .agg({"payment_value": "sum"})
        .reset_index()
    )

    # Sort the DataFrame by payment_value in descending order
    Q1_df = Q1_df.sort_values(by="payment_value", ascending=False)

    return Q1_df


def create_Q2_df(df):
    Q2_df = (
        df.groupby("customer_city")
        .order_item_id.sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return Q2_df


all_df = pd.read_csv("all_df.csv")
datetime_columns = ["order_purchase_timestamp_y", "order_delivered_customer_date_y"]
all_df.sort_values(by="order_purchase_timestamp_y", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# membuat komponen filter

min_date = all_df["order_purchase_timestamp_y"].min()
max_date = all_df["order_purchase_timestamp_y"].max()

# ...
with st.sidebar:
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

main_df = all_df
selected_data = (all_df["order_purchase_timestamp_y"] >= str(start_date)) & (
    all_df["order_purchase_timestamp_y"] <= str(end_date)
)

Q1_df = create_Q1_df(main_df)
Q2_df = create_Q2_df(main_df)


# Visualisasi Data
st.header(":sparkles: E-Commerce Report Dashboard :sparkles:")

st.subheader("Produk dengan pembelian tertinggi dan terrendah sesuai jumlah pembayaran")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="payment_value",
    y="product_category_name_english_y",
    data=Q1_df.head(5),
    palette=colors,
    ax=ax[0],
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Produk dengan pembelian tertinggi", loc="center", fontsize=15)
ax[0].tick_params(axis="y", labelsize=12)

sns.barplot(
    x="payment_value",
    y="product_category_name_english_y",
    data=Q1_df.sort_values(by="payment_value", ascending=True).head(5),
    palette=colors,
    ax=ax[1],
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk dengan pembelian terrendah", loc="center", fontsize=15)
ax[1].tick_params(axis="y", labelsize=12)
st.pyplot(fig)


st.subheader("Penjualan Terbanyak Berdasarkan Kota (Top 10)")

# Mengambil 10 data tertinggi
top_10_cities = Q2_df.sort_values(by="order_item_id", ascending=False).head(10)


plt.figure(figsize=(10, 5))
colors_ = [
    "#72BCD4",
    "#D3D3D3",
    "#D3D3D3",
    "#D3D3D3",
    "#D3D3D3",
    "#D3D3D3",
    "#D3D3D3",
    "#D3D3D3",
    "#D3D3D3",
    "#D3D3D3",
]

sns.barplot(x="order_item_id", y="customer_city", data=top_10_cities, palette=colors_)

st.set_option("deprecation.showPyplotGlobalUse", False)
st.pyplot()
