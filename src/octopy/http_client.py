"""Base HTTP client with error handling for GET requests."""
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)


class BaseHTTPClient:
    """Base class for making HTTP GET requests with error handling."""
    
    DEFAULT_TIMEOUT = 10
    
    def __init__(self, session: Optional[requests.Session] = None):
        """Initialise the HTTP client."""
        self.session = session or requests.Session()
    
    def get(
        self,
        url: str,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make a GET request with error handling.
        
        Args:
            url: URL to request
            timeout: Request timeout (uses DEFAULT_TIMEOUT if not specified)
            **kwargs: Additional arguments for requests (params, headers, etc.)
        
        Returns:
            Response object
            
        Raises:
            ValueError: For API errors (401, 403, 404, 429)
            TimeoutError: For request timeouts
            ConnectionError: For connection failures
            RuntimeError: For other request failures
        """
        timeout = timeout or self.DEFAULT_TIMEOUT
        
        logger.debug(f"Making GET request to {url}")
        
        try:
            response = self.session.get(url, timeout=timeout, **kwargs)
            logger.debug(f"Response - Status: {response.status_code}")
            
            response.raise_for_status()
            return response
            
        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e)
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {timeout}s")
            raise TimeoutError(f"Request timed out after {timeout}s")
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection failed: {e}")
            raise ConnectionError(f"Failed to connect to API: {e}") from e
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}", exc_info=True)
            raise RuntimeError(f"API request failed: {e}") from e
    
    def _handle_http_error(self, error: requests.exceptions.HTTPError) -> None:
        """Handle HTTP errors with appropriate logging and exceptions."""
        response = error.response
        status_code = response.status_code
        
        if status_code == 401:
            logger.error("Authentication failed - invalid API key")
            raise ValueError("Invalid API key") from error
        elif status_code == 403:
            logger.error("Access forbidden - check API permissions")
            raise ValueError("Access forbidden") from error
        elif status_code == 404:
            logger.warning(f"Resource not found: {response.url}")
            raise ValueError("Resource not found") from error
        elif status_code == 429:
            retry_after = response.headers.get('Retry-After', 'unknown')
            logger.warning(f"Rate limited - Retry after: {retry_after}s")
            raise ValueError(f"Rate limited. Retry after {retry_after}s") from error
        else:
            logger.error(f"HTTP error {status_code}: {error}")
            raise ValueError(f"API error: {status_code}") from error
