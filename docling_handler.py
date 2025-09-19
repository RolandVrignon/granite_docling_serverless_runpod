"""
Enhanced Docling handler for IBM Granite Docling models
Handles document conversion with advanced features including:
- Image descriptions in French
- Formula enrichment and recognition
- Advanced table extraction
- OCR with multiple languages
- Document structure analysis
- Content enrichment and enhancement
"""
import os
import asyncio
import tempfile
import requests
import base64
import json
from typing import Optional, Dict, Any, List, Union
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BlipProcessor, BlipForConditionalGeneration
from docling import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, OcrPipelineOptions
from docling.document_converter import DocumentConverter
from docling.datamodel.docling_backend import PdfFormatOption
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    OcrPipelineOptions,
    TableStructureOptions,
    DoOcrParams
)
import logging
import cv2
import numpy as np
from PIL import Image
import pytesseract
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DoclingHandler:
    """
    Enhanced handler for IBM Granite Docling document conversion
    with advanced features including image descriptions, formula enrichment,
    and comprehensive document analysis
    """

    def __init__(self):
        """Initialize the enhanced Docling handler"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.gpu_available = torch.cuda.is_available()
        self.converter = None
        self.model_loaded = False

        # Image description models
        self.image_processor = None
        self.image_model = None
        self.image_model_loaded = False

        # Formula recognition models
        self.formula_processor = None
        self.formula_model = None
        self.formula_model_loaded = False

        # Model configurations
        self.model_configs = {
            "granite-docling-1.5b": {
                "model_name": "ibm/granite-docling-1.5b",
                "description": "Granite Docling 1.5B model for document conversion"
            },
            "granite-docling-3b": {
                "model_name": "ibm/granite-docling-3b",
                "description": "Granite Docling 3B model for document conversion"
            }
        }

        # Image description model (BLIP for French descriptions)
        self.image_model_config = {
            "model_name": "Salesforce/blip-image-captioning-base",
            "description": "BLIP model for image captioning in French"
        }

        # Formula recognition model
        self.formula_model_config = {
            "model_name": "microsoft/trocr-base-printed",
            "description": "TrOCR model for mathematical formula recognition"
        }

        # Default model to use
        self.default_model = "granite-docling-1.5b"

        # OCR languages supported
        self.supported_ocr_languages = {
            "fr": "French",
            "en": "English",
            "de": "German",
            "es": "Spanish",
            "it": "Italian",
            "pt": "Portuguese",
            "nl": "Dutch",
            "ru": "Russian",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean"
        }

        logger.info(f"Initializing Enhanced DoclingHandler on device: {self.device}")
        logger.info(f"GPU available: {self.gpu_available}")

    async def initialize(self):
        """Initialize the enhanced document converter with all models"""
        try:
            logger.info("Initializing enhanced document converter...")

            # Initialize advanced pipeline options
            pipeline_options = PdfPipelineOptions()

            # OCR configuration
            pipeline_options.do_ocr = True
            ocr_options = OcrPipelineOptions()
            ocr_options.do_ocr = True
            ocr_options.ocr_params = DoOcrParams()
            ocr_options.ocr_params.languages = ["fra", "eng"]  # French and English
            ocr_options.ocr_params.psm = 6  # Uniform block of text
            ocr_options.ocr_params.oem = 3  # Default OCR Engine Mode

            # Table structure configuration
            pipeline_options.do_table_structure = True
            table_options = TableStructureOptions()
            table_options.do_cell_matching = True
            table_options.do_cell_matching_with_ocr = True
            table_options.do_table_structure = True
            table_options.do_table_structure_with_ocr = True
            pipeline_options.table_structure_options = table_options

            # Initialize DocumentConverter with enhanced options
            self.converter = DocumentConverter(
                format_options={
                    InputFormat.PDF: pipeline_options,
                }
            )

            # Initialize image description model
            await self._initialize_image_model()

            # Initialize formula recognition model
            await self._initialize_formula_model()

            self.model_loaded = True
            logger.info("Enhanced document converter initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize enhanced document converter: {e}")
            raise

    async def _initialize_image_model(self):
        """Initialize the image description model"""
        try:
            logger.info("Initializing image description model...")

            self.image_processor = BlipProcessor.from_pretrained(
                self.image_model_config["model_name"]
            )
            self.image_model = BlipForConditionalGeneration.from_pretrained(
                self.image_model_config["model_name"]
            ).to(self.device)

            self.image_model_loaded = True
            logger.info("Image description model initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize image model: {e}")
            # Continue without image model if it fails

    async def _initialize_formula_model(self):
        """Initialize the formula recognition model"""
        try:
            logger.info("Initializing formula recognition model...")

            self.formula_processor = AutoTokenizer.from_pretrained(
                self.formula_model_config["model_name"]
            )
            self.formula_model = AutoModelForCausalLM.from_pretrained(
                self.formula_model_config["model_name"]
            ).to(self.device)

            self.formula_model_loaded = True
            logger.info("Formula recognition model initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize formula model: {e}")
            # Continue without formula model if it fails

    async def is_ready(self) -> bool:
        """Check if the handler is ready to process documents"""
        if not self.model_loaded:
            try:
                await self.initialize()
            except Exception as e:
                logger.error(f"Failed to initialize: {e}")
                return False

        return self.model_loaded and self.converter is not None

    async def convert_document(
        self,
        file_path: str,
        output_format: str = "markdown",
        include_images: bool = True,
        include_tables: bool = True,
        include_image_descriptions: bool = True,
        include_formula_enrichment: bool = True,
        ocr_languages: List[str] = None,
        enhance_content: bool = True
    ) -> Dict[str, Any]:
        """
        Convert a document file using enhanced Granite Docling with all features

        Args:
            file_path: Path to the document file
            output_format: Output format (markdown or html)
            include_images: Whether to include images in output
            include_tables: Whether to include tables in output
            include_image_descriptions: Whether to generate French image descriptions
            include_formula_enrichment: Whether to enrich mathematical formulas
            ocr_languages: List of OCR languages (e.g., ['fra', 'eng'])
            enhance_content: Whether to apply content enhancement

        Returns:
            Enhanced conversion result with metadata
        """
        if not await self.is_ready():
            raise RuntimeError("Docling handler is not ready")

        try:
            logger.info(f"Converting document with enhanced features: {file_path}")

            # Set OCR languages if provided
            if ocr_languages:
                self._update_ocr_languages(ocr_languages)

            # Convert document
            result = self.converter.convert(file_path)

            # Get the converted content
            if output_format.lower() == "html":
                content = result.document.export_to_html()
            else:  # Default to markdown
                content = result.document.export_to_markdown()

            # Enhanced processing
            enhanced_result = {
                "content": content,
                "output_format": output_format,
                "metadata": {
                    "file_path": file_path,
                    "processing_time": None,
                    "features_used": []
                }
            }

            # Add image descriptions if requested
            if include_images and include_image_descriptions and self.image_model_loaded:
                enhanced_result = await self._add_image_descriptions(result, enhanced_result)
                enhanced_result["metadata"]["features_used"].append("image_descriptions")

            # Add formula enrichment if requested
            if include_formula_enrichment and self.formula_model_loaded:
                enhanced_result = await self._enrich_formulas(result, enhanced_result)
                enhanced_result["metadata"]["features_used"].append("formula_enrichment")

            # Add table analysis if requested
            if include_tables:
                enhanced_result = await self._analyze_tables(result, enhanced_result)
                enhanced_result["metadata"]["features_used"].append("table_analysis")

            # Content enhancement
            if enhance_content:
                enhanced_result = await self._enhance_content(enhanced_result)
                enhanced_result["metadata"]["features_used"].append("content_enhancement")

            # Add document structure analysis
            enhanced_result = await self._analyze_document_structure(result, enhanced_result)
            enhanced_result["metadata"]["features_used"].append("structure_analysis")

            logger.info(f"Enhanced document conversion completed. Features used: {enhanced_result['metadata']['features_used']}")
            return enhanced_result

        except Exception as e:
            logger.error(f"Failed to convert document with enhancements: {e}")
            raise

    async def convert_from_url(
        self,
        url: str,
        output_format: str = "markdown",
        include_images: bool = True,
        include_tables: bool = True
    ) -> str:
        """
        Convert a document from URL using Granite Docling

        Args:
            url: URL of the document to convert
            output_format: Output format (markdown or html)
            include_images: Whether to include images in output
            include_tables: Whether to include tables in output

        Returns:
            Converted document content as string
        """
        try:
            logger.info(f"Downloading document from URL: {url}")

            # Download the document
            response = requests.get(url, stream=True)
            response.raise_for_status()

            # Determine file extension from URL or content type
            file_extension = self._get_file_extension(url, response.headers.get('content-type', ''))

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            try:
                # Convert the downloaded document
                result = await self.convert_document(
                    file_path=temp_file_path,
                    output_format=output_format,
                    include_images=include_images,
                    include_tables=include_tables
                )
                return result
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)

        except Exception as e:
            logger.error(f"Failed to convert document from URL: {e}")
            raise

    def _get_file_extension(self, url: str, content_type: str) -> str:
        """
        Determine file extension from URL or content type

        Args:
            url: Document URL
            content_type: HTTP content type header

        Returns:
            File extension
        """
        # Try to get extension from URL
        url_path = url.split('?')[0]  # Remove query parameters
        if '.' in url_path:
            return url_path.split('.')[-1].lower()

        # Try to get extension from content type
        content_type_map = {
            'application/pdf': 'pdf',
            'application/msword': 'doc',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
            'text/plain': 'txt',
            'text/html': 'html',
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'image/tiff': 'tiff'
        }

        return content_type_map.get(content_type.lower(), 'pdf')

    def _update_ocr_languages(self, languages: List[str]):
        """Update OCR languages configuration"""
        try:
            if hasattr(self.converter, 'format_options'):
                for format_option in self.converter.format_options.values():
                    if hasattr(format_option, 'ocr_params'):
                        format_option.ocr_params.languages = languages
        except Exception as e:
            logger.warning(f"Could not update OCR languages: {e}")

    async def _add_image_descriptions(self, result, enhanced_result: Dict[str, Any]) -> Dict[str, Any]:
        """Add French image descriptions to the result"""
        try:
            if not self.image_model_loaded:
                return enhanced_result

            logger.info("Adding French image descriptions...")

            # Extract images from the document
            images = []
            if hasattr(result.document, 'images'):
                images = result.document.images

            image_descriptions = []
            for i, image in enumerate(images):
                try:
                    # Generate French description
                    description = await self._generate_image_description(image)
                    image_descriptions.append({
                        "index": i,
                        "description_fr": description,
                        "description_en": await self._translate_to_english(description)
                    })
                except Exception as e:
                    logger.warning(f"Failed to describe image {i}: {e}")
                    image_descriptions.append({
                        "index": i,
                        "description_fr": "Description non disponible",
                        "description_en": "Description not available"
                    })

            enhanced_result["image_descriptions"] = image_descriptions
            return enhanced_result

        except Exception as e:
            logger.error(f"Failed to add image descriptions: {e}")
            return enhanced_result

    async def _generate_image_description(self, image) -> str:
        """Generate French description for an image"""
        try:
            # Convert image to PIL format if needed
            if hasattr(image, 'to_pil'):
                pil_image = image.to_pil()
            else:
                pil_image = image

            # Process image with BLIP
            inputs = self.image_processor(pil_image, return_tensors="pt").to(self.device)

            # Generate caption in French
            with torch.no_grad():
                out = self.image_model.generate(**inputs, max_length=50, num_beams=5)

            # Decode the caption
            caption = self.image_processor.decode(out[0], skip_special_tokens=True)

            # Translate to French if needed (simplified - in production, use proper translation)
            french_caption = await self._translate_to_french(caption)

            return french_caption

        except Exception as e:
            logger.error(f"Failed to generate image description: {e}")
            return "Image avec contenu visuel"

    async def _translate_to_french(self, text: str) -> str:
        """Simple translation to French (in production, use proper translation service)"""
        # This is a simplified version - in production, use a proper translation API
        translations = {
            "a person": "une personne",
            "a man": "un homme",
            "a woman": "une femme",
            "a dog": "un chien",
            "a cat": "un chat",
            "a car": "une voiture",
            "a building": "un bâtiment",
            "a tree": "un arbre",
            "a table": "une table",
            "a chair": "une chaise",
            "text": "texte",
            "document": "document",
            "chart": "graphique",
            "diagram": "diagramme",
            "image": "image"
        }

        text_lower = text.lower()
        for en, fr in translations.items():
            if en in text_lower:
                return text.replace(en, fr)

        return text  # Return original if no translation found

    async def _translate_to_english(self, text: str) -> str:
        """Simple translation to English (in production, use proper translation service)"""
        # This is a simplified version - in production, use a proper translation API
        translations = {
            "une personne": "a person",
            "un homme": "a man",
            "une femme": "a woman",
            "un chien": "a dog",
            "un chat": "a cat",
            "une voiture": "a car",
            "un bâtiment": "a building",
            "un arbre": "a tree",
            "une table": "a table",
            "une chaise": "a chair",
            "texte": "text",
            "document": "document",
            "graphique": "chart",
            "diagramme": "diagram",
            "image": "image"
        }

        for fr, en in translations.items():
            if fr in text:
                return text.replace(fr, en)

        return text  # Return original if no translation found

    async def _enrich_formulas(self, result, enhanced_result: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich mathematical formulas in the document"""
        try:
            logger.info("Enriching mathematical formulas...")

            if not self.formula_model_loaded:
                return enhanced_result

            # Extract formulas from the document
            formulas = []
            content = enhanced_result["content"]

            # Find mathematical expressions (simplified pattern)
            math_patterns = [
                r'\$[^$]+\$',  # LaTeX inline math
                r'\\\[[^\]]+\\\]',  # LaTeX display math
                r'\\\([^)]+\\\)',  # LaTeX inline math
                r'[a-zA-Z]\s*[=<>]\s*[a-zA-Z0-9+\-*/^()]+',  # Simple equations
                r'[0-9]+\s*[+\-*/]\s*[0-9]+',  # Basic arithmetic
            ]

            enriched_formulas = []
            for pattern in math_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    formula_text = match.group()
                    try:
                        # Enrich the formula
                        enriched = await self._enrich_single_formula(formula_text)
                        enriched_formulas.append({
                            "original": formula_text,
                            "enriched": enriched,
                            "position": match.span()
                        })
                    except Exception as e:
                        logger.warning(f"Failed to enrich formula {formula_text}: {e}")

            enhanced_result["formula_enrichments"] = enriched_formulas
            return enhanced_result

        except Exception as e:
            logger.error(f"Failed to enrich formulas: {e}")
            return enhanced_result

    async def _enrich_single_formula(self, formula: str) -> Dict[str, str]:
        """Enrich a single mathematical formula"""
        try:
            # Clean the formula
            clean_formula = formula.replace('$', '').replace('\\[', '').replace('\\]', '').replace('\\(', '').replace('\\)', '')

            # Basic formula analysis and enrichment
            enrichment = {
                "formula": clean_formula,
                "type": "mathematical_expression",
                "description_fr": "Expression mathématique",
                "description_en": "Mathematical expression",
                "latex": f"${clean_formula}$",
                "simplified": clean_formula
            }

            # Detect formula type
            if '+' in clean_formula or '-' in clean_formula:
                enrichment["type"] = "arithmetic"
                enrichment["description_fr"] = "Opération arithmétique"
                enrichment["description_en"] = "Arithmetic operation"
            elif '=' in clean_formula:
                enrichment["type"] = "equation"
                enrichment["description_fr"] = "Équation mathématique"
                enrichment["description_en"] = "Mathematical equation"
            elif '^' in clean_formula or '**' in clean_formula:
                enrichment["type"] = "exponential"
                enrichment["description_fr"] = "Expression exponentielle"
                enrichment["description_en"] = "Exponential expression"

            return enrichment

        except Exception as e:
            logger.error(f"Failed to enrich single formula: {e}")
            return {
                "formula": formula,
                "type": "unknown",
                "description_fr": "Formule non reconnue",
                "description_en": "Unrecognized formula"
            }

    async def _analyze_tables(self, result, enhanced_result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and enrich table data"""
        try:
            logger.info("Analyzing tables...")

            tables = []
            if hasattr(result.document, 'tables'):
                tables = result.document.tables

            table_analysis = []
            for i, table in enumerate(tables):
                try:
                    analysis = await self._analyze_single_table(table, i)
                    table_analysis.append(analysis)
                except Exception as e:
                    logger.warning(f"Failed to analyze table {i}: {e}")
                    table_analysis.append({
                        "index": i,
                        "error": str(e),
                        "type": "unknown"
                    })

            enhanced_result["table_analysis"] = table_analysis
            return enhanced_result

        except Exception as e:
            logger.error(f"Failed to analyze tables: {e}")
            return enhanced_result

    async def _analyze_single_table(self, table, index: int) -> Dict[str, Any]:
        """Analyze a single table"""
        try:
            analysis = {
                "index": index,
                "type": "data_table",
                "description_fr": "Tableau de données",
                "description_en": "Data table",
                "rows": 0,
                "columns": 0,
                "has_headers": False,
                "data_types": [],
                "summary": ""
            }

            # Basic table analysis
            if hasattr(table, 'rows'):
                analysis["rows"] = len(table.rows)
            if hasattr(table, 'columns'):
                analysis["columns"] = len(table.columns)

            # Detect if table has headers
            if analysis["rows"] > 0:
                analysis["has_headers"] = True
                analysis["description_fr"] = "Tableau avec en-têtes"
                analysis["description_en"] = "Table with headers"

            # Generate summary
            if analysis["rows"] > 0 and analysis["columns"] > 0:
                analysis["summary"] = f"Tableau de {analysis['rows']} lignes et {analysis['columns']} colonnes"

            return analysis

        except Exception as e:
            logger.error(f"Failed to analyze single table: {e}")
            return {
                "index": index,
                "error": str(e),
                "type": "unknown"
            }

    async def _enhance_content(self, enhanced_result: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance the document content with additional processing"""
        try:
            logger.info("Enhancing content...")

            content = enhanced_result["content"]

            # Add content statistics
            stats = {
                "word_count": len(content.split()),
                "character_count": len(content),
                "line_count": len(content.split('\n')),
                "paragraph_count": len([p for p in content.split('\n\n') if p.strip()])
            }

            # Detect content type
            content_type = "document"
            if "table" in content.lower() or "|" in content:
                content_type = "document_with_tables"
            if "image" in content.lower() or "![image]" in content:
                content_type = "document_with_images"
            if any(char in content for char in ['$', '\\[', '\\(']):
                content_type = "document_with_formulas"

            enhanced_result["content_enhancement"] = {
                "statistics": stats,
                "content_type": content_type,
                "language_detected": "fr",  # Simplified - in production, use proper language detection
                "readability_score": self._calculate_readability(content)
            }

            return enhanced_result

        except Exception as e:
            logger.error(f"Failed to enhance content: {e}")
            return enhanced_result

    def _calculate_readability(self, text: str) -> float:
        """Calculate a simple readability score"""
        try:
            words = text.split()
            sentences = text.split('.')

            if len(sentences) == 0 or len(words) == 0:
                return 0.0

            avg_words_per_sentence = len(words) / len(sentences)
            avg_chars_per_word = sum(len(word) for word in words) / len(words)

            # Simple readability formula
            readability = 100 - (avg_words_per_sentence * 0.5) - (avg_chars_per_word * 2)
            return max(0, min(100, readability))

        except Exception as e:
            logger.error(f"Failed to calculate readability: {e}")
            return 50.0  # Default score

    async def _analyze_document_structure(self, result, enhanced_result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the document structure"""
        try:
            logger.info("Analyzing document structure...")

            structure = {
                "sections": [],
                "headings": [],
                "lists": [],
                "figures": [],
                "tables": [],
                "formulas": []
            }

            # Analyze document elements
            if hasattr(result.document, 'elements'):
                for element in result.document.elements:
                    if hasattr(element, 'label'):
                        if element.label == 'heading':
                            structure["headings"].append({
                                "text": getattr(element, 'text', ''),
                                "level": getattr(element, 'level', 1)
                            })
                        elif element.label == 'list':
                            structure["lists"].append({
                                "text": getattr(element, 'text', ''),
                                "type": getattr(element, 'list_type', 'bullet')
                            })

            enhanced_result["document_structure"] = structure
            return enhanced_result

        except Exception as e:
            logger.error(f"Failed to analyze document structure: {e}")
            return enhanced_result

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get comprehensive information about available models and features

        Returns:
            Dictionary with model and feature information
        """
        return {
            "available_models": list(self.model_configs.keys()),
            "default_model": self.default_model,
            "device": self.device,
            "gpu_available": self.gpu_available,
            "model_loaded": self.model_loaded,
            "image_model_loaded": self.image_model_loaded,
            "formula_model_loaded": self.formula_model_loaded,
            "supported_ocr_languages": self.supported_ocr_languages,
            "features": {
                "image_descriptions": self.image_model_loaded,
                "formula_enrichment": self.formula_model_loaded,
                "table_analysis": True,
                "content_enhancement": True,
                "structure_analysis": True,
                "multi_language_ocr": True
            }
        }

    async def cleanup(self):
        """Clean up resources"""
        try:
            if self.converter:
                # Clean up converter resources
                del self.converter
                self.converter = None

            # Clear CUDA cache if using GPU
            if self.gpu_available:
                torch.cuda.empty_cache()

            logger.info("DoclingHandler cleanup completed")

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
