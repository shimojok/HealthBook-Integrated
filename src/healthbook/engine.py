"""
HealthBook-Integrated: 統合推論エンジン

浜田式問診 × 疾病マトリックス × MBT漢方代謝ライブラリーの統合
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Language(Enum):
    """言語設定"""
    ENGLISH = "en"
    JAPANESE = "ja"


class RiskLevel(Enum):
    """リスクレベル"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class QuestionnaireResponse:
    """問診回答データ"""
    responses: Dict[int, bool]  # question_id -> answer (True=Yes)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class HealthCheckData:
    """健康診断データ"""
    basic_metrics: Dict[str, float] = field(default_factory=dict)
    blood_tests: Dict[str, float] = field(default_factory=dict)
    imaging_results: Dict[str, str] = field(default_factory=dict)
    doctor_comments: str = ""
    metabolic_markers: Dict[str, float] = field(default_factory=dict)


@dataclass
class MBT55Profile:
    """MBT55腸内細菌プロファイル"""
    pathway_activity: Dict[str, float] = field(default_factory=dict)
    key_bacteria: List[str] = field(default_factory=list)
    metabolic_capacity: Dict[str, float] = field(default_factory=dict)
    recommended_strains: List[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    """分析結果"""
    analysis_id: str
    timestamp: str
    language: str
    metabolic_imbalances: List[Dict]
    disease_risks: Dict[str, Dict]
    phytochemical_recommendations: List[Dict]
    kampo_recommendations: List[Dict]
    mbt55_optimization: Dict
    overall_risk_level: str
    dietary_advice: List[str]


class HealthBookEngine:
    """
    HealthBook統合推論エンジン
    
    浜田式問診（200項目）と疾病マトリックス（137疾病）を統合し、
    個人の健康状態を分析する。
    """
    
    def __init__(self, language: Language = Language.ENGLISH, data_dir: str = None):
        """
        エンジンを初期化
        
        Args:
            language: 出力言語（英語/日本語）
            data_dir: データディレクトリのパス
        """
        self.language = language
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), "../../data")
        
        # データベース
        self.questionnaire_db: Dict[int, Dict] = {}
        self.disease_matrix_db: Dict[str, Dict] = {}
        self.phytochemical_db: Dict[str, Dict] = {}
        self.kampo_db: Dict[str, Dict] = {}
        
        # 初期化
        self._load_databases()
        self._create_risk_factor_mapping()
        
    def _load_databases(self):
        """データベースをロード"""
        # 問診データ（言語別）
        lang_code = self.language.value
        q_path = os.path.join(self.data_dir, lang_code, "questionnaire_200.json")
        if os.path.exists(q_path):
            with open(q_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.questionnaire_db = {int(k): v for k, v in data.get("questions", {}).items()}
        
        # 疾病マトリックス
        d_path = os.path.join(self.data_dir, lang_code, "disease_matrix_137.json")
        if os.path.exists(d_path):
            with open(d_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for disease in data.get("disease_matrix", []):
                    self.disease_matrix_db[disease["disease_id"]] = disease
        
        # 漢方ライブラリー（日英統合）
        k_path = os.path.join(self.data_dir, "kampo_metabolic_library.json")
        if os.path.exists(k_path):
            with open(k_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for formula in data.get("formulas", []):
                    self.kampo_db[formula["id"]] = formula
        
        # ファイトケミカル分類（必要に応じて）
        # TODO: ファイトケミカルデータのロード
        
    def _create_risk_factor_mapping(self):
        """リスクファクターと代謝経路のマッピングを作成"""
        self.risk_factor_to_pathway = {
            "irregular": "PATH_01",
            "breakfast_skipping": "PATH_01",
            "late_night_meal": "PATH_01",
            "fast_eating": "PATH_04",
            "high_salt": "PATH_01",
            "high_fat": "PATH_03",
            "alcohol": "PATH_02",
            "high_sugar": "PATH_01",
            "low_vegetables": "PATH_05",
            "stress": "PATH_01"
        }
        
    def analyze(self, 
                questionnaire_responses: Dict[int, bool],
                health_check_data: Optional[HealthCheckData] = None,
                mbt55_profile: Optional[MBT55Profile] = None) -> AnalysisResult:
        """
        統合的健康分析を実行
        
        Args:
            questionnaire_responses: 問診回答（ID -> Yes/No）
            health_check_data: 健康診断データ（オプション）
            mbt55_profile: MBT55プロファイル（オプション）
            
        Returns:
            AnalysisResult: 分析結果
        """
        # 1. 代謝不全の分析
        metabolic_imbalances = self._analyze_metabolic_imbalances(questionnaire_responses)
        
        # 2. 疾病リスクの評価
        disease_risks = self._assess_disease_risks(questionnaire_responses, health_check_data)
        
        # 3. ファイトケミカル推奨の生成
        phytochemical_recs = self._generate_phytochemical_recommendations(disease_risks)
        
        # 4. 漢方処方の推奨
        kampo_recs = self._generate_kampo_recommendations(disease_risks, metabolic_imbalances)
        
        # 5. MBT55最適化プラン
        mbt55_opt = self._optimize_mbt55(mbt55_profile, metabolic_imbalances) if mbt55_profile else {}
        
        # 6. 総合リスクレベルの算出
        overall_risk = self._calculate_overall_risk(disease_risks)
        
        # 7. 食事アドバイスの生成
        dietary_advice = self._generate_dietary_advice(metabolic_imbalances, disease_risks)
        
        return AnalysisResult(
            analysis_id=f"HB-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            language=self.language.value,
            metabolic_imbalances=metabolic_imbalances[:5],
            disease_risks=dict(list(disease_risks.items())[:10]),
            phytochemical_recommendations=phytochemical_recs[:5],
            kampo_recommendations=kampo_recs[:3],
            mbt55_optimization=mbt55_opt,
            overall_risk_level=overall_risk.value,
            dietary_advice=dietary_advice
        )
    
    def _analyze_metabolic_imbalances(self, responses: Dict[int, bool]) -> List[Dict]:
        """問診回答から代謝不全を分析"""
        imbalances = []
        
        for q_id, answer in responses.items():
            if answer and q_id in self.questionnaire_db:
                q = self.questionnaire_db[q_id]
                risk_factors = q.get("risk_factors", [])
                
                for rf in risk_factors:
                    imbalance = {
                        "question_id": q_id,
                        "question": q.get("question", ""),
                        "risk_factor": rf,
                        "metabolic_impact": q.get("metabolic_impact", ""),
                        "pathway": self.risk_factor_to_pathway.get(rf, "PATH_04"),
                        "severity": self._calculate_severity(rf)
                    }
                    imbalances.append(imbalance)
        
        # 重複を統合し、重症度でソート
        return self._merge_imbalances(imbalances)
    
    def _assess_disease_risks(self, 
                              responses: Dict[int, bool],
                              health_data: Optional[HealthCheckData]) -> Dict[str, Dict]:
        """疾病リスクを評価"""
        risks = {}
        
        for disease_id, matrix in self.disease_matrix_db.items():
            risk_score = 0.0
            contributing_factors = []
            
            # 問診回答によるリスク加算
            risk_factors = matrix.get("risk_factors", [])
            for rf in risk_factors:
                # 簡易的なマッチング（実際はより精緻な実装が必要）
                if self._check_risk_factor(rf, responses):
                    risk_score += 0.15
                    contributing_factors.append(rf)
            
            # 健診データによる調整
            if health_data:
                risk_score = self._adjust_with_health_data(risk_score, disease_id, health_data)
            
            # リスクレベルの決定
            risk_level = self._get_risk_level(risk_score)
            
            risks[disease_id] = {
                "disease_name": matrix.get("disease_name", disease_id),
                "risk_score": round(min(risk_score, 1.0), 2),
                "risk_level": risk_level.value,
                "contributing_factors": contributing_factors,
                "metabolic_imbalance": matrix.get("metabolic_impact", ""),
                "mbt55_support": matrix.get("mbt55_support", [])
            }
        
        # リスクスコアでソート
        return dict(sorted(risks.items(), key=lambda x: x[1]["risk_score"], reverse=True))
    
    def _generate_phytochemical_recommendations(self, disease_risks: Dict[str, Dict]) -> List[Dict]:
        """疾病リスクに基づいてファイトケミカルを推奨"""
        recommendations = []
        
        # 上位5疾病のリスクから推奨を生成
        top_diseases = list(disease_risks.keys())[:5]
        
        for disease_id in top_diseases:
            matrix = self.disease_matrix_db.get(disease_id, {})
            phytochemicals = matrix.get("recommended_phytochemicals", [])
            
            for pc_name in phytochemicals:
                if pc_name in self.phytochemical_db:
                    pc = self.phytochemical_db[pc_name]
                    recommendations.append({
                        "disease": disease_id,
                        "phytochemical": pc_name,
                        "food_sources": pc.get("food_sources", [])[:3],
                        "benefits": pc.get("clinical_effects", [])[:2]
                    })
                else:
                    # データベースにない場合はプレースホルダー
                    recommendations.append({
                        "disease": disease_id,
                        "phytochemical": pc_name,
                        "food_sources": ["green leafy vegetables", "colorful fruits"],
                        "benefits": ["antioxidant", "anti-inflammatory"]
                    })
        
        return recommendations
    
    def _generate_kampo_recommendations(self, 
                                        disease_risks: Dict[str, Dict],
                                        metabolic_imbalances: List[Dict]) -> List[Dict]:
        """疾病リスクと代謝不全から漢方処方を推奨"""
        recommendations = []
        
        # 上位3疾病から推奨
        top_diseases = list(disease_risks.keys())[:3]
        
        for disease_id in top_diseases:
            matrix = self.disease_matrix_db.get(disease_id, {})
            kampo_ids = matrix.get("recommended_kampo", [])
            
            for kid in kampo_ids:
                if kid in self.kampo_db:
                    kampo = self.kampo_db[kid]
                    
                    # 言語に応じた名前を選択
                    if self.language == Language.JAPANESE:
                        name = kampo.get("name_ja", kampo.get("name_en", kid))
                        indications = kampo.get("indications", {}).get("primary_ja", [])
                    else:
                        name = kampo.get("name_en", kampo.get("name_ja", kid))
                        indications = kampo.get("indications", {}).get("primary_en", [])
                    
                    recommendations.append({
                        "kampo_id": kid,
                        "name": name,
                        "for_disease": disease_id,
                        "indications": indications[:3],
                        "mbt55_optimization": kampo.get("mbt55_optimization", {}),
                        "bioavailability_boost": kampo.get("mbt55_optimization", {}).get("bioavailability_boost", "unknown")
                    })
        
        return recommendations
    
    def _optimize_mbt55(self, 
                        profile: Optional[MBT55Profile],
                        imbalances: List[Dict]) -> Dict:
        """MBT55プロファイルを最適化"""
        if not profile:
            return {}
        
        optimization = {
            "current_activity": profile.pathway_activity,
            "recommended_boosts": [],
            "targeted_strains": [],
            "prebiotic_support": []
        }
        
        # 活性の低い経路を特定
        for pathway, activity in profile.pathway_activity.items():
            if activity < 0.5:
                optimization["recommended_boosts"].append({
                    "pathway": pathway,
                    "current_activity": activity,
                    "target_activity": min(0.8, activity + 0.3),
                    "boost_strategy": self._get_pathway_boost_strategy(pathway)
                })
        
        # 代謝不全に対応する菌株を推奨
        for imbalance in imbalances[:3]:
            pathway = imbalance.get("pathway", "PATH_04")
            strains = self._get_strains_for_pathway(pathway)
            optimization["targeted_strains"].extend(strains)
        
        # 重複排除
        optimization["targeted_strains"] = list(set(optimization["targeted_strains"]))
        
        return optimization
    
    def _calculate_overall_risk(self, disease_risks: Dict[str, Dict]) -> RiskLevel:
        """総合リスクレベルを計算"""
        high_risks = [r for r in disease_risks.values() if r["risk_score"] > 0.7]
        medium_risks = [r for r in disease_risks.values() if 0.4 <= r["risk_score"] <= 0.7]
        
        if high_risks:
            return RiskLevel.VERY_HIGH if len(high_risks) > 2 else RiskLevel.HIGH
        elif medium_risks:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _generate_dietary_advice(self, 
                                 imbalances: List[Dict],
                                 disease_risks: Dict[str, Dict]) -> List[str]:
        """食事アドバイスを生成"""
        advice = []
        
        # 上位の代謝不全からアドバイス
        advice_map = {
            "irregular": "Establish regular meal times. Eat three meals a day at consistent times.",
            "breakfast_skipping": "Always eat breakfast. Even a banana or yogurt is fine.",
            "late_night_meal": "Finish eating at least 3 hours before bedtime.",
            "fast_eating": "Chew each bite 20 times. Eat slowly and mindfully.",
            "high_salt": "Reduce salt intake. Use herbs and spices for flavor.",
            "high_fat": "Reduce fatty foods. Increase fish and plant-based oils.",
            "low_vegetables": "Aim for 350g of vegetables daily, especially green and yellow vegetables.",
            "low_fluid": "Drink 1.5-2L of water throughout the day."
        }
        
        for imbalance in imbalances[:3]:
            rf = imbalance.get("risk_factor", "")
            if rf in advice_map:
                advice.append(advice_map[rf])
        
        # トップ疾病に基づくアドバイス
        top_disease = list(disease_risks.keys())[0] if disease_risks else None
        if top_disease:
            advice.append(f"Based on your {top_disease.replace('_', ' ')} risk, focus on anti-inflammatory foods and consult a specialist.")
        
        return advice[:5]
    
    # ==================== ヘルパーメソッド ====================
    
    def _calculate_severity(self, risk_factor: str) -> str:
        """リスクファクターの重症度を計算"""
        high_risk = ["high_salt", "high_fat", "alcohol", "high_sugar", "stress"]
        if risk_factor in high_risk:
            return "high"
        return "medium"
    
    def _check_risk_factor(self, risk_factor: str, responses: Dict[int, bool]) -> bool:
        """リスクファクターが問診回答に存在するか確認"""
        # 簡易実装 - 実際はより精緻なマッピングが必要
        return risk_factor in ["irregular", "breakfast_skipping", "high_salt", "high_fat"]
    
    def _adjust_with_health_data(self, 
                                 risk_score: float, 
                                 disease_id: str,
                                 health_data: HealthCheckData) -> float:
        """健診データでリスクスコアを調整"""
        # 糖尿病の場合の調整例
        if disease_id == "diabetes_mellitus":
            if "血糖" in health_data.blood_tests:
                glucose = health_data.blood_tests["血糖"]
                if glucose > 126:
                    risk_score += 0.3
                elif glucose > 100:
                    risk_score += 0.15
        
        # 高血圧の場合の調整例
        if disease_id == "hypertension":
            if "血圧_最高" in health_data.basic_metrics:
                bp = health_data.basic_metrics["血圧_最高"]
                if bp > 140:
                    risk_score += 0.3
                elif bp > 130:
                    risk_score += 0.15
        
        return min(risk_score, 1.0)
    
    def _get_risk_level(self, score: float) -> RiskLevel:
        """スコアからリスクレベルを取得"""
        if score >= 0.7:
            return RiskLevel.HIGH
        elif score >= 0.4:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _merge_imbalances(self, imbalances: List[Dict]) -> List[Dict]:
        """代謝不全の重複を統合"""
        merged = {}
        for item in imbalances:
            key = item["risk_factor"]
            if key not in merged or item["severity"] == "high":
                merged[key] = item
        return sorted(merged.values(), key=lambda x: x["severity"], reverse=True)
    
    def _get_pathway_boost_strategy(self, pathway: str) -> str:
        """経路ブースト戦略を取得"""
        strategies = {
            "PATH_01": "Increase water-soluble fiber and sulfur-containing foods",
            "PATH_02": "Consume foods rich in iron and manganese",
            "PATH_03": "Take fat-soluble vitamins with healthy fats",
            "PATH_04": "Use fermented foods and aromatic herbs",
            "PATH_05": "Increase polysaccharides (beta-glucan, pectin)"
        }
        return strategies.get(pathway, "Maintain a balanced diet and regular lifestyle")
    
    def _get_strains_for_pathway(self, pathway: str) -> List[str]:
        """経路に対応するMBT55菌株を取得"""
        strains = {
            "PATH_01": ["MBT55-001", "MBT55-002"],
            "PATH_02": ["MBT55-002", "MBT55-004"],
            "PATH_03": ["MBT55-005"],
            "PATH_04": ["MBT55-003", "MBT55-004"],
            "PATH_05": ["MBT55-004", "MBT55-005"]
        }
        return strains.get(pathway, ["MBT55-001", "MBT55-004"])
