"""
HealthBook-Integrated: 統合ヘルスケア推論システム

浜田式問診 × 137疾病マトリックス × MBT漢方代謝ライブラリー
"""

__version__ = "1.0.0"
__author__ = "Kazuhiko Shimojo"

from .engine import HealthBookEngine
from .disease_risk import DiseaseRiskPredictor
from .phytochemical_recommender import PhytochemicalRecommender
from .kampo_mapper import KampoMapper

__all__ = [
    "HealthBookEngine",
    "DiseaseRiskPredictor", 
    "PhytochemicalRecommender",
    "KampoMapper"
]
