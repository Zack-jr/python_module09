from pydantic import BaseModel, Field, model_validator
from enum import Enum
from datetime import datetime
from typing import List


class Rank(Enum):
    """rank"""
    cadet = "cadet"
    officer = "officer"
    lieuteneant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    """crew member"""
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=81)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(True)


class SpaceMission(BaseModel):
    """spacemission"""
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field("planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def check(self):

        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID should start with M")

        crew_ranks = [member.rank for member in self.crew]
        if not any(r in crew_ranks for r in [Rank.commander, Rank.captain]):
            raise ValueError("Mission should have at least 1 commander"
                             " or 1 captain")

        if self.duration_days > 365:
            experimented_members = sum(
                1 for m in self.crew if m.years_experience >= 5)
            if (experimented_members < len(self.crew) / 2):
                raise ValueError("Long missions (> 365 days) need 50% "
                                 "experienced crew (5+ years)")

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def main():
    print("Space Mission Crew Validation")
    print("========================================")

    try:
        crew_members = [

            CrewMember(member_id="S001",
                       name="Sarah Connor",
                       rank=(Rank.commander.value),
                       age=40,
                       specialization="Mission Command",
                       years_experience=20,
                       is_active=True),

            CrewMember(member_id="J001",
                       name="John Smith",
                       rank=(Rank.lieuteneant.value),
                       age=32,
                       specialization="Navigation",
                       years_experience=8,
                       is_active=True),

            CrewMember(member_id="A001",
                       name="Alice Johnson",
                       rank=(Rank.officer.value),
                       age=50,
                       specialization="Engineering",
                       years_experience=20,
                       is_active=True)

                            ]

        bad_crew_members = [

            CrewMember(member_id="S001",
                       name="Sarah Connor",
                       rank=(Rank.officer.value),
                       age=40,
                       specialization="Mission Command",
                       years_experience=20,
                       is_active=True),

            CrewMember(member_id="J001",
                       name="John Smith",
                       rank=(Rank.cadet.value),
                       age=32,
                       specialization="Navigation",
                       years_experience=8,
                       is_active=True),

            CrewMember(member_id="A001",
                       name="Alice Johnson",
                       rank=(Rank.cadet.value),
                       age=50,
                       specialization="Engineering",
                       years_experience=20,
                       is_active=True)

                            ]
    except Exception:
        print("Error creating crew member")

    try:
        valid_mission = SpaceMission(mission_id="M2024_MARS",
                                     mission_name="Mars Colony Establishement",
                                     destination="Mars",
                                     launch_date=datetime.now(),
                                     duration_days=900,
                                     crew=crew_members,
                                     mission_status="planned",
                                     budget_millions=2500.0)

        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for member in valid_mission.crew:
            print(f"- {member.name} ({member.rank.value})"
                  f" - {member.specialization}")

    except ValueError as e:
        raw_msg = e.errors()[0]['msg']
        clean_msg = raw_msg.removeprefix("Value error, ")
        print(clean_msg)

    print("\n========================================")

    try:
        inv_mission = SpaceMission(mission_id="M2024_MARS",
                                   mission_name="Mars Colony Establishement",
                                   destination="Mars",
                                   launch_date=datetime.now(),
                                   duration_days=900,
                                   crew=bad_crew_members,
                                   mission_status="planned",
                                   budget_millions=2500.0)
        print(inv_mission)

    except ValueError as e:
        print("Expected validation error:")
        raw_msg = e.errors()[0]['msg']
        clean_msg = raw_msg.removeprefix("Value error, ")
        print(clean_msg)


if __name__ == '__main__':
    main()
