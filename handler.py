"""
Runpod Serverless Handler for IBM Granite Docling
This is the main entry point for the serverless function
"""
import os
import tempfile
import asyncio
import json
import logging
from typing import Dict, Any, Optional
import runpod
from docling_handler import DoclingHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global handler instance
docling_handler = None

async def initialize_handler():
    """Initialize the Docling handler once"""
    global docling_handler
    if docling_handler is None:
        logger.info("Initializing Docling handler...")
        docling_handler = DoclingHandler()
        await docling_handler.initialize()
        logger.info("Docling handler initialized successfully")

def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main serverless handler function for Runpod

    Args:
        event: Event data from Runpod containing input parameters

    Returns:
        Response data for Runpod
    """
    try:
        # Initialize handler if not already done
        asyncio.run(initialize_handler())

        # Extract input data
        input_data = event.get("input", {})

        # Validate input
        if not input_data:
            return {
                "error": "No input data provided",
                "success": False
            }

        # Handle different types of requests
        if "document_url" in input_data:
            return handle_url_conversion(input_data)
        elif "document_base64" in input_data:
            return handle_base64_conversion(input_data)
        elif "get_model_info" in input_data:
            return handle_model_info_request()
        else:
            return {
                "error": "Either 'document_url', 'document_base64', or 'get_model_info' must be provided",
                "success": False
            }

    except Exception as e:
        logger.error(f"Handler error: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

def handle_url_conversion(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle enhanced document conversion from URL with all advanced features

    Args:
        input_data: Input parameters containing document_url and options

    Returns:
        Enhanced conversion result with all features
    """
    try:
        # Extract parameters with defaults for all advanced features
        document_url = input_data["document_url"]
        output_format = input_data.get("output_format", "markdown")
        include_images = input_data.get("include_images", True)
        include_tables = input_data.get("include_tables", True)
        include_image_descriptions = input_data.get("include_image_descriptions", True)
        include_formula_enrichment = input_data.get("include_formula_enrichment", True)
        ocr_languages = input_data.get("ocr_languages", ["fra", "eng"])
        enhance_content = input_data.get("enhance_content", True)

        logger.info(f"Converting document from URL with enhanced features: {document_url}")

        # Convert document with all enhancements
        result = asyncio.run(docling_handler.convert_from_url(
            url=document_url,
            output_format=output_format,
            include_images=include_images,
            include_tables=include_tables,
            include_image_descriptions=include_image_descriptions,
            include_formula_enrichment=include_formula_enrichment,
            ocr_languages=ocr_languages,
            enhance_content=enhance_content
        ))

        return {
            "success": True,
            "content": result.get("content", ""),
            "output_format": output_format,
            "source": "url",
            "source_url": document_url,
            "enhanced_features": result.get("metadata", {}).get("features_used", []),
            "image_descriptions": result.get("image_descriptions", []),
            "formula_enrichments": result.get("formula_enrichments", []),
            "table_analysis": result.get("table_analysis", []),
            "content_enhancement": result.get("content_enhancement", {}),
            "document_structure": result.get("document_structure", {}),
            "metadata": result.get("metadata", {})
        }

    except Exception as e:
        logger.error(f"Enhanced URL conversion error: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

def handle_base64_conversion(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle enhanced document conversion from base64 encoded data with all advanced features

    Args:
        input_data: Input parameters containing document_base64 and options

    Returns:
        Enhanced conversion result with all features
    """
    try:
        import base64

        # Extract parameters with defaults for all advanced features
        document_base64 = input_data["document_base64"]
        filename = input_data.get("filename", "document.pdf")
        output_format = input_data.get("output_format", "markdown")
        include_images = input_data.get("include_images", True)
        include_tables = input_data.get("include_tables", True)
        include_image_descriptions = input_data.get("include_image_descriptions", True)
        include_formula_enrichment = input_data.get("include_formula_enrichment", True)
        ocr_languages = input_data.get("ocr_languages", ["fra", "eng"])
        enhance_content = input_data.get("enhance_content", True)

        logger.info(f"Converting document from base64 with enhanced features: {filename}")

        # Decode base64 data
        document_data = base64.b64decode(document_base64)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{filename.split('.')[-1]}") as temp_file:
            temp_file.write(document_data)
            temp_file_path = temp_file.name

        try:
            # Convert document with all enhancements
            result = asyncio.run(docling_handler.convert_document(
                file_path=temp_file_path,
                output_format=output_format,
                include_images=include_images,
                include_tables=include_tables,
                include_image_descriptions=include_image_descriptions,
                include_formula_enrichment=include_formula_enrichment,
                ocr_languages=ocr_languages,
                enhance_content=enhance_content
            ))

            return {
                "success": True,
                "content": result.get("content", ""),
                "output_format": output_format,
                "source": "base64",
                "filename": filename,
                "enhanced_features": result.get("metadata", {}).get("features_used", []),
                "image_descriptions": result.get("image_descriptions", []),
                "formula_enrichments": result.get("formula_enrichments", []),
                "table_analysis": result.get("table_analysis", []),
                "content_enhancement": result.get("content_enhancement", {}),
                "document_structure": result.get("document_structure", {}),
                "metadata": result.get("metadata", {})
            }

        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)

    except Exception as e:
        logger.error(f"Enhanced base64 conversion error: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

def handle_batch_conversion(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle batch document conversion

    Args:
        input_data: Input parameters containing list of documents

    Returns:
        Batch conversion results
    """
    try:
        documents = input_data.get("documents", [])
        output_format = input_data.get("output_format", "markdown")
        include_images = input_data.get("include_images", True)
        include_tables = input_data.get("include_tables", True)

        if not documents:
            return {
                "error": "No documents provided in batch",
                "success": False
            }

        results = []

        for i, doc in enumerate(documents):
            try:
                if "url" in doc:
                    result = handle_url_conversion({
                        "document_url": doc["url"],
                        "output_format": output_format,
                        "include_images": include_images,
                        "include_tables": include_tables
                    })
                elif "base64" in doc:
                    result = handle_base64_conversion({
                        "document_base64": doc["base64"],
                        "filename": doc.get("filename", f"document_{i}.pdf"),
                        "output_format": output_format,
                        "include_images": include_images,
                        "include_tables": include_tables
                    })
                else:
                    result = {
                        "error": "Document must have either 'url' or 'base64' field",
                        "success": False
                    }

                results.append({
                    "index": i,
                    "result": result
                })

            except Exception as e:
                results.append({
                    "index": i,
                    "error": str(e),
                    "success": False
                })

        return {
            "success": True,
            "results": results,
            "total_documents": len(documents),
            "successful_conversions": len([r for r in results if r.get("result", {}).get("success", False)])
        }

    except Exception as e:
        logger.error(f"Batch conversion error: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

def handle_model_info_request() -> Dict[str, Any]:
    """
    Handle model information request

    Returns:
        Model and feature information
    """
    try:
        logger.info("Getting model information...")

        # Get model info from handler
        model_info = docling_handler.get_model_info()

        return {
            "success": True,
            "model_info": model_info,
            "available_features": [
                "image_descriptions_fr",
                "formula_enrichment",
                "table_analysis",
                "content_enhancement",
                "structure_analysis",
                "multi_language_ocr",
                "batch_processing"
            ],
            "supported_formats": {
                "input": ["pdf", "docx", "doc", "txt", "html", "png", "jpg", "jpeg", "tiff"],
                "output": ["markdown", "html"]
            },
            "supported_languages": {
                "ocr": ["fra", "eng", "deu", "spa", "ita", "por", "nld", "rus", "chi", "jpn", "kor"],
                "descriptions": ["fr", "en"]
            }
        }

    except Exception as e:
        logger.error(f"Model info request error: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

# Register the handler with Runpod
if __name__ == "__main__":
    # For local testing
    test_event = {
        "input": {
            "document_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "output_format": "markdown",
            "include_images": True,
            "include_tables": True
        }
    }

    result = handler(test_event)
    print(json.dumps(result, indent=2))
else:
    # Register with Runpod
    runpod.serverless.start({"handler": handler})
