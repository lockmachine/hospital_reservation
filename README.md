# Hospital Reservation System

病院の予約システムを自動化するPythonスクリプトです。Seleniumを使用してブラウザ操作を自動化し、指定時刻に予約を行います。

## 機能

- 複数ユーザーの予約対応（1人または2人分の予約）
- 指定時刻に自動実行（スケジュール機能）
- Selenium + webdriver-manager による自動化

## 必要要件

- Python 3.9以上
- Google Chrome ブラウザ

## セットアップ

1. 仮想環境を作成
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

3. 設定ファイルを作成
`person_data.env` ファイルを作成し、以下の情報を入力：
```
HOSPITAL_URL="病院のURL"
E_ID="ユーザーID1"
E_BIRTH="生年月日(MMDD形式)"
E_NAME="ユーザー名1"
T_ID="ユーザーID2"
T_BIRTH="生年月日(MMDD形式)"
T_NAME="ユーザー名2"
```

## 使用方法

```bash
python hospital_reservation.py
```

実行後、以下の手順で操作：
1. 予約対象を選択（e/t/2）
2. 開始時刻を入力（HH:MM:SS形式）
3. 指定時刻に自動実行

## ファイル説明

- `hospital_reservation.py` - メインスクリプト
- `hospital_reservation_2.py` - バージョン2
- `hospital_reservation_3.py` - バージョン3
- `person_data.env` - 設定ファイル（.gitignoreで除外）
- `Pipfile` - Pipenv依存関係ファイル

## 注意事項

- `person_data.env` には個人情報を含むため、GitHubにはアップロードされません
- Chromeのバージョンと webdriver-manager の互換性を確認してください
