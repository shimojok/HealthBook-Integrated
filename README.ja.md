# HealthBook-Integrated

**浜田式問診 × 疾病マトリックス × MBT漢方代謝ライブラリー統合ヘルスケア推論プラットフォーム**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## 概要

HealthBook-Integratedは、以下の3つのコアコンポーネントを統合した総合ヘルスケア推論システムです：

1. **浜田式200項目問診** - 30年間・30万人以上の臨床データに基づく
2. **137疾病マトリックス** - 食生活と疾病の相関マッピング
3. **MBT漢方代謝ライブラリー** - 293方剤のファイトケミカル分析付き

本システムは、代謝解析、疾病リスク評価、ファイトケミカル推奨、漢方処方推奨、MBT55プロバイオティクス最適化を含むパーソナライズされた健康推奨を提供します。

## リポジトリ構造

```
HealthBook-Integrated/
├── README.md                          # 英語版ドキュメント
├── README.ja.md                       # 日本語版ドキュメント（本ファイル）
├── LICENSE                            # MITライセンス
├── requirements.txt                   # Python依存パッケージ
├── data/
│   ├── en/                            # 英語データ
│   │   ├── questionnaire_200.json     # 200項目問診（英語）
│   │   └── disease_matrix_137.json    # 137疾病マトリックス（英語）
│   ├── ja/                            # 日本語データ
│   │   ├── questionnaire_200.json     # 200項目問診（日本語）
│   │   └── disease_matrix_137.json    # 137疾病マトリックス（日本語）
│   └── kampo_metabolic_library.json   # 293漢方処方（日英統合）
├── src/healthbook/
│   ├── __init__.py
│   ├── engine.py                      # メイン推論エンジン
│   ├── disease_risk.py                # 疾病リスク予測
│   ├── phytochemical_recommender.py   # ファイトケミカル推奨
│   └── kampo_mapper.py                # 漢方処方マッパー
├── examples/
│   ├── healthbook_demo.py             # 完全デモスクリプト
│   └── mbt55_integration.py           # MBT55連携デモ
└── tests/
    └── test_engine.py                 # 単体テスト
```

## クイックスタート

### インストール

```bash
# リポジトリのクローン
git clone https://github.com/shimojok/HealthBook-Integrated.git
cd HealthBook-Integrated

# 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 基本的な使用方法

```python
from src.healthbook import HealthBookEngine, Language

# エンジンの初期化（日本語）
engine = HealthBookEngine(language=Language.JAPANESE)

# 問診回答（question_id -> Yes/No）
responses = {
    1: True,   # 食事の時間が不定である
    2: True,   # 朝食を抜くことがよくある
    9: True,   # 塩辛い食べものが好き
    55: True,  # 運動不足である
    60: True,  # ストレスを感じやすい
}

# 分析実行
result = engine.analyze(questionnaire_responses=responses)

# 結果表示
print(f"総合リスクレベル: {result.overall_risk_level}")
print(f"上位疾病リスク: {list(result.disease_risks.keys())[0]}")
```

## 機能

### 1. 代謝不全分析
問診回答から代謝問題を特定し、各リスクファクターを特定の代謝経路（PATH_01～05）にマッピングします。

### 2. 疾病リスク予測
浜田式疾病マトリックスを使用して137疾病を評価し、40以上の食生活・生活習慣パターンに基づいてリスクスコアを計算します。

### 3. ファイトケミカル推奨
検出された疾病リスクに基づいて有益なファイトケミカルを提案し、食品源とMBT55経路マッピングを提供します。

### 4. 漢方処方推奨
MBT漢方代謝ライブラリー（293方剤）から伝統的な漢方処方を推奨し、MBT55最適化パラメータを含みます。

### 5. MBT55最適化
パーソナライズされたプロバイオティクス菌株の推奨と発酵プロトコルを提供します。

## APIリファレンス

### HealthBookEngine

| メソッド | 説明 |
|---------|------|
| `__init__(language=Language.ENGLISH)` | 言語を指定してエンジンを初期化 |
| `analyze(questionnaire_responses, health_check_data=None, mbt55_profile=None)` | 総合分析を実行 |

### DiseaseRiskPredictor

| メソッド | 説明 |
|---------|------|
| `predict(risk_factors)` | リスクファクターから疾病リスクを予測 |
| `get_top_risks(risk_factors, top_n=10)` | 上位N個の疾病リスクを取得 |

### PhytochemicalRecommender

| メソッド | 説明 |
|---------|------|
| `recommend_for_disease(disease_id, top_n=5)` | 特定疾病に対する推奨 |
| `get_food_sources(phytochemical_name)` | ファイトケミカルの食品源を取得 |

### KampoMapper

| メソッド | 説明 |
|---------|------|
| `search_by_symptom(symptom, language="ja")` | 症状から漢方処方を検索 |
| `recommend_by_disease(disease_id, top_n=3)` | 疾病から漢方処方を推奨 |
| `get_mbt55_optimization(formula_id)` | MBT55最適化情報を取得 |

## データソース

| コンポーネント | 出典 | 説明 |
|--------------|------|------|
| 問診 | 浜田式 | 200項目、30年以上の臨床データ |
| 疾病マトリックス | 浜田式 | 137疾病 × 40以上の生活習慣パターン |
| 漢方ライブラリー | MBT漢方 v2.44 | 293方剤、ファイトケミカル分析付き |
| ファイトケミカル | 下條式分類 | ポリフェノール、カロテノイド、イオウ化合物 |

## M3-BioSynergyとの連携

本リポジトリは [M3-BioSynergy](https://github.com/shimojok/M3-BioSynergy) と連携して動作します。M3-BioSynergyは以下を実装しています：

- 微生物多様性モデル（120菌種）
- 炭素隔離のハイパーサイクルエンジン
- 栄養カスケードシミュレーション

パーソナライズされた健康推奨にはHealthBook-Integratedを、生態学・農業応用にはM3-BioSynergyを使用してください。

## ライセンス

MITライセンス - 詳細は [LICENSE](LICENSE) ファイルをご覧ください。

## 著者

**下條和彦** - BNioNexus Holdings Co-Founder, 日本サプリメント協会 元理事

## 関連リポジトリ

- [M3-BioSynergy](https://github.com/shimojok/M3-BioSynergy) - 微生物-代謝-モジュラー理論

## 引用

本ソフトウェアを研究で使用する場合は、以下のように引用してください：

```bibtex
@software{Shimojo_HealthBook_Integrated_2025,
  author = {Shimojo, Kazuhiko},
  title = {HealthBook-Integrated: 統合ヘルスケア推論プラットフォーム},
  year = {2025},
  url = {https://github.com/shimojok/HealthBook-Integrated}
}
```
