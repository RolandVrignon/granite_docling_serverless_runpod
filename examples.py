"""
Exemples d'utilisation complets pour Granite Docling Serverless
avec toutes les fonctionnalités avancées
"""
import json
import base64
from handler import handler

def example_basic_conversion():
    """Exemple de conversion basique depuis une URL"""
    print("🔍 Exemple: Conversion basique depuis URL")

    event = {
        "input": {
            "document_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "output_format": "markdown"
        }
    }

    result = handler(event)
    print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

def example_full_featured_conversion():
    """Exemple de conversion avec toutes les fonctionnalités avancées"""
    print("\n🚀 Exemple: Conversion avec toutes les fonctionnalités")

    event = {
        "input": {
            "document_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "output_format": "markdown",
            "include_images": True,
            "include_tables": True,
            "include_image_descriptions": True,
            "include_formula_enrichment": True,
            "ocr_languages": ["fra", "eng"],
            "enhance_content": True
        }
    }

    result = handler(event)
    print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

def example_base64_conversion():
    """Exemple de conversion depuis base64 avec enrichissement"""
    print("\n📄 Exemple: Conversion depuis base64 avec enrichissement")

    # Créer un document de test simple
    test_content = b"Document de test avec des formules: E = mc^2 et des tableaux."
    test_base64 = base64.b64encode(test_content).decode('utf-8')

    event = {
        "input": {
            "document_base64": test_base64,
            "filename": "test_document.txt",
            "output_format": "markdown",
            "include_image_descriptions": True,
            "include_formula_enrichment": True,
            "enhance_content": True
        }
    }

    result = handler(event)
    print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

def example_multilingual_ocr():
    """Exemple avec OCR multilingue"""
    print("\n🌍 Exemple: OCR multilingue (français et anglais)")

    event = {
        "input": {
            "document_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "output_format": "markdown",
            "ocr_languages": ["fra", "eng", "deu"],
            "include_image_descriptions": True,
            "enhance_content": True
        }
    }

    result = handler(event)
    print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

def example_formula_enrichment():
    """Exemple avec enrichissement de formules mathématiques"""
    print("\n🧮 Exemple: Enrichissement de formules mathématiques")

    # Créer un document avec des formules
    test_content = b"""
    Document scientifique avec formules:

    Équation d'Einstein: E = mc^2
    Formule quadratique: x = (-b ± √(b²-4ac)) / 2a
    Intégrale: ∫ f(x) dx
    Limite: lim(x→0) sin(x)/x = 1
    """
    test_base64 = base64.b64encode(test_content).decode('utf-8')

    event = {
        "input": {
            "document_base64": test_base64,
            "filename": "formulas.pdf",
            "output_format": "markdown",
            "include_formula_enrichment": True,
            "enhance_content": True
        }
    }

    result = handler(event)
    print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

def example_table_analysis():
    """Exemple avec analyse de tableaux"""
    print("\n📊 Exemple: Analyse de tableaux")

    # Créer un document avec des tableaux
    test_content = b"""
    Rapport financier:

    | Année | Revenus | Dépenses | Profit |
    |-------|---------|----------|--------|
    | 2020  | 100000  | 80000    | 20000  |
    | 2021  | 120000  | 90000    | 30000  |
    | 2022  | 150000  | 110000   | 40000  |

    Tableau des ventes par région:
    - Europe: 45%
    - Amérique: 35%
    - Asie: 20%
    """
    test_base64 = base64.b64encode(test_content).decode('utf-8')

    event = {
        "input": {
            "document_base64": test_base64,
            "filename": "financial_report.pdf",
            "output_format": "markdown",
            "include_tables": True,
            "enhance_content": True
        }
    }

    result = handler(event)
    print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

def example_batch_processing():
    """Exemple de traitement par lots"""
    print("\n📦 Exemple: Traitement par lots")

    event = {
        "input": {
            "documents": [
                {
                    "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
                },
                {
                    "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
                }
            ],
            "output_format": "markdown",
            "include_image_descriptions": True,
            "include_formula_enrichment": True,
            "enhance_content": True
        }
    }

    result = handler(event)
    print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

def example_model_info():
    """Exemple pour obtenir les informations sur les modèles"""
    print("\nℹ️ Exemple: Informations sur les modèles")

    event = {
        "input": {
            "get_model_info": True
        }
    }

    result = handler(event)
    print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

def example_custom_configuration():
    """Exemple avec configuration personnalisée"""
    print("\n⚙️ Exemple: Configuration personnalisée")

    event = {
        "input": {
            "document_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "output_format": "html",
            "include_images": True,
            "include_tables": True,
            "include_image_descriptions": True,
            "include_formula_enrichment": True,
            "ocr_languages": ["fra", "eng", "spa"],
            "enhance_content": True
        }
    }

    result = handler(event)
    print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

def example_error_handling():
    """Exemple de gestion d'erreurs"""
    print("\n❌ Exemple: Gestion d'erreurs")

    # Test avec URL invalide
    event = {
        "input": {
            "document_url": "https://invalid-url-that-does-not-exist.com/document.pdf",
            "output_format": "markdown"
        }
    }

    result = handler(event)
    print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

def run_all_examples():
    """Exécuter tous les exemples"""
    print("🎯 Exécution de tous les exemples Granite Docling Serverless\n")

    examples = [
        ("Conversion basique", example_basic_conversion),
        ("Conversion complète", example_full_featured_conversion),
        ("Conversion base64", example_base64_conversion),
        ("OCR multilingue", example_multilingual_ocr),
        ("Enrichissement formules", example_formula_enrichment),
        ("Analyse tableaux", example_table_analysis),
        ("Traitement par lots", example_batch_processing),
        ("Infos modèles", example_model_info),
        ("Configuration personnalisée", example_custom_configuration),
        ("Gestion d'erreurs", example_error_handling)
    ]

    results = {}

    for name, example_func in examples:
        try:
            print(f"\n{'='*60}")
            print(f"Exécution: {name}")
            print('='*60)
            result = example_func()
            results[name] = result.get("success", False)
        except Exception as e:
            print(f"❌ Erreur dans {name}: {e}")
            results[name] = False

    # Résumé
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ DES EXEMPLES")
    print('='*60)

    successful = sum(1 for success in results.values() if success)
    total = len(results)

    for name, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {name}")

    print(f"\n🎯 Résultat: {successful}/{total} exemples réussis")

    return results

if __name__ == "__main__":
    # Exécuter tous les exemples
    run_all_examples()

    # Ou exécuter un exemple spécifique
    # example_full_featured_conversion()
