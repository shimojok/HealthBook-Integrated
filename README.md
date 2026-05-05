> [!NOTE]
> **This repository has been archived.**
> 
> このリポジトリはアーカイブされました。最新の人体フェノミクスエンジンは以下の後継リポジトリを参照してください。
> 
> 🩺 [**HealthBook-AI**](https://github.com/shimojok/HealthBook-AI) — 137 diseases × 293 Kampo × 200 questionnaire causal inference engine
> 

---

# HealthBook-Integrated

**Integrated Health Inference Platform combining Hamada Questionnaire × Disease Matrix × MBT Kampo Metabolic Library**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Overview

HealthBook-Integrated is a comprehensive health inference system that integrates three core components:

1. **Hamada 200-Item Questionnaire** - 30 years of clinical data from 300,000+ patients
2. **137 Disease Matrix** - Diet-disease correlation mapping
3. **MBT Kampo Metabolic Library** - 293 Kampo formulas with phytochemical analysis

The system provides personalized health recommendations including metabolic analysis, disease risk assessment, phytochemical suggestions, Kampo formula recommendations, and MBT55 probiotic optimization.

## Repository Structure

```
HealthBook-Integrated/
├── README.md                          # This file
├── README.ja.md                       # Japanese version
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── data/
│   ├── en/                            # English data
│   │   ├── questionnaire_200.json     # 200-questionnaire (English)
│   │   └── disease_matrix_137.json    # 137-disease matrix (English)
│   ├── ja/                            # Japanese data
│   │   ├── questionnaire_200.json     # 200-questionnaire (Japanese)
│   │   └── disease_matrix_137.json    # 137-disease matrix (Japanese)
│   └── kampo_metabolic_library.json   # 293 Kampo formulas (bilingual)
├── src/healthbook/
│   ├── __init__.py
│   ├── engine.py                      # Main inference engine
│   ├── disease_risk.py                # Disease risk predictor
│   ├── phytochemical_recommender.py   # Phytochemical recommender
│   └── kampo_mapper.py                # Kampo formula mapper
├── examples/
│   ├── healthbook_demo.py             # Complete demo script
│   └── mbt55_integration.py           # MBT55 integration demo
└── tests/
    └── test_engine.py                 # Unit tests
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/shimojok/HealthBook-Integrated.git
cd HealthBook-Integrated

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from src.healthbook import HealthBookEngine, Language

# Initialize engine (English)
engine = HealthBookEngine(language=Language.ENGLISH)

# Questionnaire responses (question_id -> Yes/No)
responses = {
    1: True,   # Meal times are irregular
    2: True,   # Often skip breakfast
    9: True,   # Prefer salty foods
    55: True,  # Lack of exercise
    60: True,  # Prone to stress
}

# Run analysis
result = engine.analyze(questionnaire_responses=responses)

# Display results
print(f"Overall Risk Level: {result.overall_risk_level}")
print(f"Top Disease Risk: {list(result.disease_risks.keys())[0]}")
```

## Features

### 1. Metabolic Imbalance Analysis
Identifies metabolic issues from questionnaire responses, mapping each risk factor to specific metabolic pathways (PATH_01 to PATH_05).

### 2. Disease Risk Prediction
Evaluates 137 diseases using the Hamada Disease Matrix, calculating risk scores based on 40+ dietary and lifestyle patterns.

### 3. Phytochemical Recommendations
Suggests beneficial phytochemicals based on detected disease risks, with food sources and MBT55 pathway mapping.

### 4. Kampo Formula Recommendations
Recommends traditional Kampo formulas from the 293-formula MBT Kampo Metabolic Library, including MBT55 optimization parameters.

### 5. MBT55 Optimization
Provides personalized probiotic strain recommendations and fermentation protocols.

## API Reference

### HealthBookEngine

| Method | Description |
|--------|-------------|
| `__init__(language=Language.ENGLISH)` | Initialize engine with language |
| `analyze(questionnaire_responses, health_check_data=None, mbt55_profile=None)` | Run comprehensive analysis |

### DiseaseRiskPredictor

| Method | Description |
|--------|-------------|
| `predict(risk_factors)` | Predict disease risks from risk factors |
| `get_top_risks(risk_factors, top_n=10)` | Get top N disease risks |

### PhytochemicalRecommender

| Method | Description |
|--------|-------------|
| `recommend_for_disease(disease_id, top_n=5)` | Recommend for specific disease |
| `get_food_sources(phytochemical_name)` | Get food sources for phytochemical |

### KampoMapper

| Method | Description |
|--------|-------------|
| `search_by_symptom(symptom, language="en")` | Search formulas by symptom |
| `recommend_by_disease(disease_id, top_n=3)` | Recommend formulas by disease |
| `get_mbt55_optimization(formula_id)` | Get MBT55 optimization info |

## Data Sources

| Component | Source | Description |
|-----------|--------|-------------|
| Questionnaire | Hamada Method | 200 items, 30+ years clinical data |
| Disease Matrix | Hamada Method | 137 diseases × 40+ lifestyle patterns |
| Kampo Library | MBT Kampo v2.44 | 293 formulas with phytochemical analysis |
| Phytochemicals | Shimojo Classification | Polyphenols, carotenoids, sulfur compounds |

## Integration with M3-BioSynergy

This repository works alongside [M3-BioSynergy](https://github.com/shimojok/M3-BioSynergy), which implements:

- Microbial diversity models (120-species)
- Hypercycle engines for carbon sequestration
- Nutrient cascade simulations

Use HealthBook-Integrated for personalized health recommendations and M3-BioSynergy for ecological/agricultural applications.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

**Kazuhiko Shimojo** - BioNexus Holdings Co-Founder, Japan Supplement Association (former board member)

## Related Repositories

- [M3-BioSynergy](https://github.com/shimojok/M3-BioSynergy) - Microbial-Metabolic-Modular Theory

## Citation

If you use this software in your research, please cite:

```
bibtex
@software{Shimojo_HealthBook_Integrated_2025,
  author = {Shimojo, Kazuhiko},
  title = {HealthBook-Integrated: Health Inference Platform},
  year = {2025},
  url = {https://github.com/shimojok/HealthBook-Integrated}
}
```
