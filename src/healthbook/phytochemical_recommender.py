"""
ファイトケミカル推奨エンジン

下條式ファイトケミカル分類に基づく栄養推奨
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import os


@dataclass
class PhytochemicalRecommendation:
    """ファイトケミカル推奨"""
    name: str
    category: str
    defense_type: str
    food_sources: List[str]
    benefits: List[str]
    mbt_pathway: str


class PhytochemicalRecommender:
    """
    ファイトケミカル推奨エンジン
    
    下條式ファイトケミカル分類に基づき、疾病リスクに応じた
    ファイトケミカルと食品を推奨する。
    """
    
    # 下條式防御タイプ
    DEFENSE_TYPES = {
        "hydrophilic": "水溶性防御（体液・血液保護）",
        "lipophilic": "脂溶性防御（細胞膜・脂質保護）",
        "sulfur": "イオウ化合物（循環・抗菌）"
    }
    
    # 疾病とファイトケミカルのマッピング
    DISEASE_PHYTOCHEMICAL_MAP = {
        "hypertension": ["potassium_rich_vegetables", "sesamin", "rutin", "taurine"],
        "diabetes_mellitus": ["chlorogenic_acid", "isoflavone", "catechin", "beta_glucan"],
        "hyperlipidemia": ["sesamin", "catechin", "isoflavone", "allicin"],
        "fatty_liver": ["sesamin", "catechin", "curcumin", "taurine"],
        "atherosclerosis": ["anthocyanin", "quercetin", "lycopene", "lutein"],
        "gastritis": ["curcumin", "catechin", "gingerol", "rosmarinic_acid"],
        "constipation": ["dietary_fiber", "pectin", "beta_glucan"],
        "insomnia": ["gaba", "l_theanine", "apigenin"],
        "anxiety": ["gaba", "l_theanine", "rosmarinic_acid"],
        "osteoporosis": ["isoflavone", "vitamin_k", "calcium"],
        "anemia": ["iron_rich_vegetables", "vitamin_c", "folate"],
        "allergy": ["quercetin", "catechin", "rosmarinic_acid"]
    }
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), "../../data")
        self.phytochemical_db: Dict[str, Dict] = {}
        self._load_data()
    
    def _load_data(self):
        """ファイトケミカルデータをロード"""
        # TODO: ファイトケミカルJSONからロード
        # 現時点では組み込みデータを使用
        self._init_builtin_database()
    
    def _init_builtin_database(self):
        """組み込みファイトケミカルデータベース"""
        self.phytochemical_db = {
            "anthocyanin": {
                "name": "Anthocyanin",
                "category": "Polyphenol / Flavonoid",
                "defense_type": "hydrophilic",
                "food_sources": ["blueberries", "grapes", "eggplant skin", "purple sweet potato"],
                "benefits": ["antioxidant", "anti-inflammatory", "eye health"],
                "mbt_pathway": "PATH_01"
            },
            "quercetin": {
                "name": "Quercetin",
                "category": "Polyphenol / Flavonol",
                "defense_type": "hydrophilic",
                "food_sources": ["onions", "broccoli", "apples", "green tea"],
                "benefits": ["antioxidant", "anti-allergic", "anti-inflammatory"],
                "mbt_pathway": "PATH_01"
            },
            "catechin": {
                "name": "Catechin",
                "category": "Polyphenol / Flavan-3-ol",
                "defense_type": "hydrophilic",
                "food_sources": ["green tea", "black tea", "oolong tea", "cacao"],
                "benefits": ["antioxidant", "metabolism boost", "cardiovascular health"],
                "mbt_pathway": "PATH_05"
            },
            "lycopene": {
                "name": "Lycopene",
                "category": "Carotenoid",
                "defense_type": "lipophilic",
                "food_sources": ["tomatoes", "watermelon", "pink grapefruit"],
                "benefits": ["antioxidant", "prostate health", "skin protection"],
                "mbt_pathway": "PATH_03"
            },
            "lutein": {
                "name": "Lutein",
                "category": "Carotenoid / Xanthophyll",
                "defense_type": "lipophilic",
                "food_sources": ["spinach", "kale", "broccoli", "corn", "egg yolk"],
                "benefits": ["eye health", "cognitive health", "skin health"],
                "mbt_pathway": "PATH_03"
            },
            "curcumin": {
                "name": "Curcumin",
                "category": "Polyphenol / Curcuminoid",
                "defense_type": "lipophilic",
                "food_sources": ["turmeric", "ginger"],
                "benefits": ["anti-inflammatory", "antioxidant", "joint health"],
                "mbt_pathway": "PATH_01"
            },
            "allicin": {
                "name": "Allicin",
                "category": "Sulfur Compound",
                "defense_type": "sulfur",
                "food_sources": ["garlic", "onions"],
                "benefits": ["antibacterial", "cardiovascular health", "immune support"],
                "mbt_pathway": "PATH_01"
            },
            "sesamin": {
                "name": "Sesamin",
                "category": "Lignan",
                "defense_type": "lipophilic",
                "food_sources": ["sesame seeds", "sesame oil"],
                "benefits": ["liver health", "antioxidant", "cholesterol reduction"],
                "mbt_pathway": "PATH_01"
            },
            "isoflavone": {
                "name": "Isoflavone",
                "category": "Polyphenol / Isoflavone",
                "defense_type": "hydrophilic",
                "food_sources": ["soybeans", "tofu", "natto", "soymilk"],
                "benefits": ["menopausal support", "bone health", "cardiovascular health"],
                "mbt_pathway": "PATH_01"
            },
            "chlorogenic_acid": {
                "name": "Chlorogenic Acid",
                "category": "Polyphenol / Phenolic Acid",
                "defense_type": "hydrophilic",
                "food_sources": ["coffee beans", "burdock root", "sweet potato"],
                "benefits": ["blood glucose regulation", "antioxidant"],
                "mbt_pathway": "PATH_01"
            },
            "beta_glucan": {
                "name": "Beta-Glucan",
                "category": "Polysaccharide",
                "defense_type": "hydrophilic",
                "food_sources": ["mushrooms", "oats", "barley"],
                "benefits": ["immune modulation", "cholesterol reduction", "blood glucose regulation"],
                "mbt_pathway": "PATH_05"
            },
            "gaba": {
                "name": "GABA",
                "category": "Amino Acid",
                "defense_type": "hydrophilic",
                "food_sources": ["fermented foods", "tomatoes", "soybeans"],
                "benefits": ["stress reduction", "sleep improvement", "blood pressure regulation"],
                "mbt_pathway": "PATH_04"
            }
        }
    
    def recommend_for_disease(self, disease_id: str, top_n: int = 5) -> List[PhytochemicalRecommendation]:
        """疾病に基づくファイトケミカル推奨"""
        phytochemical_names = self.DISEASE_PHYTOCHEMICAL_MAP.get(disease_id, [])
        recommendations = []
        
        for name in phytochemical_names[:top_n]:
            if name in self.phytochemical_db:
                pc = self.phytochemical_db[name]
                recommendations.append(PhytochemicalRecommendation(
                    name=pc["name"],
                    category=pc["category"],
                    defense_type=pc["defense_type"],
                    food_sources=pc["food_sources"][:3],
                    benefits=pc["benefits"][:2],
                    mbt_pathway=pc["mbt_pathway"]
                ))
        
        return recommendations
    
    def recommend_for_risks(self, disease_risks: List[tuple]) -> List[PhytochemicalRecommendation]:
        """
        複数の疾病リスクに基づくファイトケミカル推奨
        
        Args:
            disease_risks: (disease_id, risk_score) のリスト
            
        Returns:
            List[PhytochemicalRecommendation]: 推奨リスト（重複排除済み）
        """
        all_recommendations = []
        seen = set()
        
        for disease_id, _ in disease_risks[:3]:  # 上位3疾病
            recs = self.recommend_for_disease(disease_id, top_n=3)
            for rec in recs:
                if rec.name not in seen:
                    seen.add(rec.name)
                    all_recommendations.append(rec)
        
        return all_recommendations[:5]
    
    def get_food_sources(self, phytochemical_name: str) -> List[str]:
        """ファイトケミカルを含む食品を取得"""
        pc = self.phytochemical_db.get(phytochemical_name)
        return pc["food_sources"] if pc else []
