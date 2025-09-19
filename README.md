# Granite Docling Serverless on Runpod - Complete Version

This project deploys IBM Granite Docling as a serverless function on Runpod with **ALL** advanced features for end-to-end document conversion.

## 🚀 Complete Features

### 🎯 **Document Conversion**
- **Supported formats**: PDF, DOCX, DOC, TXT, HTML, PNG, JPG, JPEG, TIFF
- **Outputs**: Markdown, HTML with preserved structure
- **Conversion from URL** or **base64 data**

### 🖼️ **French Image Descriptions**
- **Automatic generation** of image descriptions in French
- **BLIP model** for image recognition
- **Translation** French ↔ English
- **Visual content analysis** (charts, diagrams, photos)

### 🧮 **Mathematical Formula Enrichment**
- **Recognition** of LaTeX and mathematical formulas
- **Classification** of formula types (arithmetic, equations, exponential)
- **Descriptions** in French and English
- **Conversion** to standardized LaTeX format

### 📊 **Advanced Table Analysis**
- **Automatic detection** of tables
- **Structure analysis** (rows, columns, headers)
- **Data type classification**
- **Conversion** to structured Markdown/HTML format

### 🌍 **Multilingual OCR**
- **Support for 11 languages**: French, English, German, Spanish, Italian, Portuguese, Dutch, Russian, Chinese, Japanese, Korean
- **Optimized recognition** for multilingual documents
- **Automatic language detection**

### 📈 **Content Enhancement**
- **Document statistics** (words, characters, paragraphs)
- **Automatic readability score**
- **Content type detection**
- **Structure analysis** (headings, lists, sections)

### 🔄 **Batch Processing**
- **Multiple document conversion** in a single request
- **Mixed support** URL + base64
- **Detailed results** per document

### ⚡ **Performance and Scalability**
- **Serverless**: Automatic scaling on Runpod
- **GPU Support**: Optimal GPU utilization
- **Smart caching**: Model reuse
- **Configurable timeout**: Up to 5 minutes

## 📋 Prerequisites

- Runpod account with GPU access
- Docker installed
- Python 3.11+
- Runpod CLI

## 🛠️ Installation

### 1. Clone the project

```bash
git clone https://github.com/RolandVrignon/granite_docling_serverless_runpod.git
cd granite_docling_serverless_runpod
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Runpod CLI

```bash
pip install runpod
```

### 4. Connect to Runpod

```bash
runpod login
```

## 🚀 Deployment

### Automatic deployment via GitHub

The project is configured for automatic deployment from GitHub:

1. **Push to main branch** triggers automatic build
2. **Runpod detects changes** and builds Docker image
3. **Serverless function deploys** automatically
4. **Endpoint becomes available** at: `https://api.runpod.ai/v2/granite_docling_serverless_runpod`

### Manual deployment

```bash
# Build Docker image
docker build -t granite-docling-serverless:latest .

# Tag for Runpod registry
docker tag granite-docling-serverless:latest runpod.io/granite-docling-serverless:latest

# Push to Runpod registry
docker push runpod.io/granite-docling-serverless:latest

# Deploy serverless function
runpod serverless deploy \
    --name granite-docling-serverless \
    --image runpod.io/granite-docling-serverless:latest \
    --handler handler.handler \
    --timeout 300 \
    --memory 16Gi \
    --gpu 1 \
    --cpu 4
```

## 🧪 Local Testing

### Start local testing

```bash
python examples.py
```

### Test serverless handler

```bash
python test_serverless.py
```

## 📚 Serverless Function Usage

### Complete Input Parameters

#### 1. URL conversion with all features
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

#### 2. Base64 conversion with enrichment
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

#### 3. Batch processing
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

#### 4. Model information
```json
{
  "input": {
    "get_model_info": true
  }
}
```

### Complete Response with All Features

```json
{
  "success": true,
  "content": "Converted document content...",
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

### Usage Examples with curl

```bash
# Complete conversion from URL
curl -X POST https://api.runpod.ai/v2/granite_docling_serverless_runpod/runsync \
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

