from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin_code: str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address  # Nested model

address_dict = {"city": "New York",
"state": "NY",
"pin_code": "10001"}
address1 = Address(**address_dict)

patient_dict = {"name": "John Doe",
"gender": "Male",
"age": 30,
"address": address1}
patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.name)
print(patient1.address.city)