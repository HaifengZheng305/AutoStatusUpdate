from app.db.mongo import get_container_collection
from app.models.container import Container
from bson import ObjectId

collection = get_container_collection()

def add_container(container: Container) -> str:
    """
    Insert a Container model into MongoDB.
    Returns the inserted document's ID as a string.
    """
    # Convert Pydantic model → dict
    document = container.model_dump()

    # Insert into MongoDB
    result = collection.insert_one(document)

    # Return _id as string
    return str(result.inserted_id)