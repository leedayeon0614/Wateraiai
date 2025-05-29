import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ✅ 반드시 가장 위에 작성
st.set_page_config(page_title="도시 침수 예경보 모델", layout="wide")

# 🚀 제목 표시
st.title("📊 도시 침수 예경보 시각화")

# ✅ 엑셀 파일 업로드
uploaded_file = st.file_uploader("📤 엑셀 파일 업로드 (.xlsx)", type=["xlsx"])

# ✅ 파일 불러오기: 업로드된 파일 또는 기본 파일
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    st.success("✅ 업로드한 파일을 불러왔습니다.")
else:
    try:
        df = pd.read_excel("강남침수_감성분석_결과.xlsx", engine="openpyxl")
        st.warning("⚠️ 업로드된 파일이 없어서 기본 예제 파일을 불러왔습니다.")
    except FileNotFoundError:
        st.error("❌ 기본 예제 파일도 존재하지 않습니다. 엑셀 파일을 업로드해주세요.")
        st.stop()

# ✅ 컬럼 확인 및 기본 전처리
df.columns = df.columns.str.strip()
required_columns = ['위도', '경도', 'cluster', '감성분류', 'risk_level', '내용']
missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.error(f"❌ 데이터에 다음 컬럼이 없습니다: {missing_cols}\n엑셀 파일의 컬럼명을 확인해주세요.")
    st.stop()

# ✅ 지도 그리기
st.subheader("🗺️ 지도 시각화")

m = folium.Map(location=[37.4979, 127.0276], zoom_start=13)

cluster_colors = {0: 'blue', 1: 'green', 2: 'purple'}

for _, row in df.dropna(subset=['cluster', '위도', '경도']).iterrows():
    popup_text = (
        f"<b>📌 클러스터:</b> {row['cluster']}<br>"
        f"<b>🧠 감성 분류:</b> {row['감성분류']}<br>"
        f"<b>⚠️ 위험도:</b> {row['risk_level']}단계<br><br>"
        f"<b>📝 내용:</b> {row['내용'][:60]}..."
    )
    folium.CircleMarker(
        location=[row['위도'], row['경도']],
        radius=6,
        color=cluster_colors.get(int(row['cluster']), 'gray'),
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=f"Cluster {row['cluster']} / 위험도 {row['risk_level']}"
    ).add_to(m)

st_data = st_folium(m, width=900)

# ✅ 데이터 미리보기
st.subheader("🔍 데이터 미리보기")
st.dataframe(df.head())
