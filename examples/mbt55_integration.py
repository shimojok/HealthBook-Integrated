#!/usr/bin/env python3
"""
MBT55 Integration Demo

このスクリプトは、HealthBook-IntegratedとM3-BioSynergyの連携を示します。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MBT55IntegrationDemo:
    """MBT55連携デモ"""
    
    def __init__(self):
        self.mbt55_strains = {
            "MBT55-001": {
                "name": "Actinobacteria strain",
                "pathway": "PATH_01",
                "functions": ["Deglycation", "Sulfur metabolism", "Alkaloid activation"],
                "optimal_conditions": {"pH": 6.5, "temperature": 37}
            },
            "MBT55-003": {
                "name": "Yeast strain",
                "pathway": "PATH_04",
                "functions": ["Aromatic compound分解", "Neurotransmitter precursor production"],
                "optimal_conditions": {"pH": 5.5, "temperature": 30}
            },
            "MBT55-005": {
                "name": "Bile-acid metabolizing bacteria",
                "pathway": "PATH_03",
                "functions": ["Micellization", "Lipid absorption", "Carotenoid conversion"],
                "optimal_conditions": {"pH": 7.0, "temperature": 37}
            }
        }
        
        self.fermentation_protocols = {
            "standard": {"time": "24 hours", "temperature": "37°C", "pH": "6.5-7.0"},
            "extended": {"time": "36-48 hours", "temperature": "37°C", "pH": "6.5-7.0"},
            "herbal": {"time": "24-36 hours", "temperature": "35-37°C", "pH": "5.5-6.5"}
        }
    
    def get_strain_recommendation(self, pathway: str) -> dict:
        """経路に基づく菌株推奨"""
        for strain_id, info in self.mbt55_strains.items():
            if info["pathway"] == pathway:
                return {"strain_id": strain_id, **info}
        return {"strain_id": "MBT55-001", **self.mbt55_strains["MBT55-001"]}
    
    def create_custom_probiotic(self, kampo_formula: dict) -> dict:
        """漢方処方に基づくカスタムプロバイオティクス処方"""
        strains = []
        
        # 推奨菌株の取得
        for strain_id in kampo_formula.get("mbt55_strains", []):
            if strain_id in self.mbt55_strains:
                strains.append(self.mbt55_strains[strain_id])
        
        if not strains:
            strains = [self.mbt55_strains["MBT55-001"]]
        
        # 発酵プロトコルの選択
        fermentation_time = kampo_formula.get("fermentation_time", "24 hours")
        protocol = self.fermentation_protocols.get(
            "extended" if "36" in fermentation_time else "standard"
        )
        
        return {
            "formula_name": kampo_formula.get("name_en", kampo_formula.get("name_ja", "Unknown")),
            "probiotic_strains": strains,
            "fermentation_protocol": protocol,
            "expected_compounds": kampo_formula.get("enhanced_compounds", []),
            "bioavailability_boost": kampo_formula.get("bioavailability_boost", "2-5x")
        }
    
    def simulate_fermentation(self, formulation: dict) -> dict:
        """発酵シミュレーション（簡易版）"""
        return {
            "status": "success",
            "estimated_yield": "10^9 CFU/g",
            "active_compounds": formulation.get("expected_compounds", [])[:3],
            "quality_score": 0.92
        }


def demo():
    """デモ実行"""
    print("=" * 60)
    print("MBT55 Integration Demo")
    print("=" * 60)
    
    demo_obj = MBT55IntegrationDemo()
    
    # 菌株情報の表示
    print("\n🔬 Available MBT55 Strains:")
    for strain_id, info in demo_obj.mbt55_strains.items():
        print(f"  • {strain_id}: {info['name']}")
        print(f"    Pathway: {info['pathway']}")
        print(f"    Functions: {', '.join(info['functions'][:2])}")
    
    # 経路に基づく推奨
    print("\n📋 Strain Recommendation for PATH_03:")
    rec = demo_obj.get_strain_recommendation("PATH_03")
    print(f"  • {rec['strain_id']}: {rec['name']}")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    demo()
