from pydantic import BaseModel, Field, model_validator
from enum import Enum
from datetime import datetime
from typing import Optional


class ContactType(Enum):
    """contacttype"""
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    """aliencontact"""
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, lt=100)
    message_received: Optional[str] = Field(max_length=500)
    is_verified: bool = Field(False)

    @model_validator(mode='after')
    def check_attributes(self):

        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID should start with AC")

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact must be verified")

        if self.witness_count < 3 and self.contact_type.telepathic:
            raise ValueError("Telepathic contact requires "
                             "at least 3 witnesses")

        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError("Signal > 7.0 should provide a message")

        self.is_verified = True
        return self


def main():
    print("Alien Contact Log Validation")
    print("======================================")

    try:
        valid_report = AlienContact(contact_id="AC_2024_001",
                                    timestamp=datetime.now(),
                                    location="Area 51, Nevada",
                                    contact_type=ContactType.radio,
                                    signal_strength=8.5,
                                    duration_minutes=45,
                                    witness_count=5,
                                    message_received=("Greetings from"
                                                      " Zeta Reticuli"),
                                    is_verified=False)

        print("Valid contact report:")
        print(f"ID: {valid_report.contact_id}")
        print(f"Type: {valid_report.contact_type.value}")
        print(f"Location: {valid_report.location}")
        print(f"Signal: {valid_report.signal_strength}/10")
        print(f"Duration: {valid_report.duration_minutes} minutes")
        print(f"Witnesses: {valid_report.witness_count}")
        print(f"Message: '{valid_report.message_received}'")

    except Exception as e:
        print(e)

    print("\n======================================")

    try:
        AlienContact(contact_id="AC_2024_001",
                     timestamp=datetime.now(),
                     location="Area 51, Nevada",
                     contact_type=ContactType.radio,
                     signal_strength=8.5,
                     duration_minutes=45,
                     witness_count=1,
                     message_received="Greetings from Zeta Reticuli",
                     is_verified=False)

    except ValueError as e:
        raw_msg = e.errors()[0]['msg']
        clean_msg = raw_msg.removeprefix("Value error, ")
        print(clean_msg)


if __name__ == '__main__':
    main()
