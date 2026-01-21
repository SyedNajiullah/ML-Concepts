from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: str
    email: EmailStr 
    age: int 
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split("@")[-1]
        if domain_name not in valid_domains:
            raise ValueError(f"Not a valid domain")
        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator('age', mode='before') # before type conversion (after = after type conversion)
    @classmethod
    def age_validator(cls, value):
        if value > 0 and value < 100:
            return value
        raise ValueError("Age must be between 1 and 99")

def insert_patient(patient: Patient):
    print(f"Inserted patient: {patient.name}, Email: {patient.email}, Age: {patient.age}, Weight: {patient.weight}, Married: {patient.married}, Allergies: {patient.allergies}, Contact Details: {patient.contact_details}")

def update_patient(patient: Patient):
    print(f"Updated patient: {patient.name}, Email: {patient.email}, Age: {patient.age}, Weight: {patient.weight}, Married: {patient.married}, Allergies: {patient.allergies}, Contact Details: {patient.contact_details}")

patient_info = {"name": "Naji", "email": "naji@hdfc.com", "age": 30, "weight": 75.5, "married": True, "allergies": ["pollen", "dust"], "contact_details": {"phone": "123-456-7890", "phone": "123456789"}}

patient1 = Patient(**patient_info)
insert_patient(patient1)