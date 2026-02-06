from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import List, Optional

def get_region_name_from_gsp(gsp_code: str) -> str:
    """Maps a Grid Service Provider (GSP) group code to a human-readable region name."""
    gsp_map = {
        "A": "Eastern England",
        "B": "East Midlands",
        "C": "London",
        "D": "Merseyside and Northern Wales",
        "E": "West Midlands",
        "F": "North Eastern England",
        "G": "North Western England",
        "H": "Southern England",
        "J": "South Eastern England",
        "K": "Southern Wales",
        "L": "South Western England",
        "M": "Yorkshire",
        "N": "Southern Scotland",
        "P": "Northern Scotland"
    }
    clean_code = gsp_code.upper().replace("_", "")
    return gsp_map.get(clean_code, f"Unknown Region ({clean_code})")

class Agreement(BaseModel):
    """Represents a specific tariff agreement for a meter point."""
    tariff_code: str = Field(..., description="The unique code for the energy tariff")
    valid_from: datetime
    valid_to: Optional[datetime] = Field(None, description="End date of tariff. None indicates an active/rolling tariff.")

    @property
    def is_active(self) -> bool:
        """Returns True if the agreement is currently active (no end date or future end date)."""
        now = datetime.now(timezone.utc)

        # No end date
        if self.valid_to is None:
            return True
        
        # End date is in the future
        return self.valid_to > now

class Meter(BaseModel):
    """Details of a physical meter installed at a property."""
    serial_number: str

class ElectricityMeterPoint(BaseModel):
    """An electricity connection point (MPAN) containing one or more meters."""
    mpan: str
    meters: List[Meter]
    agreements: List[Agreement]
    is_export: bool = Field(False, description="True if this meter exports solar/wind energy to the grid")

class GasMeterPoint(BaseModel):
    """A gas connection point (MPRN) containing one or more meters."""
    mprn: str
    meters: List[Meter]
    agreements: List[Agreement]

class Property(BaseModel):
    """A physical location associated with an Octopus account."""
    id: int
    address_line_1: str
    postcode: str
    electricity_meter_points: List[ElectricityMeterPoint] = []
    gas_meter_points: List[GasMeterPoint] = []

class Account(BaseModel):
    """The top-level Octopus Account object containing all properties and meters."""
    number: str
    properties: List[Property]

class Link(BaseModel):
    """Represents a HATEOAS link provided by the API."""
    href: str
    method: str
    rel: str

class Product(BaseModel):
    """Summary of an Octopus Energy product."""
    code: str
    direction: str
    full_name: str
    display_name: str
    description: str
    is_variable: bool
    is_green: bool
    is_tracker: bool
    is_prepay: bool
    is_business: bool
    is_restricted: bool
    term: Optional[int] = None
    available_from: Optional[datetime] = None
    available_to: Optional[datetime] = None
    links: List[Link] = []
    brand: str

    @property
    def is_export(self) -> bool:
        """Returns True if this is an export tariff."""
        return self.direction.upper() == "EXPORT"