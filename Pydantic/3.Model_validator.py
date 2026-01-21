from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: str
    email: EmailStr 
    age: int 
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @model_validator(mode="after")
    def validate_emergency_contact(cls, model):
        if model.age > 60 and "emergency" not in model.contact_details:
            raise ValueError("Patients older than 60 must have emergency contact details.")
        return model

    
def insert_patient(patient: Patient):
    print(f"Inserted patient: {patient.name}, Email: {patient.email}, Age: {patient.age}, Weight: {patient.weight}, Married: {patient.married}, Allergies: {patient.allergies}, Contact Details: {patient.contact_details}")

def update_patient(patient: Patient):
    print(f"Updated patient: {patient.name}, Email: {patient.email}, Age: {patient.age}, Weight: {patient.weight}, Married: {patient.married}, Allergies: {patient.allergies}, Contact Details: {patient.contact_details}")

patient_info = {"name": "Naji", "email": "naji@hdfc.com", "age": 65, "weight": 75.5, "married": True, "allergies": ["pollen", "dust"], "contact_details": {"phone": "123-456-7890", "phone": "123456789", "emergency": "987-654-3210"}}

patient1 = Patient(**patient_info)
insert_patient(patient1)