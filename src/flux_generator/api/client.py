"""
FLUX API client for image generation.
"""

import requests
import time
import json
from typing import Optional

from ..config.settings import settings
from .base import BaseAPIClient, APIError
from .models import GenerationRequest, GenerationResponse


class FluxAPIClient(BaseAPIClient):
    """Client for BFL.ai FLUX API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize API client."""
        super().__init__(settings=settings, api_key=api_key, base_url=settings.api.base_url)
    
    def poll_generation_status(self, polling_url: str) -> Optional[dict]:
        """Poll generation status until completion."""
        max_attempts = self.settings.api.polling_timeout_attempts
        polling_interval = self.settings.api.polling_interval
        attempt = 0
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        # Special handling for moderation
        moderation_start_time = None
        max_moderation_time = getattr(self.settings.api, 'moderation_timeout', 300)
        moderation_attempts = 0
        max_moderation_attempts = getattr(self.settings.api, 'moderation_max_attempts', 100)
        moderation_interval = getattr(self.settings.api, 'moderation_interval', 3)
        
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
                        time.sleep(polling_interval)
                    elif status == 'Content Moderated':
                        # Special handling for content moderation
                        if moderation_start_time is None:
                            moderation_start_time = time.time()
                            print(f"🛡️ Content moderation in progress...")
                        
                        moderation_attempts += 1
                        consecutive_errors = 0
                        
                        # Check if moderation is taking too long
                        moderation_duration = time.time() - moderation_start_time
                        if moderation_duration > max_moderation_time:
                            raise APIError(0, f"Content moderation timeout after {moderation_duration:.1f} seconds")
                        
                        if moderation_attempts > max_moderation_attempts:
                            raise APIError(0, f"Content moderation exceeded maximum attempts ({max_moderation_attempts})")
                        
                        # Use optimized interval for moderation status
                        if moderation_attempts % 10 == 0:  # Show progress every 10 attempts
                            print(f"🛡️ Still moderating... ({moderation_attempts} checks, {moderation_duration:.1f}s)")
                        
                        time.sleep(moderation_interval)
                    else:
                        consecutive_errors = 0  # Reset error counter on success
                        print(f"ℹ️ Status: {status}")
                        time.sleep(polling_interval)
                else:
                    consecutive_errors += 1
                    print(f"❌ HTTP {response.status_code} error while polling status")
                    
                    if consecutive_errors >= max_consecutive_errors:
                        print(f"⚠️ Too many consecutive errors ({consecutive_errors}), increasing delay...")
                        time.sleep(polling_interval * 6)  # Longer delay after many errors
                    else:
                        time.sleep(polling_interval)
                    
            except requests.exceptions.Timeout:
                consecutive_errors += 1
                print(f"⚠️ Timeout while polling status (attempt {attempt + 1})")
                
                if consecutive_errors >= max_consecutive_errors:
                    print(f"⚠️ Too many consecutive timeouts, increasing delay...")
                    time.sleep(polling_interval * 6)
                else:
                    time.sleep(polling_interval)
                    
            except requests.exceptions.ConnectionError as e:
                consecutive_errors += 1
                print(f"❌ Connection error while polling: {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    print(f"⚠️ Too many consecutive connection errors, waiting longer...")
                    time.sleep(polling_interval * 12)  # Much longer delay for connection issues
                else:
                    time.sleep(polling_interval * 2)
                    
            except requests.exceptions.RequestException as e:
                consecutive_errors += 1
                print(f"❌ Network error while polling: {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    print(f"⚠️ Too many consecutive network errors, waiting longer...")
                    time.sleep(polling_interval * 6)
                else:
                    time.sleep(polling_interval * 2)
            
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
        try:
            # Submit generation request
            print(f"🚀 Submitting generation request...")
            response = self._make_request(
                "POST",
                "/flux-kontext-pro",
                data=request.to_dict()
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
                print(f"🔍 Response Status: {response.status_code}")
                print(f"🔍 Response Headers: {dict(response.headers)}")
                print(f"🔍 Response Text: {response.text[:500]}...")
                
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", error_msg)
                    # Log detailed error information
                    print(f"🔍 API Error Details: {json.dumps(error_data, indent=2)}")
                except Exception as e:
                    print(f"🔍 Could not parse JSON response: {e}")
                    print(f"🔍 Raw response: {response.text}")
                
                if response.status_code == 403:
                    raise APIError(403, "Access denied. Check API key.")
                
                return GenerationResponse.error_response(error_msg)
                
        except APIError:
            raise
        except Exception as e:
            return GenerationResponse.error_response(f"Request failed: {e}")