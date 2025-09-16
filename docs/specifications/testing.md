# テスト仕様書

## 概要

献立作成ツールにおけるテスト戦略、TDD（テスト駆動開発）実践方法、および品質保証の仕組みを定義する。

## テスト戦略

### TDD導入（t-wada流）

**t-wada流テスト駆動開発**を採用し、品質と安全性を確保：

#### 基本原則

- **Red-Green-Refactor**: 厳格なサイクル遵守
- **ベイビーステップ**: 一度に一つの変更のみ
- **仮実装**: 固定値から始めて段階的に一般化
- **三角測量**: 複数テストで段階的に仕様を固める

#### 実装順序

1. **既存機能保護テスト** （最優先）
2. **新機能TDD実装** （段階的）
3. **リファクタリング** （Green時のみ）

### テスト分類

#### 1. 回帰テスト（既存機能保護）

**目的**: TDD導入前の既存機能を保護し、変更による破損を防止

**対象機能**:

- 月曜日バリデーション
- JSON出力形式
- 長期休暇対応（空オブジェクト出力）
- 基本入力→出力フロー

#### 2. 単体テスト

**新規TDD実装**:

- 複数行入力処理（parse_menu_text関数）
- 改行文字の保持・変換
- 空行・特殊文字対応

**既存機能のテスト強化**:

- 月曜日バリデーション機能
- JSON構造化処理
- 空オブジェクト生成機能

#### 3. 統合テスト

**対象範囲**:

- GUI操作からファイル出力まで
- エラーハンドリングの統合動作
- 長期休暇確認ダイアログの動作

#### 4. UI/UXテスト

**対象操作**:

- 業者データのコピー&ペースト操作
- 複数行入力の使いやすさ検証
- 長期休暇期間の入力操作
- エラーメッセージの表示確認

## テスト実行環境

### 技術スタック

- **テストフレームワーク**: pytest>=8.0
- **実行環境**: Python 3.12+
- **依存関係管理**: uv

### 実行方法

```bash
# 全テスト実行
uv run pytest

# 特定ファイルのテスト
uv run pytest tests/test_main.py

# 詳細表示
uv run pytest -v

# カバレッジ確認（将来実装）
uv run pytest --cov=main

# 失敗したテストのみ再実行
uv run pytest --lf
```

### テストファイル構成

```
tests/
├── __init__.py                    # テストパッケージ
├── test_main.py                   # メイン機能テスト
│   ├── test_monday_validation()   # 月曜日バリデーション
│   ├── test_json_output()         # JSON出力形式
│   ├── test_empty_meal_handling() # 空データ処理
│   └── test_parse_menu_text()     # 複数行入力処理
├── test_regression.py             # 回帰テスト
├── test_integration.py            # 統合テスト（将来実装）
└── fixtures/                     # テストデータ
    ├── sample_menu.json
    └── test_input.txt
```

## TDD実践ガイド

### テスト命名規則

```python
def test_機能名_条件_期待結果():
    """
    例: test_parse_menu_text_multiline_returns_list()
    例: test_monday_validation_tuesday_returns_false()
    例: test_json_output_empty_meal_creates_empty_object()
    """
```

### TDDサイクル実践例

#### Red → Green → Refactor の具体例

```python
# 1. Red: 失敗するテストを作成
def test_parse_menu_text_multiline_returns_list():
    menu_text = "パン\nスープ\nウィンナー"
    expected = ["パン", "スープ", "ウィンナー"]
    assert parse_menu_text(menu_text) == expected

# 2. Green: 仮実装で通す
def parse_menu_text(text):
    return ["パン", "スープ", "ウィンナー"]  # 固定値

# 3. 三角測量: 別のテストで仮実装を破る
def test_parse_menu_text_different_menu_returns_list():
    menu_text = "ご飯\n味噌汁"
    expected = ["ご飯", "味噌汁"]
    assert parse_menu_text(menu_text) == expected

# 4. Green: 一般化
def parse_menu_text(text: str) -> list[str]:
    if not text.strip():
        return []
    return [line.strip() for line in text.split('\n') if line.strip()]

# 5. Refactor: 改善・最適化
```

### ベイビーステップの例

```python
# ステップ1: 基本的な分割
def test_parse_menu_text_simple_split():
    assert parse_menu_text("A\nB") == ["A", "B"]

# ステップ2: 空行対応
def test_parse_menu_text_with_empty_lines():
    assert parse_menu_text("A\n\nB") == ["A", "B"]

# ステップ3: 前後の空白除去
def test_parse_menu_text_strips_whitespace():
    assert parse_menu_text(" A \n B ") == ["A", "B"]

# ステップ4: 空文字列対応
def test_parse_menu_text_empty_string():
    assert parse_menu_text("") == []
```

## 品質指標

### テストカバレッジ目標

- **回帰テスト**: 100%（既存機能保護）
- **新機能**: 95%以上（TDD実装）
- **統合テスト**: 主要フロー100%

### 合格基準

- **全テストGreen**: 必須
- **実行時間**: 10秒以内
- **エラーゼロ**: 警告含む

## CI/CD統合（将来実装）

### 自動テスト実行

```bash
# GitHub Actions想定
- name: Run tests
  run: |
    uv sync
    uv run pytest --cov=main --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

### テスト実行タイミング

- **コミット前**: 必須
- **プルリクエスト**: 自動実行
- **リリース前**: 全テスト + 手動確認

## エラーハンドリングテスト

### テスト対象エラー

```python
def test_monday_validation_invalid_date():
    """無効な日付でエラーが発生することを確認"""
    with pytest.raises(ValueError):
        validate_monday("2025-13-32")

def test_json_output_write_permission_error():
    """書き込み権限エラーの処理を確認"""
    # 読み取り専用ディレクトリでのテスト
    pass

def test_file_encoding_error_handling():
    """文字エンコーディングエラーの処理を確認"""
    pass
```

## テストデータ管理

### テストフィクスチャ

```python
import pytest

@pytest.fixture
def sample_menu_data():
    return {
        "week_start": "2025-09-15",
        "facility": "職業訓練施設寮",
        "meals": [
            {
                "date": "2025-09-15",
                "day_of_week": "月",
                "breakfast": {
                    "menu": "パン\nスープ\nウィンナー",
                    "start_time": "07:00",
                    "end_time": "08:00",
                    "location": "寮食堂"
                }
            }
        ]
    }

@pytest.fixture
def empty_menu_data():
    """長期休暇用の空データ"""
    return {}
```

## デバッグ・トラブルシューティング

### よくある問題

1. **GUIテストの実行エラー**
   - ヘッドレス環境での実行設定
   - モックを使用した分離テスト

2. **ファイルI/Oテストの競合**
   - 一時ディレクトリの使用
   - テスト後のクリーンアップ

3. **日付依存テストの不安定性**
   - 固定日付でのテスト
   - モック使用による時間制御

### デバッグコマンド

```bash
# 特定のテストのみ実行
uv run pytest tests/test_main.py::test_monday_validation -v

# 失敗時に即座に停止
uv run pytest -x

# デバッグ情報付きで実行
uv run pytest -s --tb=long
```

## 今後の拡張計画

### Phase 1: 基盤構築（現在）

- [x] pytest環境構築
- [ ] 回帰テスト実装
- [ ] 基本TDD実装

### Phase 2: 充実化

- [ ] パフォーマンステスト
- [ ] UI自動テスト
- [ ] カバレッジ向上

### Phase 3: 自動化

- [ ] CI/CD統合
- [ ] 自動レポート生成
- [ ] テスト並列実行

---

**更新**: 2025-09-16 - TDD導入フェーズに合わせて作成
