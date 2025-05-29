import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

st.set_page_config(page_title="도시 침수 예경보 모델", layout="wide")

st.title("도시 침수 예경보 모델")

# 현재 작업 디렉토리 및 파일 목록 출력 (디버그용)
st.write("현재 작업 디렉토리:", os.getcwd())
st.write("현재 폴더 내 파일 목록:", os.listdir())

# 변경된 엑셀 파일명
excel_file = "gangnam_flood_analysis.xlsx"

# 절대 경로 확인 및 존재 여부 출력
excel_path = os.path.abspath(excel_file)
st.write("절대 경로:", excel_path)
st.write("파일 존재 여부:", os.path.isfile(excel_path))

if not os.path.isfile(excel_file):
    st.error(f"❌ 기본 예제 파일도 존재하지 않습니다. '{excel_file}' 파일을 업로드해주세요.")
    st.stop()

# 엑셀 파일 읽기
df = pd.read_excel(excel_file, engine="openpyxl")

# 컬럼명 공백 제거
df.columns = df.columns.str.strip()

st.write("업로드된 엑셀 파일 컬럼명:")
st.write(df.columns.tolist())

# 필요한 컬럼 체크
required_cols = ['위도', '경도', 'cluster', '감성분류', 'risk_level', '내용']
missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"데이터에 다음 컬럼이 없습니다: {missing_cols} 엑셀 파일 컬럼명을 확인해주세요.")
    st.stop()

# 지도 생성
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

st_folium(m, width=700, height=500)
