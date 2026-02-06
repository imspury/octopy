# Standard library imports
import logging
from typing import Dict, Any

# Third-party imports
import requests

# Custom imports
from .models import get_region_name_from_gsp, Account
from .http_client import BaseHTTPClient

logger = logging.getLogger(__name__)

class OctoClient(BaseHTTPClient):
    """Client for interacting with the Octopus Energy API."""

    BASE_URL = "https://api.octopus.energy/v1"

    def __init__(self, api_key: str):
        """Initialise the Octopus Energy API client."""
        session = requests.Session()
        session.auth = (api_key, "")
        super().__init__(session)

        self.api_key = api_key
        logger.info(f"Using API base URL: {self.BASE_URL}")

    def _fetch_paginated_data(self, url: str, params: dict) -> list[dict]:
        """
        Internal helper to handle Octopus API pagination.
        Follows 'next' links until all data is collected.

        Args:
            url: The initial URL to fetch data from.
            params: Query parameters for the initial request.
        
        Returns:
            A list of all results across paginated responses.
        """
        all_results = []
        current_url = url
        is_first_page = True

        while current_url:
            # On first request, we attach the params.
            # On subsequent requests, the 'next' URL provided by the API already contains the necessary parameters.
            response = self.session.get(
                current_url, 
                params=params if is_first_page else None
            )
            response.raise_for_status()
            data = response.json()
            
            # Safely add the results from this page to our main list
            all_results.extend(data.get("results", []))
            
            # Get the URL for the next page (will be None if we are done)
            current_url = data.get("next")
            is_first_page = False
            
        return all_results
    
    def get_account(self, account_number: str) -> Account:
        """
        Retrieve account details.

        Args:
            account_number: The Octopus Energy account number.
        
        Returns:
            An Account object containing all properties and meters.
        """
        logger.info(f"Fetching account details for: {account_number}")

        response = self.get(f"{self.BASE_URL}/accounts/{account_number}/")
        data = response.json()

        num_properties = len(data.get('properties', []))
        logger.info(f"Successfully retrieved account with {num_properties} property/properties.")

        return Account(**response.json())
    
    def get_region_from_postcode(self, postcode: str) -> str:
        """
        Get region name from postcode using Grid Service Provider (GSP) code.

        Args:
            postcode: The postcode to look up.

        Returns:
            The name of the region corresponding to the postcode.
        Raises:
            ValueError: If the postcode is invalid or GSP cannot be found.
        """
        logger.info(f"Looking up region for postcode: {postcode}")

        response = self.get(
            f"{self.BASE_URL}/industry/grid-supply-points/",
            params={"postcode": postcode}
        )
        
        data = response.json()
        results = data.get("results", [])

        if not results:
            logger.warning(f"No GSP results found for postcode: {postcode}")
            raise ValueError(f"No GSP data found for postcode: {postcode}")
        
        gsp_code = results[0].get("group_id", "")
        region_name = get_region_name_from_gsp(gsp_code)
        logger.info(f"Region found: {region_name} (GSP: {gsp_code})")

        return region_name