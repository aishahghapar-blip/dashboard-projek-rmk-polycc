import streamlit as st
import pandas as pd

# Tajuk Dashboard
st.title("DASHBOARD PROJEK PEMBANGUNAN POLYCC (RMK)")
st.subheader("Analisis dan Pemantauan Projek RMK10 hingga RMK13")

# Load data Excel
df = pd.read_excel("RMK11 & RMK12 & RMK13.xlsx")

# Sidebar Filter
st.sidebar.header("Tapis Data")

search = st.sidebar.text_input("Cari Projek")

negeri = st.sidebar.multiselect("Negeri", df['negeri'].unique())
institusi = st.sidebar.multiselect("Institusi", df['institusi'].unique())
jenis = st.sidebar.multiselect("Jenis Projek", df['jenis'].unique())
rmk = st.sidebar.multiselect("RMK", df['rmk'].unique())

# Filter Logic
if search:
    df = df[df['tajuk'].str.contains(search, case=False)]

if negeri:
    df = df[df['negeri'].isin(negeri)]

if institusi:
    df = df[df['institusi'].isin(institusi)]

if jenis:
    df = df[df['jenis'].isin(jenis)]

if rmk:
    df = df[df['rmk'].isin(rmk)]

# Ringkasan
st.subheader("Ringkasan")

col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Projek", len(df))
col2.metric("Bilangan Institusi", df['institusi'].nunique())
col3.metric("Bilangan Negeri", df['negeri'].nunique())

# Papar Data
st.subheader("Senarai Projek")
st.dataframe(df)

# Chart
st.subheader("Projek Mengikut Institusi")
st.bar_chart(df['institusi'].value_counts())
