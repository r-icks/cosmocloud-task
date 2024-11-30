from bson.objectid import ObjectId
from fastapi import HTTPException
from config.database import db
import bleach
import logging

collection = db["students"]


def sanitize_input(data: dict) -> dict:
    """Sanitize input to prevent malicious data."""
    if "name" in data and data["name"] is not None:
        data["name"] = bleach.clean(data["name"])

    if "address" in data and data["address"] is not None:
        if "city" in data["address"] and data["address"]["city"] is not None:
            data["address"]["city"] = bleach.clean(data["address"]["city"])
        if "country" in data["address"] and data["address"]["country"] is not None:
            data["address"]["country"] = bleach.clean(data["address"]["country"])

    return data


async def create_student(student: dict):
    """Insert a new student into the database."""
    sanitized_student = sanitize_input(student)
    result = collection.insert_one(sanitized_student)
    logging.info(f"Created student with ID: {result.inserted_id}")
    return {"id": str(result.inserted_id)}


async def list_students(filters: dict):
    """List students with optional filters."""
    students = list(collection.find(filters))
    result = [{"name": student["name"], "age": student["age"]} for student in students]
    return {"data": result}


async def fetch_student(student_id: str):
    """Fetch a student by ID."""
    student = collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "name": student["name"],
        "age": student["age"],
        "address": {
            "city": student["address"]["city"],
            "country": student["address"]["country"],
        },
    }


async def update_student(student_id: str, update_data: dict):
    """Update a student's details."""
    existing_student = collection.find_one({"_id": ObjectId(student_id)})
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    if "address" in update_data:
        existing_address = existing_student.get("address", {})
        update_data["address"] = {**existing_address, **update_data["address"]}

    sanitized_data = sanitize_input(update_data)

    if "address" in sanitized_data and not any(sanitized_data["address"].values()):
        sanitized_data.pop("address")

    result = collection.update_one({"_id": ObjectId(student_id)}, {"$set": sanitized_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    logging.info(f"Updated student with ID: {student_id}")
    return {"detail": "Student updated successfully"}


async def delete_student(student_id: str):
    """Delete a student by ID."""
    result = collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    logging.info(f"Deleted student with ID: {student_id}")
    return {"detail": "Student deleted successfully"}