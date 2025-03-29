# 令和2年 国勢調査 人口集計アプリ

## 概要

本アプリケーションは、2020年（令和2年）の国勢調査のデータを利用して、都道府県・地域別の人口や世帯数を簡単に集計・表示できるWebアプリケーションです。Streamlitを用いて直感的でユーザーフレンドリーなインターフェースを提供します。

実際に公開されているアプリはこちらからご覧いただけます：
👉 [令和2年 国勢調査 人口集計アプリ](https://japan-population.streamlit.app/)

## 機能説明

- **人口および世帯数の集計**：
  - 特定の地域（都道府県）の人口や世帯数を簡単に算出
  - 年齢範囲、性別、日本人のみ・外国籍を含む等、細かい条件設定が可能
  - 集計条件を複数設定し、比較表示することも可能

- **Excel出力機能**：
  - 集計結果をExcel形式でダウンロード可能

- **直感的なインターフェース**：
  - Streamlitによるわかりやすい画面構成
  - サイドバーでの簡単な条件設定

## 使用データ

本アプリは、日本政府の統計ポータルサイト [e-Stat](https://www.e-stat.go.jp/) に掲載された以下のデータを利用しています。

- **令和2年（2020年）国勢調査データ**：
  - [人口（表番号1-1）](https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466&stat_infid=000032142402&tclass2val=0)
  - [世帯数（表番号2-1）](https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466&stat_infid=000032142404&tclass2val=0)

## 使用技術

- Python（3.8以上）
- Streamlit
- Pandas
- XlsxWriter

## ディレクトリ構成

```bash
population_app/
├── data/
│   ├── R2_pop_age.pickle
│   └── R2_pop_setai.pickle
├── model.py
├── app.py
├── requirements.txt
└── README.md
```

## インストールと実行方法

### 環境構築

1. リポジトリをクローンします。

```bash
git clone https://github.com/your-username/population_app.git
cd population_app
```

2. 仮想環境を作成し、必要なライブラリをインストールします。

```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合は venv\Scripts\activate
pip install -r requirements.txt
```

### アプリの起動

```bash
streamlit run app.py
```

ブラウザで [http://localhost:8501](http://localhost:8501) を開いてアクセスします。

## 使用方法

- サイドバーから「人口」または「世帯数」を選択します。
- 集計条件（地域、性別、年齢範囲など）を入力します。
- 「集計数」で複数条件を同時に設定・表示可能です。
- 条件を入力後、自動的に結果が画面中央に表示されます。
- 必要に応じて「Excelでダウンロード」ボタンをクリックし、結果を保存できます。

## 注意事項

- 年齢上限を110歳に設定すると、110歳以上の全人口が含まれます。
- 年齢不詳の人口（約290万人）は計算に含めていません。

## 次回の更新予定

次回の国勢調査は2025年秋頃に実施予定であり、その結果は2026年末頃に公開される予定です。公開後、随時アップデート予定です。

## 著作権・データ利用について

使用データは全て政府統計(e-Stat)より取得しており、政府の定める利用規約に従って利用しています。詳しくは [e-Stat利用規約](https://www.e-stat.go.jp/terms) をご確認ください。

## 最終更新

- **日付**：2025年3月31日
- **更新内容**：アプリケーション全体を最新化し、UI・UXを向上

