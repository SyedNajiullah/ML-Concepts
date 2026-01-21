from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: Annotated[str, Field(min_length=2, max_length=50, title="Name of the patient", description="Full name of the patient in less then 50 charecters", examples=["naji", "Syed najiullah"])]
    email: EmailStr # email validation
    linkedin_url: AnyUrl # url validation
    age: int = Field(gt=0, lt=120) # gt = greater than, lt = less than
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=None, title="Marital Status", description="Is the patient married or not")]
    allergies: Annotated[Optional[List[str]], Field(default= None, max_length=5)]
    contact_details: Dict[str, str]

def insert_patient(patient: Patient):
    print(f"Inserted patient: {patient.name}, Email: {patient.email}, Linkedin: {patient.linkedin_url}, Age: {patient.age}, Weight: {patient.weight}, Married: {patient.married}, Allergies: {patient.allergies}, Contact Details: {patient.contact_details}")

def update_patient(patient: Patient):
    print(f"Updated patient: {patient.name}, Email: {patient.email}, Linkedin: {patient.linkedin_url}, Age: {patient.age}, Weight: {patient.weight}, Married: {patient.married}, Allergies: {patient.allergies}, Contact Details: {patient.contact_details}")

patient_info = {"name": "Naji", "email": "naji@example.com", "linkedin_url": "https://www.linkedin.com/in/syed-najiullah-0a17a726b", "age": 30, "weight": 75.5, "married": True, "allergies": ["pollen", "dust"], "contact_details": {"phone": "123-456-7890", "phone": "123456789"}}

patient1 = Patient(**patient_info)
insert_patient(patient1)