# Granite Docling Serverless sur Runpod - Version Complète

Ce projet déploie IBM Granite Docling comme une fonction serverless sur Runpod avec **TOUTES** les fonctionnalités avancées pour la conversion de documents de bout en bout.

## 🚀 Fonctionnalités Complètes

### 🎯 **Conversion de Documents**
- **Formats supportés** : PDF, DOCX, DOC, TXT, HTML, PNG, JPG, JPEG, TIFF
- **Sorties** : Markdown, HTML avec structure préservée
- **Conversion depuis URL** ou **données base64**

### 🖼️ **Descriptions d'Images en Français**
- **Génération automatique** de descriptions d'images en français
- **Modèle BLIP** pour la reconnaissance d'images
- **Traduction** français ↔ anglais
- **Analyse de contenu visuel** (graphiques, diagrammes, photos)

### 🧮 **Enrichissement des Formules Mathématiques**
- **Reconnaissance** des formules LaTeX et mathématiques
- **Classification** des types de formules (arithmétique, équations, exponentielles)
- **Descriptions** en français et anglais
- **Conversion** vers format LaTeX standardisé

### 📊 **Analyse Avancée des Tableaux**
- **Détection automatique** des tableaux
- **Analyse de structure** (lignes, colonnes, en-têtes)
- **Classification** des types de données
- **Conversion** en format Markdown/HTML structuré

### 🌍 **OCR Multilingue**
- **Support de 11 langues** : Français, Anglais, Allemand, Espagnol, Italien, Portugais, Néerlandais, Russe, Chinois, Japonais, Coréen
- **Reconnaissance optimisée** pour documents multilingues
- **Détection automatique** de la langue

### 📈 **Enrichissement de Contenu**
- **Statistiques** du document (mots, caractères, paragraphes)
- **Score de lisibilité** automatique
- **Détection du type** de contenu
- **Analyse de structure** (titres, listes, sections)

### 🔄 **Traitement par Lots**
- **Conversion multiple** de documents en une seule requête
- **Support mixte** URL + base64
- **Résultats détaillés** par document

### ⚡ **Performance et Scalabilité**
- **Serverless** : Scaling automatique sur Runpod
- **GPU Support** : Utilisation optimale des GPU
- **Cache intelligent** : Réutilisation des modèles
- **Timeout configurable** : Jusqu'à 5 minutes

## 📋 Prérequis

- Compte Runpod avec accès aux GPU
- Docker installé
- Python 3.11+
- Runpod CLI

## 🛠️ Installation

### 1. Cloner le projet

```bash
git clone <votre-repo>
cd Docling_Granite_Serverless_Runpod
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Installer Runpod CLI

```bash
pip install runpod
```

### 4. Se connecter à Runpod

```bash
runpod login
```

## 🚀 Déploiement

### Déploiement automatique

```bash
./deploy.sh
```

### Déploiement manuel

1. **Construire l'image Docker** :
```bash
docker build -t granite-docling:latest .
```

2. **Tagger pour Runpod** :
```bash
docker tag granite-docling:latest runpod.io/granite-docling:latest
```

3. **Pousser vers Runpod** :
```bash
docker push runpod.io/granite-docling:latest
```

4. **Déployer la fonction serverless** :
```bash
runpod serverless deploy \
    --name granite-docling-serverless \
    --image runpod.io/granite-docling:latest \
    --handler main.runpod_handler \
    --timeout 300 \
    --memory 16Gi \
    --gpu 1 \
    --cpu 4
```

## 🧪 Test local

### Démarrer l'API localement

```bash
python main.py
```

L'API sera disponible sur `http://localhost:8000`

### Exécuter les tests

```bash
python test_local.py
```

## 📚 Utilisation de la Fonction Serverless

### Paramètres d'Entrée Complets

#### 1. Conversion depuis URL avec toutes les fonctionnalités
```json
{
  "input": {
    "document_url": "https://example.com/document.pdf",
    "output_format": "markdown",
    "include_images": true,
    "include_tables": true,
    "include_image_descriptions": true,
    "include_formula_enrichment": true,
    "ocr_languages": ["fra", "eng"],
    "enhance_content": true
  }
}
```

#### 2. Conversion depuis base64 avec enrichissement
```json
{
  "input": {
    "document_base64": "BASE64_ENCODED_DATA",
    "filename": "document.pdf",
    "output_format": "html",
    "include_image_descriptions": true,
    "include_formula_enrichment": true,
    "ocr_languages": ["fra", "eng", "deu"],
    "enhance_content": true
  }
}
```

#### 3. Traitement par lots
```json
{
  "input": {
    "documents": [
      {
        "url": "https://example.com/doc1.pdf"
      },
      {
        "base64": "BASE64_DATA",
        "filename": "doc2.pdf"
      }
    ],
    "output_format": "markdown",
    "include_image_descriptions": true,
    "include_formula_enrichment": true
  }
}
```

#### 4. Informations sur les modèles
```json
{
  "input": {
    "get_model_info": true
  }
}
```

### Réponse Complète avec Toutes les Fonctionnalités

