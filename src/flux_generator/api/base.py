"""
Base API Classes for FLUX Image Generator.

This module provides base classes for API functionality
to reduce code duplication across client and models.
"""

import requests
import time
import json
from typing import Optional, Dict, Any, Union
from abc import ABC, abstractmethod
from pathlib import Path

from ..config.base import EnvironmentConfig


class BaseAPIClient(ABC):
    """Base class for API clients."""
    
    def __init__(self, settings, api_key: Optional[str] = None, base_url: str = ""):
        """Initialize base API client."""
        self.settings = settings
        self.api_key = api_key or EnvironmentConfig.get_api_key()
        if not self.api_key:
            raise ValueError("API key is required")
        
        self.base_url = base_url
        self.timeout = self.settings.api.timeout
        self.max_retries = self.settings.api.max_retries
        self.retry_delay = self.settings.api.retry_delay
        
        # Remove quotes if present
        self.api_key = self.api_key.strip('"\'')
        
        self.headers = {
            "x-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """Make HTTP request with retry logic."""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=data,
                    timeout=self.timeout,
                    **kwargs
                )
                
                # If successful or client error (4xx), don't retry
                if response.status_code < 500:
                    return response
                
                # Server error (5xx), retry
                if attempt < self.max_retries - 1:
                    print(f"⚠️ Server error {response.status_code}, retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                
                return response
                
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    print(f"⚠️ Request timeout, retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                raise
                
            except requests.exceptions.ConnectionError as e:
                if attempt < self.max_retries - 1:
                    print(f"⚠️ Connection error: {e}, retrying in {self.retry_delay * 2} seconds...")
                    time.sleep(self.retry_delay * 2)
                    continue
                raise
                
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    print(f"⚠️ Request failed: {e}, retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                raise
        
        raise requests.exceptions.RequestException(f"All {self.max_retries} attempts failed")
    
    def test_connection(self) -> bool:
        """Test API connection."""
        try:
            # Simple test request
            test_data = {
                "prompt": "test",
                "input_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=",
                "seed": 1000,
                "aspect_ratio": "1:1"
            }
            
            response = self._make_request("POST", "/flux-kontext-pro", data=test_data)
            
            # If we get any response (even error), the API key is working
            if response.status_code in [200, 400, 422]:  # Success or validation errors
                return True
            elif response.status_code == 403:
                raise Exception("Access denied. Check API key.")
            else:
                return True
                
        except Exception:
            return False


class BaseRequest:
    """Base class for API requests."""
    
    def __init__(self, **kwargs):
        """Initialize request with keyword arguments."""
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseRequest":
        """Create request from dictionary."""
        return cls(**data)


class BaseResponse:
    """Base class for API responses."""
    
    def __init__(self, success: bool, **kwargs):
        """Initialize response."""
        self.success = success
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def success_response(cls, **kwargs) -> "BaseResponse":
        """Create success response."""
        return cls(success=True, **kwargs)
    
    @classmethod
    def error_response(cls, error_message: str, **kwargs) -> "BaseResponse":
        """Create error response."""
        return cls(success=False, error_message=error_message, **kwargs)


class APIError(Exception):
    """API error exception."""
    
    def __init__(self, status_code: int, message: str, details: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"API Error {self.status_code}: {self.message}" 