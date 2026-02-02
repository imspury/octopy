from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import List, Optional

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