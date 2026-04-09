"""
疾病リスク予測エンジン

137疾病マトリックスに基づくリスク評価
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import os


@dataclass
class DiseaseRisk:
    """疾病リスク情報"""
    disease_id: str
    disease_name: str
    risk_score: float
    risk_level: str
    contributing_factors: List[str]
    metabolic_insight: str
    mbt55_support: List[str]


class DiseaseRiskPredictor:
    """
    疾病リスク予測エンジン
    
    浜田式疾病マトリックス（137疾病 × 40食生活パターン）に基づき、
    問診回答から疾病リスクを計算する。
    """
    
    def __init__(self, data_dir: str = None, language: str = "en"):
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), "../../data")
        self.language = language
        self.disease_matrix: Dict[str, Dict] = {}
        self.risk_factor_weights: Dict[str, float] = {}
        
        self._load_data()
        self._initialize_weights()
    
    def _load_data(self):
        """疾病マトリックスデータをロード"""
        path = os.path.join(self.data_dir, self.language, "disease_matrix_137.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for disease in data.get("disease_matrix", []):
                    self.disease_matrix[disease["disease_id"]] = disease
    
    def _initialize_weights(self):
        """リスクファクターの重みを初期化"""
        self.risk_factor_weights = {
            "irregular": 0.70,
            "breakfast_skipping": 0.85,
            "late_night_meal": 0.80,
            "fast_eating": 0.75,
            "overeating": 0.78,
            "high_salt": 0.90,
            "high_fat": 0.88,
            "alcohol": 0.90,
            "heavy_drinking": 0.88,
            "high_sugar": 0.92,
            "low_vegetables": 0.80,
            "stress": 0.90,
            "physical_inactivity": 0.92,
            "sleep_deficiency": 0.85
        }
    
    def predict(self, risk_factors: List[str]) -> List[DiseaseRisk]:
        """
        リスクファクターから疾病リスクを予測
        
        Args:
            risk_factors: 抽出されたリスクファクターのリスト
            
        Returns:
            List[DiseaseRisk]: リスク順にソートされた疾病リスク
        """
        risks = {}
        
        for disease_id, matrix in self.disease_matrix.items():
            risk_score = 0.0
            contributing = []
            
            # マトリックスのリスクファクターと一致するものを加算
            matrix_factors = matrix.get("risk_factors", [])
            for rf in risk_factors:
                if rf in matrix_factors:
                    weight = self.risk_factor_weights.get(rf, 0.50)
                    risk_score += weight
                    contributing.append(rf)
            
            # スコアを正規化（最大1.0）
            risk_score = min(risk_score, 1.0)
            
            if risk_score > 0:
                risks[disease_id] = DiseaseRisk(
                    disease_id=disease_id,
                    disease_name=matrix.get("disease_name", disease_id),
                    risk_score=risk_score,
                    risk_level=self._get_risk_level(risk_score),
                    contributing_factors=contributing,
                    metabolic_insight=matrix.get("metabolic_impact", ""),
                    mbt55_support=matrix.get("mbt55_support", [])
                )
        
        # リスクスコアでソート
        return sorted(risks.values(), key=lambda x: x.risk_score, reverse=True)
    
    def get_top_risks(self, risk_factors: List[str], top_n: int = 10) -> List[DiseaseRisk]:
        """上位N個の疾病リスクを取得"""
        all_risks = self.predict(risk_factors)
        return all_risks[:top_n]
    
    def _get_risk_level(self, score: float) -> str:
        """スコアからリスクレベルを取得"""
        if score >= 0.7:
            return "high"
        elif score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def get_disease_details(self, disease_id: str) -> Optional[Dict]:
        """疾病の詳細情報を取得"""
        return self.disease_matrix.get(disease_id)
