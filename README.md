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



# ブランチ運用について

## 概要
   - 本プロジェクトでは、効率的な開発とコード品質の維持を目的としたGitブランチ運用ルールを定めている。社内学習用プロジェクトのため、通常のreleaseブランチを経由したリリースフローは省略し、シンプルな運用を採用

## ブランチ構成

### main
 - 目的: 本番環境の状態を管理
 - 特徴: 常に安定した状態を保つ
 - マージ元: developブランチ

### develop
 - 目的: 開発版の統合ブランチ
 - 特徴: 各機能開発の統合地点
 - マージ元: feature/, bugfix/
 - マージ先: mainブランチ

### feature
 - 目的: 新機能開発用ブランチ
 - 作成元・マージ先: developブランチ

### bugfix
 - 目的: developにマージ済み機能のバグ修正用
 - 作成元・マージ先: developブランチ
 
### 運用フロー図
 ```mermaid
   gitGraph
      commit id: "初期化"
      branch develop order:1
      checkout develop
      commit id: "開発環境構築"
      
      branch feature order:2
      checkout feature
      commit id: "新機能開発"
      commit id: "機能完成"
      checkout develop
      merge feature
      commit id: "機能マージ完了"
      
      branch bugfix order:3
      checkout bugfix
      commit id: "バグ修正"
      commit id: "修正完了"
      checkout develop
      merge bugfix
      commit id: "バグ修正マージ完了"
      
      checkout main
      merge develop
      commit id: "本番環境反映"
 ```

## 使用時のルール

### 開発フロー（マージ・被マージ）
1. developブランチからfeature/bugfixブランチ作成
   - 各担当者が開発・修正作業
   - タスク毎にブランチを作成

2. Pull Request作成
   - developブランチへのPull Requestを作成
   - タイトルに MYIS-{チケット番号} を先頭に記載
      - ex）``MYIS-1234:ログイン機能追加``
   - Pull Requestのテンプレート通りに記載すること
   - CIによる単体テストクリアが必須

3. コードレビュー
   - 管理者がソースレビューを実施
   - 承認後にマージ

4. mainブランチへの反映
   - SP完了後に実施：developにマージ済みのブランチ（完了済みタスク）のみが対象となる
   - developブランチからmainブランチにマージ（例外: 本プロジェクトはリリースがないため、releaseブランチを省略してdevelop → mainに直接マージする）

### タスク別使用方法
- 新機能開発タスク
   - 使用ブランチ: feature/
   - 命名規則: feature/MYIS-{チケット番号}
      - ex）``feature/MYIS-1234``

- 既存機能バグ修正タスク
   - 使用ブランチ: bugfix/
   - 命名規則: bugfix/MYIS-{チケット番号}
      - ex）``bugfix/MYIS-1234``
   - 例外: チケット番号が追えない場合など不明な場合は、機能名や修正内容を明記する
      - ex）``bugfix/login-error-handling``

### 禁止事項
 - 直接Push禁止: main、developブランチへの直接Push
 - Pull Request必須: すべてのマージはPull Requestを経由
 - CI未通過でのマージ禁止: 単体テストクリアが必須条件