# Base64 conversion
curl -X POST https://api.runpod.ai/v2/granite_docling_serverless_runpod/runsync \
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

# Model information
curl -X POST https://api.runpod.ai/v2/granite_docling_serverless_runpod/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "input": {
      "get_model_info": true
    }
  }'
```

## 🔧 Configuration

### Environment Variables

- `CUDA_VISIBLE_DEVICES`: GPU to use (default: 0)
- `TRANSFORMERS_CACHE`: Model cache (default: /app/models)
- `HF_HOME`: Hugging Face folder (default: /app/models)
- `LOG_LEVEL`: Logging level (default: INFO)

### Runpod Configuration

The `serverless_config.yaml` file contains the serverless deployment configuration:

- **GPU**: 1 GPU with 24Gi memory
- **CPU**: 4 cores
- **RAM**: 16Gi
- **Timeout**: 5 minutes
- **Scaling**: 0-10 instances

## 📊 Supported Models

- **granite-docling-1.5b**: Compact model for general use
- **granite-docling-3b**: Larger model for better quality
- **BLIP**: Image description model
- **TrOCR**: Formula recognition model

## 🎯 Supported Formats

### Input
- PDF
- DOCX/DOC
- Images (PNG, JPG, TIFF)
- HTML
- TXT

### Output
- Markdown
- HTML

## 🔍 Advanced Features

### OCR (Optical Character Recognition)
- Automatic text recognition in images
- Multi-language support
- Image quality enhancement

### Table Extraction
- Automatic table detection
- Conversion to Markdown/HTML format
- Structure preservation

### Image Extraction
- Image detection and extraction
- Integration in output document
- Caption support

### Formula Recognition
- Mathematical expression detection
- LaTeX format conversion
- Formula type classification

## 🚨 Troubleshooting

### Common Issues

1. **GPU Error**: Check that CUDA is installed and configured
2. **Insufficient Memory**: Increase allocated memory in configuration
3. **Timeout**: Increase timeout for large documents
4. **Model Not Found**: Check internet connection for model downloads

### Logs

Logs are available in:
- Runpod Console
- Local log files
- `/health` endpoint for status

## 📈 Monitoring

### Available Metrics

- Processing time
- GPU/CPU usage
- Success rate
- Latency

### Monitoring

```bash
# Check status
curl https://api.runpod.ai/v2/granite_docling_serverless_runpod/status

# View logs
runpod logs granite_docling_serverless_runpod
```

## 💰 Costs

### Runpod Billing

- **GPU**: Billed per second of usage
- **Memory**: Billed per GB-hour
- **Network**: Billed per GB transferred

### Cost Optimization

- Use automatic scaling
- Optimize document sizes
- Cache models to avoid re-downloads

## 🤝 Contributing

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for more details.

## 🆘 Support

- **IBM Documentation**: [Granite Docling](https://www.ibm.com/granite/docs/models/granite-docling/)
- **Runpod Docs**: [Runpod Documentation](https://docs.runpod.io/)
- **Issues**: Open an issue on GitHub

## 🔄 Updates

To update the deployment:

```bash
# Rebuild and redeploy
git add .
git commit -m "Update: description of changes"
git push origin main

# Or manual update
docker build -t granite-docling-serverless:latest .
docker tag granite-docling-serverless:latest runpod.io/granite-docling-serverless:latest
docker push runpod.io/granite-docling-serverless:latest
runpod serverless update granite-docling-serverless --image runpod.io/granite-docling-serverless:latest
```

## 🎯 Key Features Summary

✅ **French image descriptions** with automatic translation
✅ **Complete mathematical formula enrichment**
✅ **Advanced table analysis** with metadata
✅ **Multilingual OCR** with 11 supported languages
✅ **Content enhancement** with statistics and scores
✅ **Batch processing** for multiple documents
✅ **Complete document structure analysis**

---

**Note**: This project uses IBM Granite Docling and requires access to IBM models. Make sure you have the appropriate permissions before deployment.
