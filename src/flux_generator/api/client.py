"""
FLUX API client for image generation.
"""

import requests
import time
import json
from typing import Optional
from pathlib import Path

from ..config.settings import settings
from .models import GenerationRequest, GenerationResponse, APIError


class FluxAPIClient:
    """Client for BFL.ai FLUX API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize API client."""
        self.api_key = api_key or settings.api_key
        if not self.api_key:
            raise ValueError("API key is required")
        
        self.base_url = settings.api.base_url
        self.timeout = settings.api.timeout
        self.max_retries = settings.api.max_retries
        self.retry_delay = settings.api.retry_delay
        
        # Remove quotes if present
        self.api_key = self.api_key.strip('"\'')
        
        self.headers = {
            "x-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def test_connection(self) -> bool:
        """Test API connection."""
        try:
            # Simple test request - just check if we can reach the API
            # We'll use a minimal test that should work
            test_data = {
                "prompt": "test",
                "input_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=",
                "seed": 1000,
                "aspect_ratio": "1:1"
            }
            
            response = requests.post(
                f"{self.base_url}/flux-kontext-pro",
                headers=self.headers,
                json=test_data,
                timeout=10
            )
            
            # If we get any response (even error), the API key is working
            if response.status_code in [200, 400, 422]:  # Success or validation errors
                return True
            elif response.status_code == 403:
                raise APIError(403, "Access denied. Check API key.")
            else:
                # Any other response means the API is reachable
                return True
                
        except requests.exceptions.RequestException as e:
            # Network error - API might be down
            return False
        except Exception as e:
            # Any other exception - assume connection failed
            return False
    
    def poll_generation_status(self, polling_url: str) -> Optional[dict]:
        """Poll generation status until completion."""
        max_attempts = 180  # Maximum 15 minutes (180 * 5 seconds)
        attempt = 0
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while attempt < max_attempts:
            try:
                # Use session with retry strategy
                session = requests.Session()
                session.headers.update(self.headers)
                
                # Increase timeout for better stability
                response = session.get(polling_url, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    status = result.get('status')
                    
                    if status == 'completed' or status == 'Ready':
                        consecutive_errors = 0  # Reset error counter on success
                        return result
                    elif status == 'failed':
                        raise APIError(0, f"Generation failed: {result.get('error', 'Unknown error')}")
                    elif status == 'processing' or status == 'Pending':
                        consecutive_errors = 0  # Reset error counter on success
                        print(f"🔄 Processing... (attempt {attempt + 1}/{max_attempts})")
                        time.sleep(5)
                    else:
                        consecutive_errors = 0  # Reset error counter on success
                        print(f"ℹ️ Status: {status}")
                        time.sleep(5)
                else:
                    consecutive_errors += 1
                    print(f"❌ HTTP {response.status_code} error while polling status")
                    
                    if consecutive_errors >= max_consecutive_errors:
                        print(f"⚠️ Too many consecutive errors ({consecutive_errors}), increasing delay...")
                        time.sleep(30)  # Longer delay after many errors
                    else:
                        time.sleep(5)
                    
            except requests.exceptions.Timeout:
                consecutive_errors += 1
                print(f"⚠️ Timeout while polling status (attempt {attempt + 1})")
                
                if consecutive_errors >= max_consecutive_errors:
                    print(f"⚠️ Too many consecutive timeouts, increasing delay...")
                    time.sleep(30)
                else:
                    time.sleep(5)
                    
            except requests.exceptions.ConnectionError as e:
                consecutive_errors += 1
                print(f"❌ Connection error while polling: {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    print(f"⚠️ Too many consecutive connection errors, waiting longer...")
                    time.sleep(60)  # Much longer delay for connection issues
                else:
                    time.sleep(10)
                    
            except requests.exceptions.RequestException as e:
                consecutive_errors += 1
                print(f"❌ Network error while polling: {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    print(f"⚠️ Too many consecutive network errors, waiting longer...")
                    time.sleep(30)
                else:
                    time.sleep(10)
            
            attempt += 1
            
            # If we've had too many consecutive errors, break early
            if consecutive_errors >= max_consecutive_errors * 2:
                print(f"❌ Too many consecutive errors ({consecutive_errors}), giving up")
                break
        
        raise APIError(0, f"Generation timeout exceeded after {attempt} attempts")
    
    def download_image(self, image_url: str) -> Optional[bytes]:
        """Download image from URL."""
        try:
            response = requests.get(image_url, timeout=30)
            
            if response.status_code == 200:
                return response.content
            else:
                print(f"❌ Failed to download image: HTTP {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Download error: {e}")
            return None
    
    def generate_image(self, request: GenerationRequest) -> GenerationResponse:
        """Generate image using FLUX API."""
        for attempt in range(self.max_retries):
            try:
                # Use session for better connection handling
                session = requests.Session()
                session.headers.update(self.headers)
                
                # Submit generation request
                print(f"🚀 Submitting generation request (attempt {attempt + 1}/{self.max_retries})...")
                response = session.post(
                    f"{self.base_url}/flux-kontext-pro",
                    headers=self.headers,
                    json=request.to_dict(),
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    # Parse response to get polling URL
                    try:
                        result = response.json()
                        polling_url = result.get('polling_url')
                        
                        if not polling_url:
                            return GenerationResponse.error_response("No polling URL in response")
                        
                        # Poll for completion
                        print("🔄 Waiting for generation to complete...")
                        final_result = self.poll_generation_status(polling_url)
                        
                        # Extract image URL from result
                        result_data = final_result.get('result', {})
                        image_url = result_data.get('sample')
                        
                        if not image_url:
                            return GenerationResponse.error_response("No image URL in result")
                        
                        # Download image
                        print("📥 Downloading generated image...")
                        image_data = self.download_image(image_url)
                        
                        if image_data:
                            print("✅ Image generated successfully!")
                            return GenerationResponse.success_response(
                                image_data=image_data,
                                request_id=final_result.get('id')
                            )
                        else:
                            return GenerationResponse.error_response("Failed to download image")
                            
                    except json.JSONDecodeError:
                        return GenerationResponse.error_response("Invalid JSON response")
                        
                else:
                    error_msg = f"API returned status {response.status_code}"
                    try:
                        error_data = response.json()
                        error_msg = error_data.get("error", error_msg)
                    except:
                        pass
                    
                    if response.status_code == 403:
                        raise APIError(403, "Access denied. Check API key.")
                    elif response.status_code >= 500:
                        # Server error, retry
                        if attempt < self.max_retries - 1:
                            print(f"⚠️ Server error, retrying in {self.retry_delay} seconds...")
                            time.sleep(self.retry_delay)
                            continue
                    
                    return GenerationResponse.error_response(error_msg)
                    
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    print(f"⚠️ Request timeout, retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                return GenerationResponse.error_response("Request timeout")
                
            except requests.exceptions.ConnectionError as e:
                if attempt < self.max_retries - 1:
                    print(f"⚠️ Connection error: {e}, retrying in {self.retry_delay * 2} seconds...")
                    time.sleep(self.retry_delay * 2)  # Longer delay for connection issues
                    continue
                return GenerationResponse.error_response(f"Connection failed: {e}")
                
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    print(f"⚠️ Request failed: {e}, retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                return GenerationResponse.error_response(f"Request failed: {e}")
        
        return GenerationResponse.error_response(f"All {self.max_retries} attempts failed")
        
        return GenerationResponse.error_response("Max retries exceeded")
    
    def generate_image_from_file(
        self, 
        prompt: str, 
        image_path: Path, 
        **kwargs
    ) -> GenerationResponse:
        """Generate image from file."""
        try:
            request = GenerationRequest.from_image_file(prompt, image_path, **kwargs)
            return self.generate_image(request)
        except FileNotFoundError as e:
            return GenerationResponse.error_response(str(e))
        except Exception as e:
            return GenerationResponse.error_response(f"Failed to create request: {e}") 