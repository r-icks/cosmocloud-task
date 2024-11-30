from pydantic import BaseModel, Field
from typing import Optional, List


class AddressSchema(BaseModel):
    city: str = Field(..., example="New York")
    country: str = Field(..., example="USA")


class CreateStudentSchema(BaseModel):
    name: str = Field(..., example="John Doe")
    age: int = Field(..., example=20, gt=0, lt=150)
    address: AddressSchema


class PartialAddressSchema(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None


class UpdateStudentSchema(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(None, gt=0, lt=150)
    address: Optional[PartialAddressSchema] = None


class StudentResponseSchema(BaseModel):
    name: str
    age: int
    address: AddressSchema


class StudentListResponseSchema(BaseModel):
    name: str
    age: int


class ListStudentsResponseSchema(BaseModel):
    data: List[StudentListResponseSchema]