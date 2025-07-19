#!/usr/bin/env python3
"""
Test Environment Variables Loading
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Environment Variables Test:")
print("="*40)

print(f"FLUX_API_KEY: {os.getenv('FLUX_API_KEY', 'Not set')}")
print(f"BFL_API_KEY: {os.getenv('BFL_API_KEY', 'Not set')}")

# Check if any API key is available
api_key = os.getenv("FLUX_API_KEY") or os.getenv("BFL_API_KEY")
print(f"Available API key: {api_key[:8] + '...' if api_key and api_key != 'your_api_key_here' else 'Not set or default'}") 