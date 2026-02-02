# Standard library imports
from typing import Dict, Any

# Third-party imports
import requests

# Custom imports
from .models import Account

class OctoClient:
    """
    A simple client for interacting with the Octopus Energy API.
    """
    BASE_URL = "https://api.octopus.energy/v1"

    def __init__(self, api_key: str):
        # Store the API key for authentication
        self.api_key = api_key
        # Initialise a session for persistent connections
        self.session = requests.Session()
        # API uses basic authentication with the API key as the username
        self.session.auth = (self.api_key, "")
    
    def check_conn(self) -> Dict[str, Any]:
        """
        Check the connection to the Octopus Energy API.

        Returns:
            A dictionary containing all currently active products.
        """
        response = self.session.get(f"{self.BASE_URL}/products/")
        response.raise_for_status()
        return response.json()
    
    def get_account(self, account_number: str) -> Account:
        """
        Retrieves details for an account and returns a validated Account object.

        Args:
            account_number: The Octopus Energy account number.
        
        Returns:
            An Account object containing all properties and meters.
        """
        url = f"{self.BASE_URL}/accounts/{account_number}/"
        response = self.session.get(url)
        response.raise_for_status()

        # Convert JSON dictionary into our Account object
        return Account(**response.json())