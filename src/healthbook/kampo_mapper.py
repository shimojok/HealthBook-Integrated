"""
漢方処方マッパー

MBT漢方代謝ライブラリーに基づく処方推奨
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import os


@dataclass
class KampoFormula:
    """漢方処方情報"""
    id: str
    name_ja: str
    name_en: str
    category_ja: str
    category_en: str
    main_herbs_ja: List[str]
    main_herbs_en: List[str]
    indications_ja: List[str]
    indications_en: List[str]
    mbt55_strains: List[str]
    fermentation_time: str
    bioavailability_boost: str


class KampoMapper:
    """
    漢方処方マッパー
    
    症状・疾病から適切な漢方処方を推奨する。
    """
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), "../../data")
        self.formulas: Dict[str, KampoFormula] = {}
        self.symptom_to_kampo: Dict[str, List[str]] = {}
        self.disease_to_kampo: Dict[str, List[str]] = {}
        
        self._load_data()
        self._build_mappings()
    
    def _load_data(self):
        """漢方データをロード"""
        path = os.path.join(self.data_dir, "kampo_metabolic_library.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for formula in data.get("formulas", []):
                    self.formulas[formula["id"]] = KampoFormula(
                        id=formula["id"],
                        name_ja=formula.get("name_ja", ""),
                        name_en=formula.get("name_en", ""),
                        category_ja=formula.get("category_ja", ""),
                        category_en=formula.get("category_en", ""),
                        main_herbs_ja=formula.get("main_herbs_ja", []),
                        main_herbs_en=formula.get("main_herbs_en", []),
                        indications_ja=formula.get("indications", {}).get("primary_ja", []),
                        indications_en=formula.get("indications", {}).get("primary_en", []),
                        mbt55_strains=formula.get("mbt55_optimization", {}).get("recommended_strains", []),
                        fermentation_time=formula.get("mbt55_optimization", {}).get("fermentation_time", ""),
                        bioavailability_boost=formula.get("mbt55_optimization", {}).get("bioavailability_boost", "")
                    )
    
    def _build_mappings(self):
        """症状・疾病と漢方のマッピングを構築"""
        for fid, formula in self.formulas.items():
            # 日本語適応症
            for indication in formula.indications_ja:
                if indication not in self.symptom_to_kampo:
                    self.symptom_to_kampo[indication] = []
                self.symptom_to_kampo[indication].append(fid)
            
            # 英語適応症
            for indication in formula.indications_en:
                if indication not in self.symptom_to_kampo:
                    self.symptom_to_kampo[indication] = []
                self.symptom_to_kampo[indication].append(fid)
    
    def search_by_symptom(self, symptom: str, language: str = "en") -> List[KampoFormula]:
        """
        症状から漢方処方を検索
        
        Args:
            symptom: 症状名（日本語または英語）
            language: 出力言語
            
        Returns:
            List[KampoFormula]: 関連する漢方処方のリスト
        """
        matched_ids = []
        
        for s, fids in self.symptom_to_kampo.items():
            if symptom.lower() in s.lower():
                matched_ids.extend(fids)
        
        # 重複排除
        matched_ids = list(set(matched_ids))
        
        # 処方情報を返す
        return [self.formulas[fid] for fid in matched_ids if fid in self.formulas]
    
    def recommend_by_disease(self, disease_id: str, top_n: int = 3) -> List[KampoFormula]:
        """
        疾病に基づく漢方推奨
        
        Args:
            disease_id: 疾病ID（例: "hypertension", "diabetes_mellitus"）
            top_n: 返す処方数
            
        Returns:
            List[KampoFormula]: 推奨処方リスト
        """
        # 疾病と漢方のマッピング（簡易版）
        disease_formula_map = {
            "hypertension": ["F045", "F062", "F088", "F184"],
            "diabetes_mellitus": ["F018", "F038", "F120", "F235"],
            "hyperlipidemia": ["F084", "F128", "F192"],
            "fatty_liver": ["F084", "F128", "F192", "F256"],
            "gastritis": ["F009", "F046", "F073", "F119", "F186", "F204"],
            "insomnia": ["F007", "F019", "F054", "F140", "F162", "F195", "F280"],
            "anxiety": ["F007", "F019", "F033", "F045", "F123", "F140", "F155", "F203", "F250", "F280"],
            "constipation": ["F031", "F071", "F075", "F077", "F081", "F135", "F170", "F194", "F213"],
            "rhinitis": ["F014", "F025", "F080", "F152", "F167", "F169", "F254", "F268", "F273"],
            "asthma": ["F025", "F029", "F039", "F050", "F133", "F159", "F167", "F212", "F228"],
            "eczema": ["F070", "F079", "F091", "F099", "F164", "F168", "F234", "F238", "F262", "F269", "F287"],
            "cold": ["F001", "F027", "F069", "F073", "F131", "F166", "F211", "F237", "F248", "F252", "F260", "F285"],
            "stiff_shoulders": ["F001", "F028", "F106", "F252", "F254"],
            "edema": ["F004", "F008", "F026", "F041", "F044", "F051", "F095", "F096", "F125", "F126", "F160", "F175", "F247"],
            "dizziness": ["F102", "F118", "F148", "F188", "F199", "F210", "F217", "F245", "F261", "F266"],
            "menopause": ["F015", "F047", "F056", "F092", "F113", "F230", "F270", "F275", "F282"],
            "dysmenorrhea": ["F005", "F035", "F036", "F097", "F103", "F176", "F241", "F264", "F265", "F274"]
        }
        
        formula_ids = disease_formula_map.get(disease_id, [])
        
        # 処方情報を取得
        recommendations = []
        for fid in formula_ids[:top_n]:
            if fid in self.formulas:
                recommendations.append(self.formulas[fid])
        
        return recommendations
    
    def get_formula(self, formula_id: str) -> Optional[KampoFormula]:
        """処方IDから処方情報を取得"""
        return self.formulas.get(formula_id)
    
    def search_by_herb(self, herb_name: str) -> List[KampoFormula]:
        """
        生薬から漢方処方を検索
        
        Args:
            herb_name: 生薬名（日本語または英語）
            
        Returns:
            List[KampoFormula]: その生薬を含む処方リスト
        """
        matched = []
        
        for fid, formula in self.formulas.items():
            herbs_ja = [h for h in formula.main_herbs_ja if herb_name.lower() in h.lower()]
            herbs_en = [h for h in formula.main_herbs_en if herb_name.lower() in h.lower()]
            if herbs_ja or herbs_en:
                matched.append(formula)
        
        return matched
    
    def get_mbt55_optimization(self, formula_id: str) -> Dict:
        """処方のMBT55最適化情報を取得"""
        formula = self.formulas.get(formula_id)
        if not formula:
            return {}
        
        return {
            "recommended_strains": formula.mbt55_strains,
            "fermentation_time": formula.fermentation_time,
            "bioavailability_boost": formula.bioavailability_boost
        }
