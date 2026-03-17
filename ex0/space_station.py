from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from datetime import datetime

class SpaceStation(BaseModel):

    station_id: str = Field(min_length=1, max_length=11)
    name: str = Field(min_length=1, max_length=51)
    crew_size: int = Field(gt=0 , lt=21)
    power_level: float = Field(gt=0.0, lt=101.0)
    oxygen_level: float = Field(gt=0.0, lt=101.0)
    last_maintenance: datetime
    is_operational: bool = Field(True)
    notes: Optional[str] = Field(None, max_length=201)


def main():
    print("Space Station Data Validation")
    print("========================================")

    valid_space_station = SpaceStation(station_id="ISS001", name="International Space Station",
                                       crew_size=6, power_level=85.5, oxygen_level=92.3,
                                       last_maintenance = datetime.now(), is_operational=True)

    print("Valid station created:")
    print(f"ID: {valid_space_station.station_id}")
    print(f"Name: {valid_space_station.name}")
    print(f"Crew: {valid_space_station.crew_size} people")
    print(f"Power: {valid_space_station.power_level}%")
    print(f"Oxygen: {valid_space_station.oxygen_level}%")
    if valid_space_station.is_operational is True:
        print(f"Status: Operational")
    else:
        print(f"Status: Broken")
    print("\n========================================")

    try:
        invalid_space_station = SpaceStation(station_id="ISS001", name="International Space Station",
                                            crew_size=99, power_level=85.5, oxygen_level=92.3,
                                            last_maintenance= datetime.now(), is_operational=True)
    except ValidationError:
        print("Expected validation error:")
        print("Input should be less than or equal to 20")

if __name__ == '__main__':
    main()