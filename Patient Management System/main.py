from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", example="P001")]
    name: Annotated[str, Field(..., description="Name of the patient", example="Syed Najiullah")]
    city: Annotated[str, Field(..., description="City of the patient", example="Lahore")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient", example=30)]
    gender: Annotated[Literal["male", "female", "others"], Field(..., description="Gender of the patient", example="male")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal["male", "female", "others"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

def load_data():
    with open("patients.json", "r") as file:
        return json.load(file)

def save_data(data):
    with open("patients.json", "w") as file:
        json.dump(data, file)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functionalAPI to manage your patient records"}

@app.get("/view")
def view():
    return load_data()

@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the patient in DB", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort on basis on height, weight, or BMI"), order: str = Query("asc", description="Sort in ascending and decending order")):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field. Must be one of {valid_fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail='Invalid order field. Must be "asc" or "desc"')
    
    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    # loading data
    data = load_data()
    #cheking if patient is already in record
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    #adding new patient
    data[patient.id] = patient.model_dump(exclude=["id"])
    #saving data
    save_data(data)
    #returning response
    return JSONResponse(status_code=201, content={"message": "Patient created successfully", "patient": data[patient.id]})

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient( **existing_patient_info)

    existing_pydantic_info = patient_pydantic_object.model_dump(exclude=["id"])

    data[patient_id] = existing_pydantic_info

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully", "patient": data[patient_id]})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})
