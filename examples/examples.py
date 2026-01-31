import os
from dotenv import load_dotenv
from octopy import OctoClient

# Load the API key and account number from your .env file
load_dotenv()
API_KEY = os.getenv("OCTOPUS_API_KEY")
ACCOUNT_NUMBER = os.getenv("OCTOPUS_ACCOUNT_NUMBER")

def main():
    if not API_KEY:
        print("Error: Set OCTOPUS_API_KEY in your .env file.")
        return

    # Initialise the client
    client = OctoClient(api_key=API_KEY)

    print(f"Starting Octopy...")
    
    try:
        # Test the connection
        print(f"Checking API connection...")
        data = client.check_conn()

        product_count = data.get("count", 0)
        print(f"Connection successful!")
        print(f"There are currently {product_count} products available.")

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    main()