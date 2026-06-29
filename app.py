import streamlit as st
import pandas as pd

# Tajuk Dashboard
st.title("DASHBOARD PROJEK PEMBANGUNAN POLYCC (RMK)")
st.subheader("Analisis dan Pemantauan Projek RMK11 hingga RMK13")

# Load semua sheet (tab)
all_sheets = pd.read_excel("RMK11 & RMK12 & RMK13.xlsx", sheet_name=None)

df_list = []

for name, data in all_sheets.items():
    data['rp'] = name  # ambil nama tab (RP1 2016 dll)
    df_list.append(data)

df = pd.concat(df_list, ignore_index=True)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Rename columns ikut Excel awak
df = df.rename(columns={
    'kod projek': 'kod_projek',
    'nama projek': 'tajuk',
    'skop': 'skop',
    'kos keseluruhan': 'kos',
    'jenis kategori projek': 'jenis',
    'institusi/ bahagian': 'institusi',
    'negeri': 'negeri',
    'rmk': 'rmk'
})

# Clean & standardize Jenis Projek
df['jenis'] = df['jenis'].str.replace(r'\s*-\s*', ' - ', regex=True)
df['jenis'] = df['jenis'].str.strip()

# Fix typo & consistency
df['jenis'] = df['jenis'].str.replace(r'\.+', '', regex=True)

df['jenis'] = df['jenis'].replace({
    'Fizikal - Kelengkapan/ Pera laten': 'Fizikal - Kelengkapan/Peralatan',
    'Fizikal - Kelengkapan/ Peralatan': 'Fizikal - Kelengkapan/Peralatan',
    'Fizikal - Kelengkapan / Peralatan': 'Fizikal - Kelengkapan/Peralatan'
})

# Remove titik pelik
df['jenis'] = df['jenis'].str.replace(r'\.', '', regex=True)

# Betulkan spacing
df['jenis'] = df['jenis'].str.replace(r'\s*-\s*', ' - ', regex=True)

# Buang space extra
df['jenis'] = df['jenis'].str.strip()

df['tahun'] = df['rp'].str.extract(r'(\d{4})')

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

import matplotlib.pyplot as plt

# PIE CHART RMK
st.subheader("Peratusan Projek Mengikut RMK")

if not df.empty:
    rmk_count = df['rmk'].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(rmk_count, labels=rmk_count.index, autopct='%1.1f%%')
    ax1.axis('equal')

    st.pyplot(fig1)

# PIE CHART RP
st.subheader("Peratusan Projek Mengikut RP")

if not df.empty:
    rp_count = df['rp'].value_counts()

    fig2, ax2 = plt.subplots()
    ax2.pie(rp_count, labels=rp_count.index, autopct='%1.1f%%')
    ax2.axis('equal')

    st.pyplot(fig2)

st.subheader("Ringkasan")

col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Projek", len(df))
col2.metric("Jumlah Institusi", df['institusi'].nunique())
col3.metric("Jumlah Negeri", df['negeri'].nunique())

# Clean kos dulu
df['kos'] = df['kos'].astype(str).str.replace('[RM,]', '', regex=True)
df['kos'] = pd.to_numeric(df['kos'], errors='coerce')

total_kos = df['kos'].sum()

st.metric("Jumlah Kos Keseluruhan", f"RM {total_kos:,.0f}")

st.subheader("Top 10 Institusi Projek")

top_inst = df['institusi'].value_counts().head(10)
st.bar_chart(top_inst)

st.subheader("Trend Projek Mengikut Tahun")

trend = df['tahun'].value_counts().sort_index()
st.line_chart(trend)
