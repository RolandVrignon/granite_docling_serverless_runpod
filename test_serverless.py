"""
Test script for the serverless handler
"""
import json
import base64
from handler import handler

def test_url_conversion():
    """Test document conversion from URL"""
    print("🧪 Testing URL conversion...")

    event = {
        "input": {
            "document_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "output_format": "markdown",
            "include_images": True,
            "include_tables": True
        }
    }

    result = handler(event)
    print(f"Result: {json.dumps(result, indent=2)}")

    if result.get("success"):
        print("✅ URL conversion test passed")
        print(f"Content length: {len(result.get('content', ''))}")
    else:
        print(f"❌ URL conversion test failed: {result.get('error')}")

def test_base64_conversion():
    """Test document conversion from base64"""
    print("\n🧪 Testing base64 conversion...")

    # Create a simple test document (you can replace this with actual file)
    test_content = b"Test document content"
    test_base64 = base64.b64encode(test_content).decode('utf-8')

    event = {
        "input": {
            "document_base64": test_base64,
            "filename": "test.txt",
            "output_format": "markdown",
            "include_images": True,
            "include_tables": True
        }
    }

    result = handler(event)
    print(f"Result: {json.dumps(result, indent=2)}")

    if result.get("success"):
        print("✅ Base64 conversion test passed")
    else:
        print(f"❌ Base64 conversion test failed: {result.get('error')}")

def test_batch_conversion():
    """Test batch document conversion"""
    print("\n🧪 Testing batch conversion...")

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
            "include_images": True,
            "include_tables": True
        }
    }

    result = handler(event)
    print(f"Result: {json.dumps(result, indent=2)}")

    if result.get("success"):
        print("✅ Batch conversion test passed")
        print(f"Total documents: {result.get('total_documents')}")
        print(f"Successful conversions: {result.get('successful_conversions')}")
    else:
        print(f"❌ Batch conversion test failed: {result.get('error')}")

def test_invalid_input():
    """Test with invalid input"""
    print("\n🧪 Testing invalid input...")

    event = {
        "input": {
            "invalid_field": "test"
        }
    }

    result = handler(event)
    print(f"Result: {json.dumps(result, indent=2)}")

    if not result.get("success"):
        print("✅ Invalid input test passed (correctly failed)")
    else:
        print("❌ Invalid input test failed (should have failed)")

def test_empty_input():
    """Test with empty input"""
    print("\n🧪 Testing empty input...")

    event = {
        "input": {}
    }

    result = handler(event)
    print(f"Result: {json.dumps(result, indent=2)}")

    if not result.get("success"):
        print("✅ Empty input test passed (correctly failed)")
    else:
        print("❌ Empty input test failed (should have failed)")

def main():
    """Run all tests"""
    print("🚀 Starting serverless handler tests...\n")

    # Test URL conversion
    test_url_conversion()

    # Test base64 conversion
    test_base64_conversion()

    # Test batch conversion
    test_batch_conversion()

    # Test invalid input
    test_invalid_input()

    # Test empty input
    test_empty_input()

    print("\n🏁 All tests completed!")

if __name__ == "__main__":
    main()
