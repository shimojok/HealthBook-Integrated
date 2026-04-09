#!/usr/bin/env python3
"""
HealthBook-Integrated デモスクリプト

このスクリプトは、HealthBook統合推論エンジンの基本的な使用方法を示します。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.healthbook import HealthBookEngine, Language
from src.healthbook.disease_risk import DiseaseRiskPredictor
from src.healthbook.kampo_mapper import KampoMapper


def demo_english():
    """英語版デモ"""
    print("=" * 60)
    print("HealthBook-Integrated Demo (English)")
    print("=" * 60)
    
    # エンジンの初期化
    engine = HealthBookEngine(language=Language.ENGLISH)
    
    # サンプル問診回答
    responses = {
        1: True,   # Meal times are irregular
        2: True,   # Often skip breakfast
        9: True,   # Prefer salty foods
        55: True,  # Lack of exercise
        60: True,  # Prone to stress
        68: True,  # Prone to constipation
        71: True,  # Easily fatigued
        75: True,  # Gain weight easily
    }
    
    # 分析実行
    result = engine.analyze(questionnaire_responses=responses)
    
    # 結果表示
    print(f"\n📊 Analysis ID: {result.analysis_id}")
    print(f"📅 Timestamp: {result.timestamp}")
    print(f"🎯 Overall Risk Level: {result.overall_risk_level.upper()}")
    
    print("\n🔬 Top 5 Disease Risks:")
    for i, (disease, risk_info) in enumerate(list(result.disease_risks.items())[:5], 1):
        print(f"  {i}. {risk_info['disease_name']}: {risk_info['risk_score']*100:.0f}% ({risk_info['risk_level']})")
    
    print("\n🌿 Phytochemical Recommendations:")
    for rec in result.phytochemical_recommendations[:3]:
        print(f"  • {rec['phytochemical']} - for {rec['disease']}")
        print(f"    Foods: {', '.join(rec['food_sources'])}")
    
    print("\n🏥 Kampo Formula Recommendations:")
    for rec in result.kampo_recommendations:
        print(f"  • {rec['name']} - for {rec['for_disease']}")
        print(f"    Indications: {', '.join(rec['indications'][:2])}")
        print(f"    MBT55 Boost: {rec['bioavailability_boost']}")
    
    return result


def demo_japanese():
    """日本語版デモ"""
    print("=" * 60)
    print("HealthBook-Integrated デモ（日本語）")
    print("=" * 60)
    
    # エンジンの初期化（日本語）
    engine = HealthBookEngine(language=Language.JAPANESE)
    
    # サンプル問診回答
    responses = {
        1: True,   # 食事の時間が不定である
        2: True,   # 朝食を抜くことがよくある
        9: True,   # 塩辛い食べものが好き
        55: True,  # 運動不足である
        60: True,  # ストレスを感じやすい
        68: True,  # 便秘がちである
        71: True,  # 疲れやすい
        75: True,  # 体重が増えやすい
    }
    
    # 分析実行
    result = engine.analyze(questionnaire_responses=responses)
    
    # 結果表示
    print(f"\n📊 分析ID: {result.analysis_id}")
    print(f"📅 日時: {result.timestamp}")
    
    # リスクレベル日本語化
    risk_level_ja = {
        "low": "低リスク",
        "medium": "中リスク",
        "high": "高リスク",
        "very_high": "極めて高リスク"
    }
    print(f"🎯 総合リスクレベル: {risk_level_ja.get(result.overall_risk_level, result.overall_risk_level)}")
    
    print("\n🔬 上位5疾病リスク:")
    for i, (disease, risk_info) in enumerate(list(result.disease_risks.items())[:5], 1):
        risk_ja = {"low": "低", "medium": "中", "high": "高", "very_high": "極高"}
        print(f"  {i}. {risk_info['disease_name']}: {risk_info['risk_score']*100:.0f}% ({risk_ja.get(risk_info['risk_level'], risk_info['risk_level'])})")
    
    print("\n🌿 ファイトケミカル推奨:")
    for rec in result.phytochemical_recommendations[:3]:
        print(f"  • {rec['phytochemical']} - {rec['disease']} に対して")
        print(f"    食品: {', '.join(rec['food_sources'])}")
    
    print("\n🏥 漢方処方推奨:")
    for rec in result.kampo_recommendations:
        print(f"  • {rec['name']} - {rec['for_disease']} に対して")
        print(f"    適応: {', '.join(rec['indications'][:2])}")
        print(f"    MBT55向上率: {rec['bioavailability_boost']}")
    
    return result


def demo_kampo_search():
    """漢方検索デモ"""
    print("\n" + "=" * 60)
    print("Kampo Search Demo")
    print("=" * 60)
    
    mapper = KampoMapper()
    
    # 症状からの検索
    print("\n🔍 Search by symptom 'headache':")
    results = mapper.search_by_symptom("headache", language="en")
    for formula in results[:3]:
        print(f"  • {formula.name_en} - {', '.join(formula.indications_en[:2])}")
    
    # 疾病からの推奨
    print("\n🔍 Recommend by disease 'hypertension':")
    recommendations = mapper.recommend_by_disease("hypertension", top_n=3)
    for formula in recommendations:
        print(f"  • {formula.name_en}")
        print(f"    MBT55 Strains: {', '.join(formula.mbt55_strains)}")
        print(f"    Bioavailability: {formula.bioavailability_boost}")


def main():
    """メイン実行関数"""
    print("\n" + "=" * 60)
    print("HealthBook-Integrated Demo")
    print("=" * 60)
    
    # 英語デモ実行
    demo_english()
    
    # 日本語デモ実行
    demo_japanese()
    
    # 漢方検索デモ
    demo_kampo_search()
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
