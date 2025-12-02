# Local implementation of _snowflake library for validation
# This module provides real API calls to Snowflake Cortex REST API

import json
import logging
import urllib.request
import urllib.parse
import urllib.error
import configparser
import os
import tomllib
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class LocalSnowflakeAPI:
    """
    Local implementation of _snowflake library functionality
    Makes real API calls to Snowflake Cortex REST API using validation credentials
    """
    
    def __init__(self, session=None):
        """
        Initialize with Snowflake connection configuration
        """
        self.session = session
        # Load validation connection from local connections.toml only
        self.config = self._load_local_connections()
        self.base_url = None
        self.auth_header = None
        self._initialize_connection()
    
    def _load_local_connections(self):
        """Load validation connection from local connections.toml only."""
        module_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(module_dir, "connections.toml")
        if not os.path.exists(path):
            logger.error("connections.toml not found in project root")
            return None
        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)
            return data
        except Exception as e:
            logger.error(f"Failed to load connections.toml: {str(e)}")
            return None
    
    def _initialize_connection(self):
        """Initialize connection parameters from local connections.toml only."""
        if not self.config or 'validation' not in self.config:
            logger.error("Validation connection not found in connections.toml")
            return

        validation = self.config['validation']

        account_identifier = validation.get('accountname')
        access_token = validation.get('accesstoken')

        if not account_identifier:
            logger.error("Missing accountname in connections.toml [validation]")
            return

        self.base_url = f"https://{account_identifier}.snowflakecomputing.com"

        if access_token:
            self.auth_header = f"Bearer {access_token}"
            logger.info(f"Initialized connection using token to {self.base_url}")
        else:
            logger.warning("accesstoken not set in connections.toml; requests will fail with auth error")
            self.auth_header = None
    
    def send_snow_api_request(self, 
                            method: str, 
                            path: str, 
                            headers: Dict = None, 
                            params: Dict = None, 
                            body: Any = None, 
                            request_guid: Optional[str] = None, 
                            timeout: int = 30000) -> Dict[str, Any]:
        """
        Make real API request to Snowflake Cortex REST API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            headers: Request headers dictionary
            params: Query parameters dictionary
            body: Request body (usually JSON)
            request_guid: Optional request identifier
            timeout: Request timeout in milliseconds
            
        Returns:
            Dict with 'status' and 'content' keys matching Snowflake response format
        """
        
        if not self.base_url or not self.auth_header:
            return {
                "status": 500,
                "content": json.dumps({
                    "error": "Connection not initialized",
                    "message": "Failed to load validation connection config"
                })
            }
        
        headers = headers or {}
        params = params or {}
        timeout_seconds = timeout / 1000.0  # Convert ms to seconds
        
        # Construct full URL
        full_url = f"{self.base_url}{path}"
        
        # Add query parameters if any
        if params:
            query_string = urllib.parse.urlencode(params)
            full_url += f"?{query_string}"
        
        # Set up headers
        request_headers = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json",
            "Accept": "application/json",
            **headers
        }
        
        # Add request GUID if provided
        if request_guid:
            request_headers["X-Request-GUID"] = request_guid
        
        logger.info(f"Making {method} request to {full_url}")
        
        try:
            # Prepare request data
            data = None
            if body:
                data = json.dumps(body).encode('utf-8')
            
            # Create request
            request = urllib.request.Request(
                full_url,
                data=data,
                headers=request_headers,
                method=method
            )
            
            # Make the request
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                status_code = response.getcode()
                response_data = response.read().decode('utf-8')
                
                logger.info(f"API response: {status_code}")
                
                return {
                    "status": status_code,
                    "content": response_data
                }
                
        except urllib.error.HTTPError as e:
            logger.error(f"HTTP Error {e.code}: {e.reason}")
            
            # Read error response
            try:
                error_response = e.read().decode('utf-8')
                
                # Handle specific error cases
                if e.code == 401:
                    try:
                        error_data = json.loads(error_response)
                        error_message = error_data.get('message', '')
                        if "Network policy is required" in error_message:
                            logger.error("Network policy restriction detected - API access may be limited by IP/network policies")
                            logger.info("This is common in production Snowflake accounts with network restrictions")
                        elif "invalid" in error_message.lower() or "expired" in error_message.lower():
                            logger.error("Access token may be invalid or expired")
                    except json.JSONDecodeError:
                        pass
                        
                return {
                    "status": e.code,
                    "content": error_response
                }
                
            except Exception:
                return {
                    "status": e.code,
                    "content": json.dumps({
                        "error": f"HTTP {e.code}",
                        "message": str(e.reason)
                    })
                }
        
        except urllib.error.URLError as e:
            logger.error(f"URL Error: {e.reason}")
            return {
                "status": 500,
                "content": json.dumps({
                    "error": "Connection failed",
                    "message": str(e.reason)
                })
            }
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "status": 500,
                "content": json.dumps({
                    "error": "Unexpected error",
                    "message": str(e)
                })
            }

# Create global instance that can be imported as _snowflake
_snowflake_instance = LocalSnowflakeAPI()

# Main function that mimics the _snowflake library interface
def send_snow_api_request(method: str, 
                         path: str, 
                         headers: Dict = None, 
                         params: Dict = None, 
                         body: Any = None, 
                         request_guid: Optional[str] = None, 
                         timeout: int = 30000) -> Dict[str, Any]:
    """
    Main function that matches _snowflake.send_snow_api_request signature
    """
    return _snowflake_instance.send_snow_api_request(
        method, path, headers, params, body, request_guid, timeout
    )

# For compatibility, also provide the class
LocalSnowflakeAPI = LocalSnowflakeAPI