from fastapi import APIRouter, Query, Path, Request, HTTPException
from schemas.students_schema import (
    CreateStudentSchema,
    UpdateStudentSchema,
    StudentResponseSchema,
    ListStudentsResponseSchema,
)
from controllers.students_controller import (
    create_student,
    list_students,
    fetch_student,
    update_student,
    delete_student,
)
from slowapi import Limiter
from slowapi.util import get_remote_address
from bson.errors import InvalidId
from bson import ObjectId

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=dict, status_code=201)
@limiter.limit("100/minute")
async def create_student_route(request: Request, student: CreateStudentSchema):
    """Create a new student in the system."""
    return await create_student(student.dict())


@router.get("/", response_model=ListStudentsResponseSchema)
@limiter.limit("100/minute")
async def list_students_route(request: Request, country: str = Query(None), age: int = Query(None)):
    """List students with optional filtering by country and age."""
    filters = {}
    if country:
        filters["address.country"] = country
    if age is not None:
        filters["age"] = {"$gte": age}
    return await list_students(filters)


@router.get("/{id}", response_model=StudentResponseSchema)
@limiter.limit("100/minute")
async def fetch_student_route(request: Request, id: str = Path(...)):
    """Fetch a student by ID."""
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    return await fetch_student(str(object_id))


@router.patch("/{id}", status_code=204)
@limiter.limit("100/minute")
async def update_student_route(request: Request, id: str = Path(...)):
    """Update a student's details."""
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    raw_body = await request.json()
    update_data = {k: v for k, v in raw_body.items() if v is not None}
    return await update_student(str(object_id), update_data)


@router.delete("/{id}", status_code=200)
@limiter.limit("100/minute")
async def delete_student_route(request: Request, id: str = Path(...)):
    """Delete a student by ID."""
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    return await delete_student(str(object_id))