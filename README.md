# 概要

 - Retrieval-Augmented Generation (RAG) 技術を活用したチャットアプリケーションのバックエンドAPI


# 使用技術
 
 - 言語：Python
 - Webフレームワーク：FastAPI
 - パッケージ管理：Poetry
 - DB：MySQL
 - ORM：SQLAlchemy
 - AIサービス：Azure OpenAI（GPT-4o, Embedding API）
 - RAGライブラリ：LlamaIndex

# 開発について

## ポート設定について

 - 開発環境のポート
   - アプリケーション: 8000 (標準)
   - MySQL: 3306 (標準)

 - テスト環境のポート
   - アプリケーション: 8001 (開発環境との競合を回避)
   - MySQL: 3307 (開発環境との競合を回避)

 - 設定ファイル
   - 開発環境: docker-compose.yml
   - テスト環境: docker-compose-test.yml

## 環境構築について

 - リポジトリをクローン
    ```
    git clone {HTTPS or SSH URL} 
    ```

 - 初回起動時・設定変更時（イメージビルド） 
   ※事前準備：.env.exampleをコピーして.envファイルを作成し、プロジェクト直下に配置

    ```
    docker compose build 
    ```

 - コンテナ起動

    ```
    docker compose up -d
    ```
## Swagger

 - http://localhost:8000/docs にアクセスし、SwaggerUIを開く
 - API実行方法
  1. APIのエンドポイント一覧が表示されるので、実行したいエンドポイント展開させる
  2. 「Try it out」ボタンを押下し、必要に応じてパラメータとリクエストボディを入力する
  3. 「Execute」ボタンを押下し、API実行

## src/rag_chat_backendディレクトリについて

 - api：エンドポイント定義、リクエスト/レスポンスの処理
 - core：アプリケーション全体の設定
 - exceptions：カスタム例外クラスの定義
 - handlers：エラー発生時の処理・例外ハンドリング
 - loggers：ログ出力の設定・管理
 - logic：ビジネスロジック（DB操作は含まない）
 - models：
    - db：テーブル定義
    - response：APIレスポンス用のモデル定義
    - request：APIリクエスト用のモデル定義
 - repositories：DBへのCRUD操作、クエリ実行
 - services：外部サービスとの通信
 - store：ナレッジの管理

# テストについて

## 基本方針
 - testsディレクトリ配下にテストファイルを作成
 - アプリケーション構造と同じ階層構造で管理
 - テストフレームワークとしてpytestを使用（unittestモジュールは使用しない）
 - 命名規則
    - テストファイル: test_*.py
    - テスト関数: test_* で始める
    - テストクラス: Test* で始める（関連するテストをグループ化する場合のみ使用）

## テスト環境について
 - テスト実行時は、開発環境で使用しているDockerコンテナとは別のコンテナを起動して実行
 - コンテナ起動
   ※テスト環境では .env.testの値を使用するため、.envに更新があった場合は、.env.testも合わせて更新
    ```
    docker compose -f docker-compose-test.yml --env-file .env.test -p rag-chat-backend-test up -d
    ```

## テスト実行について
 - テスト実行 

    ```
    pytest
    ```
