import os
import logging
from dotenv import load_dotenv
from octopy import OctoClient

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def products(client: OctoClient):
    """Example function to demonstrate fetching products with filters."""
    print("Searching for variable, green tariffs...")
    products = client.get_products(is_green=True, is_variable=True)
    print(f"Found {len(products)} variable, green products.")

    # List the first 5
    for p in products[:5]:
        print(f" - {p.display_name} (Code: {p.code})")

def main():
    # Load configuration from .env file
    load_dotenv()
    API_KEY = os.getenv("OCTOPUS_API_KEY")
    ACCOUNT_NUMBER = os.getenv("OCTOPUS_ACCOUNT_NUMBER")

    if not API_KEY or not ACCOUNT_NUMBER:
        print("Missing credentials. Check your .env file.")
        return

    # Initialise the client
    client = OctoClient(api_key=API_KEY)

    print("Obtainting account information...")
    account = client.get_account(ACCOUNT_NUMBER)
    print(f"Success! Found {len(account.properties)} properties")

    for prop in account.properties:
        print(f"Address: {prop.address_line_1}, {prop.postcode}")
        print(f"Region: {client.get_region_from_postcode(prop.postcode)}")
    
        # Electricity Meter Points (works same for gas meter points)
        for emp in prop.electricity_meter_points:
            # Find active agreement
            active_agreement = next((a for a in emp.agreements if a.is_active), None)

            print(f"Electricity MPAN: {emp.mpan}")
            if active_agreement:
                print(f"- Active Tariff: {active_agreement.tariff_code}")
            else:
                print(f"- No active electricity tariff found.")
    
    # Example of fetching products with filters
    products(client)

if __name__ == "__main__":
    main()