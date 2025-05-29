import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="감성 위험도 지도", layout="wide")
st.title("도시 침수 예경보 모델 - 감성 위험도 지도 시각화")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # 지금 데이터 컬럼에 맞게 필수 컬럼명 설정
    required_cols = ['위도', '경도', '감성결과', '내용']

    st.write("업로드된 엑셀 파일 컬럼명:")
    st.write(df.columns.tolist())

    if all(col in df.columns for col in required_cols):
        m = folium.Map(location=[37.4979, 127.0276], zoom_start=13)
        # cluster 컬럼이 없으니 기본 색상을 모두 같은 색으로 지정
        default_color = 'blue'

        # 위험도 컬럼이 없으니 감성결과를 기반으로 간단 위험도 판별 (예: '부정'이면 위험도 높음)
        def get_risk_level(sentiment):
            if sentiment == "부정":
                return "높음"
            elif sentiment == "중립":
                return "중간"
            else:
                return "낮음"

        for _, row in df.dropna(subset=required_cols).iterrows():
            risk = get_risk_level(row['감성결과'])
            popup_text = (
                f"<b>🧠 감성 결과:</b> {row['감성결과']}<br>"
                f"<b>⚠️ 위험도:</b> {risk} 단계<br><br>"
                f"<b>📝 내용:</b> {row['내용'][:60]}..."
            )
            folium.CircleMarker(
                location=[row['위도'], row['경도']],
                radius=6,
                color=default_color,
                fill=True,
                fill_opacity=0.7,
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=f"감성 결과 {row['감성결과']} / 위험도 {risk}"
            ).add_to(m)

        st_folium(m, width=700, height=500)

    else:
        missing = [col for col in required_cols if col not in df.columns]
        st.error(f"데이터에 다음 컬럼이 없습니다:\n{missing}\n엑셀 파일 컬럼명을 확인해주세요.")

else:
    st.info("위의 업로드 버튼을 눌러 엑셀 파일을 선택하세요.")
