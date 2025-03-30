from model import Population
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta, timezone
from PIL import Image


def get_japan_date_text():
    # JSTはUTC+9
    jst = timezone(timedelta(hours=9))
    now_jst = datetime.now(jst)
    return now_jst.strftime("%y%m%d")  # 西暦下2桁 + 月 + 日


# モデルの初期化
model = Population()

# ページ設定
st.set_page_config(page_title="令和2年国勢調査 人口集計", layout="wide")

# メインタイトル
image = Image.open("./fig/title.jpg")
ratio = image.height / image.width
new_height = int(500 * ratio)
resized_image = image.resize((500, new_height), Image.LANCZOS)

st.image(resized_image)
# st.image(image, use_container_width=True)

st.subheader("人口/世帯数 基本集計")

# サイドバー設定
st.sidebar.title("2020年国勢調査")
st.sidebar.header("集計設定")

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

            age_min = st.number_input("年齢（from）", min_value=0, max_value=110, value=18, key=f"age_min_{i}")
            age_max = st.number_input("年齢（to）", min_value=0, max_value=110, value=59, key=f"age_max_{i}")
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
        formatted_value = f"{value:,} {unit}"

        # 枠の外に「集計 ◯」のタイトルを出す
        st.markdown(
            f"<h4 style='margin-top:0.1rem; margin-bottom:0.3rem;'>▼ 集計 {idx}</h4>",
            unsafe_allow_html=True
        )

        # 結果だけをカード内にスタイリッシュに表示
        st.markdown(
            f"""
            <div style="
                background-color:#f8f9fa;
                padding: 1.5rem;
                border-left: 6px solid #4A90E2;
                border-radius: 8px;
                font-size: 2.0rem;
                font-weight: bold;
                color: #222;
                margin-bottom: 0.5rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            ">
                {formatted_value}
            </div>
            """,
            unsafe_allow_html=True
        )

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

        st.caption("\n")
        st.caption("※コピー用※")
        st.code(f"{value}", language="python")
        st.caption("↑コピーする場合は上記ブロックの右端ボタンをクリック")

        st.markdown("---")

# Excel出力
if excel_rows:
    st.markdown("""    
    #### Excelでエクスポート
    """)
    df_excel = pd.DataFrame(excel_rows)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_excel.to_excel(writer, index=False, sheet_name="集計結果")

    excel_data = output.getvalue()

    date_text = get_japan_date_text()
    default_filename = "令和2年国勢調査_人口集計_" + date_text + ".xlsx"
    filename_input = st.text_input("※ファイル名を変更する場合はファイル名を入力してEnter（拡張子は.xlsxのみ有効）", value=default_filename)
    st.download_button(
        label="Excelでダウンロード",
        data=excel_data,
        file_name=f"{filename_input}",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.markdown("---")

# 集計結果の後に備考を表示
st.markdown("""
<small>

#### 出典  
- **政府統計の総合窓口**：[e-Stat](https://www.e-stat.go.jp/)
- **国勢調査**： [令和2年(2020年)](https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466&tclass2val=0)  
  **表番号**： [1-1](https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466&stat_infid=000032142402&tclass2val=0) / [2-1](https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466&stat_infid=000032142404&tclass2val=0)
---
#### 人口と世帯数
- 年齢不詳の**2,931,838人**は除外
- 世帯数は「2_施設等の世帯」も含む総数で算出
- 年齢上限は110才(年齢(to)を[110]に設定すると110才以上の全ての人口を表示)  
---
#### 主要エリアの内訳
- **関東(1都6県)**： 茨城、栃木、群馬、埼玉、千葉、東京、神奈川  
- **東海(3県)**： 岐阜、愛知、三重  
- **関西(2府4県)**： 滋賀、京都、大阪、兵庫、奈良、和歌山  
- **福岡(2県)**： 福岡、佐賀
---
#### 更新情報
- **最終更新日**：2025/03/30(日)
- **更新内容**：アプリケーション全体を最新化し、UI・UXを向上
- **次回の国勢調査**： 2025年秋頃に実施想定、結果は2026年末頃に公開される見通し

</small>
""", unsafe_allow_html=True)



