import os
from dotenv import load_dotenv
from octopy.client import OctoClient

# Load the API key and account number from your .env file
load_dotenv()
API_KEY = os.getenv("OCTOPUS_API_KEY")
ACCOUNT_NUMBER = os.getenv("OCTOPUS_ACCOUNT_NUMBER")

def main():
    if not API_KEY:
        print("Error: OCTOPUS_API_KEY not found in environment.")
        print("Make sure you have a .env file with: OCTOPUS_API_KEY=sk_live_...")
        return

    # Initialise the client
    client = OctoClient(api_key=API_KEY)

    print("Connecting to Octopus Energy...")
    
    try:
        # Try to fetch account details as a test
        data = client.check_auth(ACCOUNT_NUMBER)

        property_count = len(data.get("properties", []))
        print(f"Success! Connected to Octopus API.")
        print(f"Found {property_count} properties available.")

        # Print postcode of the first property as a test
        if property_count > 0:
            first_property = data["properties"][0]
            print(f"Postcode for 1st property: {first_property.get('postcode', 'N/A')}")

    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    main()