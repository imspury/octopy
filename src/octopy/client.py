# Standard library imports
from typing import Dict, Any

# Third-party imports
import requests

class OctoClient:
    """
    A simple client for interacting with the Octopus Energy API.
    """
    BASE_URL = "https://api.octopus.energy/v1/"

    def __init__(self, api_key: str):
        # Store the API key for authentication
        self.api_key = api_key
        # Initialise a session for persistent connections
        self.session = requests.Session()
        # API uses basic authentication with the API key as the username
        self.session.auth = (self.api_key, "")
    
    def check_auth(self, account_number) -> Dict[str, Any]:
        """
        Check if the provided API key is valid by making a request to the
        account endpoint.

        Args:
            account_number (str): The account number to check.

        Returns:
            A dictionary containing account information if the API key is valid.
        """
        url = f"{self.BASE_URL}accounts/{account_number}/"
        response = self.session.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
