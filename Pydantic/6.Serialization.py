from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin_code: str

class Patient(BaseModel):
    name: str
    gender: str = "Male"
    age: int
    address: Address  # Nested model

address_dict = {"city": "New York",
"state": "NY",
"pin_code": "10001"}
address1 = Address(**address_dict)

patient_dict = {"name": "John Doe",
"age": 30,
"address": address1}
patient1 = Patient(**patient_dict)


temp = patient1.model_dump(exclude_unset=True)
print(temp)
print(type(temp))

temp = patient1.model_dump(exclude={"address": {"pin_code"}})
print(temp)
print(type(temp))

temp = patient1.model_dump(exclude=["name", 'gender'])
print(temp)
print(type(temp))

temp = patient1.model_dump(include=["name", 'gender'])
print(temp)
print(type(temp))

temp = patient1.model_dump_json()
print(temp)
print(type(temp))