```json
{
  "success": true,
  "content": "Contenu du document converti...",
  "output_format": "markdown",
  "source": "url",
  "source_url": "https://example.com/document.pdf",
  "enhanced_features": [
    "image_descriptions",
    "formula_enrichment",
    "table_analysis",
    "content_enhancement",
    "structure_analysis"
  ],
  "image_descriptions": [
    {
      "index": 0,
      "description_fr": "Graphique montrant l'évolution des ventes",
      "description_en": "Chart showing sales evolution"
    }
  ],
  "formula_enrichments": [
    {
      "original": "E = mc^2",
      "enriched": {
        "formula": "E = mc^2",
        "type": "equation",
        "description_fr": "Équation mathématique",
        "description_en": "Mathematical equation",
        "latex": "$E = mc^2$"
      },
      "position": [100, 108]
    }
  ],
  "table_analysis": [
    {
      "index": 0,
      "type": "data_table",
      "description_fr": "Tableau avec en-têtes",
      "description_en": "Table with headers",
      "rows": 5,
      "columns": 3,
      "has_headers": true,
      "summary": "Tableau de 5 lignes et 3 colonnes"
    }
  ],
  "content_enhancement": {
    "statistics": {
      "word_count": 1250,
      "character_count": 7500,
      "line_count": 45,
      "paragraph_count": 12
    },
    "content_type": "document_with_tables",
    "language_detected": "fr",
    "readability_score": 75.5
  },
  "document_structure": {
    "sections": [],
    "headings": [
      {
        "text": "Introduction",
        "level": 1
      }
    ],
    "lists": [],
    "figures": [],
    "tables": [],
    "formulas": []
  },
  "metadata": {
    "file_path": "/tmp/document.pdf",
    "processing_time": 2.5,
    "features_used": [
      "image_descriptions",
      "formula_enrichment",
      "table_analysis",
      "content_enhancement",
      "structure_analysis"
    ]
  }
}
```

### Exemples d'Utilisation avec curl

```bash
# Conversion complète depuis URL
curl -X POST https://api.runpod.ai/v2/granite-docling-serverless/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "input": {
      "document_url": "https://example.com/document.pdf",
      "output_format": "markdown",
      "include_image_descriptions": true,
      "include_formula_enrichment": true,
      "ocr_languages": ["fra", "eng"],
      "enhance_content": true
    }
  }'

# Conversion depuis base64
curl -X POST https://api.runpod.ai/v2/granite-docling-serverless/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "input": {
      "document_base64": "BASE64_DATA",
      "filename": "document.pdf",
      "include_image_descriptions": true,
      "include_formula_enrichment": true
    }
  }'

# Informations sur les modèles
curl -X POST https://api.runpod.ai/v2/granite-docling-serverless/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "input": {
      "get_model_info": true
    }
  }'
```

## 🔧 Configuration

### Variables d'environnement

- `CUDA_VISIBLE_DEVICES` : GPU à utiliser (défaut: 0)
- `TRANSFORMERS_CACHE` : Cache des modèles (défaut: /app/models)
- `HF_HOME` : Dossier Hugging Face (défaut: /app/models)

### Configuration Runpod

Le fichier `runpod_config.yaml` contient la configuration pour le déploiement serverless :

- **GPU** : 1 GPU avec 24Gi de mémoire
- **CPU** : 4 cœurs
- **RAM** : 16Gi
- **Timeout** : 5 minutes
- **Scaling** : 0-10 instances

## 📊 Modèles supportés

- **granite-docling-1.5b** : Modèle compact pour usage général
- **granite-docling-3b** : Modèle plus large pour meilleure qualité

## 🎯 Formats supportés

### Entrée
- PDF
- DOCX/DOC
- Images (PNG, JPG, TIFF)
- HTML
- TXT

### Sortie
- Markdown
- HTML

## 🔍 Fonctionnalités avancées

### OCR (Reconnaissance optique de caractères)
- Reconnaissance automatique du texte dans les images
- Support multi-langues
- Amélioration de la qualité d'image

### Extraction de tableaux
- Détection automatique des tableaux
- Conversion en format Markdown/HTML
- Préservation de la structure

### Extraction d'images
- Détection et extraction des images
- Intégration dans le document de sortie
- Support des légendes

## 🚨 Dépannage

### Problèmes courants

1. **Erreur GPU** : Vérifiez que CUDA est installé et configuré
2. **Mémoire insuffisante** : Augmentez la mémoire allouée dans la configuration
3. **Timeout** : Augmentez le timeout pour les gros documents
4. **Modèle non trouvé** : Vérifiez la connexion internet pour télécharger les modèles

### Logs

Les logs sont disponibles dans :
- Console Runpod
- Fichiers de log locaux
- Endpoint `/health` pour le statut

## 📈 Monitoring

### Métriques disponibles

- Temps de traitement
- Utilisation GPU/CPU
- Taux de succès
- Latence

### Surveillance

```bash
# Vérifier le statut
curl https://api.runpod.ai/v2/granite-docling-serverless/status

# Voir les logs
runpod logs granite-docling-serverless
```

## 💰 Coûts

### Facturation Runpod

- **GPU** : Facturé par seconde d'utilisation
- **Mémoire** : Facturée par Go-heure
- **Réseau** : Facturé par Go transféré

### Optimisation des coûts

- Utilisez le scaling automatique
- Optimisez la taille des documents
- Cachez les modèles pour éviter les re-téléchargements

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🆘 Support

- **Documentation IBM** : [Granite Docling](https://www.ibm.com/granite/docs/models/granite-docling/)
- **Runpod Docs** : [Documentation Runpod](https://docs.runpod.io/)
- **Issues** : Ouvrez une issue sur GitHub

## 🔄 Mises à jour

Pour mettre à jour le déploiement :

```bash
# Reconstruire et redéployer
./deploy.sh

# Ou mise à jour manuelle
docker build -t granite-docling:latest .
docker tag granite-docling:latest runpod.io/granite-docling:latest
docker push runpod.io/granite-docling:latest
runpod serverless update granite-docling-serverless --image runpod.io/granite-docling:latest
```

---

**Note** : Ce projet utilise IBM Granite Docling et nécessite un accès aux modèles IBM. Assurez-vous d'avoir les permissions appropriées avant le déploiement.
