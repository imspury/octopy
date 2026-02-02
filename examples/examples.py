import os
from dotenv import load_dotenv
from octopy import OctoClient

# Load configuration from .env file
load_dotenv()
API_KEY = os.getenv("OCTOPUS_API_KEY")
ACCOUNT_NUMBER = os.getenv("OCTOPUS_ACCOUNT_NUMBER")

def main():
    if not API_KEY or not ACCOUNT_NUMBER:
        print("Missing credentials. Check your .env file.")
        return

    # Initialise the client
    print(f"Starting Octopy...")
    client = OctoClient(api_key=API_KEY)
    print(f"Octopy initialised!")
    
    try:
        # Fetch the account object
        print(f"Obtainting account information...")
        account = client.get_account(ACCOUNT_NUMBER)

        print(f"Success! Found {len(account.properties)} property/properties.")

        for prop in account.properties:
            print(f"\nAddress: {prop.address_line_1}, {prop.postcode}")
            print(f"Region: {client.get_region_from_postcode(prop.postcode)}")

            # Electricity Meter Points
            for emp in prop.electricity_meter_points:
                # Find active agreement
                active_agreement = next((a for a in emp.agreements if a.is_active), None)

                print("Electricity:")
                print(f"- MPAN: {emp.mpan}")
                if active_agreement:
                    print(f"- Active Tariff: {active_agreement.tariff_code}")
                else:
                    print(f"- No active electricity tariff found.")
            
            # Gas Meter Points
            for gmp in prop.gas_meter_points:
                # Find active agreement
                active_agreement = next((a for a in gmp.agreements if a.is_active), None)

                print("Gas:")
                print(f"- Gas MPRN: {gmp.mprn}")
                if active_agreement:
                    print(f"- Active Tariff: {active_agreement.tariff_code}")
                else:
                    print(f"- No active gas tariff found.")
                
                for meter in gmp.meters:
                    print(f" - Meter Serial: {meter.serial_number}")

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    main()