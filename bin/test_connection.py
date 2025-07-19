#!/usr/bin/env python3
"""
Test API Connection Script.

This script tests the connection to the FLUX API before running generation.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.api.client import FluxAPIClient
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


def test_api_connection():
    """Test API connection with multiple attempts."""
    print("🔍 Testing FLUX API connection...")
    
    # Test multiple times to ensure stability
    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1}/3...")
            
            client = FluxAPIClient()
            result = client.test_connection()
            
            if result:
                print("✅ API connection successful!")
                return True
            else:
                print("❌ API connection failed")
                if attempt < 2:
                    print("🔄 Retrying in 5 seconds...")
                    time.sleep(5)
                    
        except Exception as e:
            print(f"❌ Error testing connection: {e}")
            if attempt < 2:
                print("🔄 Retrying in 5 seconds...")
                time.sleep(5)
    
    print("❌ All connection attempts failed")
    return False


def main():
    """Main function."""
    if test_api_connection():
        print("\n🎉 Connection test passed! You can now run generation.")
        return 0
    else:
        print("\n💥 Connection test failed! Please check your API key and internet connection.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 