from model import Population
import streamlit as st
import pandas as pd
from io import BytesIO


# モデルの初期化
model = Population()

# ページ設定
st.set_page_config(page_title="令和2年国勢調査 人口集計", layout="wide")

# メインタイトル
st.title("令和2年('20年) 国勢調査")
st.subheader("世帯数・人口 基本集計")

# サイドバー設定
st.sidebar.title("設定")

# 集計対象の選択
household_or_personal = st.sidebar.radio("【集計対象】", ["人口", "世帯数"], index=0)
area_list = model.area_list(flag_household=0 if household_or_personal == "人口" else 1)

# 集計数の入力
number_of_aggregation = st.sidebar.number_input(
    "【集計数】",
    min_value=1,
    max_value=20,
    value=1,
    step=1
)

st.sidebar.markdown("---")

# 集計ごとの条件と結果の格納リスト
aggregations = []
excel_rows = []  # Excel用データ

for i in range(number_of_aggregation):
    with st.sidebar.expander(f"▼ 集計 {i + 1} の条件", expanded=True):
        # 各集計の条件を辞書にまとめる
        settings = {}
        selected_area = st.multiselect("地域", area_list, key=f"area_{i}")
        settings["地域"] = ", ".join(selected_area) if selected_area else "未選択"

        if household_or_personal == "人口":
            flag_japanese_option = st.radio("国民種別", ["日本人のみ", "外国籍含む"], index=0, key=f"flag_japaneze_{i}")
            flag_japanese = 1 if flag_japanese_option == "日本人のみ" else 0
            settings["国民種別"] = flag_japanese_option

            sex = st.radio("性別", ["男女", "男", "女"], index=0, key=f"sex_{i}")
            settings["性別"] = sex

            age_min = st.number_input("年齢（下限）", min_value=0, max_value=110, value=20, key=f"age_min_{i}")
            age_max = st.number_input("年齢（上限）", min_value=0, max_value=110, value=59, key=f"age_max_{i}")
            settings["年齢"] = f"{age_min}～{age_max}"

            if selected_area:
                result = model.age_area_population(
                    age_min=age_min,
                    age_max=age_max,
                    area=selected_area,
                    sex=sex,
                    flag_japaneze=flag_japanese
                )
            else:
                result = None
        else:
            settings["集計対象"] = "世帯数"
            if selected_area:
                result = model.household_count(area=selected_area)
            else:
                result = None

        aggregations.append((i + 1, result, "人" if household_or_personal == "人口" else "世帯", settings))

        # Excel用データを追加
        excel_row = {
            '集計番号': i + 1,
            '集計対象': household_or_personal,
            '地域': settings.get('地域', '未選択'),
            '国民種別': settings.get('国民種別', '-'),
            '性別': settings.get('性別', '-'),
            '年齢範囲': settings.get('年齢', '-'),
            '結果': result
        }
        excel_rows.append(excel_row)

# --- 結果表示 ---
if not aggregations or all(r[1] is None for r in aggregations):
    st.info("左のサイドバーから集計条件を選択してください。")
else:
    for idx, value, unit, settings in aggregations:
        if value is None:
            continue
        formatted_value = f"{value:,} {unit}"
        # 集計結果カードの表示（設定内容は枠外に表示）
        st.markdown(
            f"""
            <div style="
                background-color:#f0f2f6;
                padding: 1.2rem;
                border-radius: 12px;
                margin-bottom: 0.5rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <h4 style="margin-bottom: 0.5rem; color: black;">集計 {idx}</h4>
                <p style="font-size: 1.5rem; font-weight: bold; color: black;">{formatted_value}</p>
            </div>
            """, unsafe_allow_html=True)
        # 設定内容をカードの外で表示
        # 設定内容を控えめに表示する例
        st.markdown(
            "<div style='font-size:0.9rem; margin-top:0.5rem;'>設定内容:</div>",
            unsafe_allow_html=True
        )
        for key, val in settings.items():
            st.markdown(
                f"<div style='font-size:0.8rem; margin-bottom:0.2rem;'>{key}: {val}</div>",
                unsafe_allow_html=True
            )

        st.markdown("---")

# Excel出力
if excel_rows:
    st.markdown("""    
    #### エクスポート
    集計結果をEXCELでダウンロード
    """)
    df_excel = pd.DataFrame(excel_rows)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_excel.to_excel(writer, index=False, sheet_name="集計結果")

    excel_data = output.getvalue()

    st.download_button(
        label="Excelでダウンロード",
        data=excel_data,
        file_name="population_aggregation.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.markdown("---")

# 集計結果の後に備考を表示
st.markdown("""
<small>

#### 出典  
- **国勢調査**： [令和2年(2020年)](https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466&tclass2val=0)  
  **表番号**： [1-1](https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466&stat_infid=000032142402&tclass2val=0) / [2-1](https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466&stat_infid=000032142404&tclass2val=0)
---
#### 人口と世帯数の補足
- 年齢不詳の**2,931,838人**は除外
- 世帯数は「2_施設等の世帯」も含む総数で算出
---
#### 主要エリアの概要 
- **関東(1都6県)**： 茨城、栃木、群馬、埼玉、千葉、東京、神奈川  
- **東海(3県)**： 岐阜、愛知、三重  
- **関西(2府4県)**： 滋賀、京都、大阪、兵庫、奈良、和歌山  
- **福岡(2県)**： 福岡、佐賀
---
#### 注意点 
- **年齢上限**： 110才 ([110]に設定すると110才以上の人口を算出)  
- **次回の国勢調査**： 2025年秋頃に実施、結果は2026年末頃に公開想定
---
#### 更新情報
- **最終更新日**：2025/03/31(日)
- **更新内容**：アプリ全体を更新
</small>
""", unsafe_allow_html=True)



