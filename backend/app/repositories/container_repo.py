from app.db.mongo import get_container_collection
from app.models.container import Container, TerminalName
from pymongo.results import UpdateResult
from bson import ObjectId
from typing import Optional, List
from datetime import date, datetime
from motor.motor_asyncio import AsyncIOMotorCollection



# ==================== CREATE OPERATIONS ====================

# def add_container(container: Container) -> str:
#     """
#     Insert a Container model into MongoDB.
#     Returns the inserted document's ID as a string.
#     """
#     # Convert Pydantic model → dict
#     document = container.model_dump()

#     # Insert into MongoDB
#     result = collection.insert_one(document)

#     # Return _id as string
#     return str(result.inserted_id)


def add_containers(containers: List[Container]) -> List[str]:
    """
    Insert multiple Container models into MongoDB.
    Returns a list of inserted document IDs as strings.
    """
    pass


# # ==================== READ OPERATIONS ====================

async def get_unchecked_containers_by_terminal(collection, terminal: str):
    cursor = collection.find({
        "terminal": terminal,
        "$or": [
            {"check": False},
            {"check": {"$exists": False}}
        ]
    })
    return [Container(**doc) async for doc in cursor]

# def get_container_by_id(container_id: str) -> Optional[Container]:
#     """
#     Retrieve a container by its MongoDB _id.
#     Returns Container model or None if not found.
#     """
#     pass


# def get_container_by_number(container_number: str) -> Optional[Container]:
#     """
#     Retrieve a container by its container_number.
#     Returns Container model or None if not found.
#     """
#     pass


# def get_all_containers(limit: Optional[int] = None, skip: Optional[int] = None) -> List[Container]:
#     """
#     Retrieve all containers from the database.
#     Optional limit and skip for pagination.
#     Returns a list of Container models.
#     """
#     pass


# def get_containers_by_terminal(terminal: TerminalName) -> List[Container]:
#     """
#     Retrieve all containers for a specific terminal.
#     Returns a list of Container models.
#     """
#     pass


# def get_containers_by_availability(available: bool) -> List[Container]:
#     """
#     Retrieve containers filtered by availability status.
#     Returns a list of Container models.
#     """
#     pass


# def get_containers_by_release_status(
#     customs_release: Optional[bool] = None,
#     freight_release: Optional[bool] = None
# ) -> List[Container]:
#     """
#     Retrieve containers filtered by release status.
#     Both parameters are optional - can filter by one or both.
#     Returns a list of Container models.
#     """
#     pass


# def get_containers_by_last_free_day(
#     start_date: Optional[date] = None,
#     end_date: Optional[date] = None
# ) -> List[Container]:
#     """
#     Retrieve containers filtered by last_free_day date range.
#     Both parameters are optional - can filter by start, end, or both.
#     Returns a list of Container models.
#     """
#     pass


# def search_containers(
#     container_number: Optional[str] = None,
#     terminal: Optional[TerminalName] = None,
#     available: Optional[bool] = None,
#     customs_release: Optional[bool] = None,
#     freight_release: Optional[bool] = None
# ) -> List[Container]:
#     """
#     Advanced search for containers with multiple optional filters.
#     Returns a list of Container models matching all specified criteria.
#     """
#     pass


# # ==================== UPDATE OPERATIONS ====================

# def update_container_by_id(container_id: str, container: Container) -> bool:
#     """
#     Update a container by its MongoDB _id.
#     Returns True if update was successful, False if container not found.
#     """
#     pass


async def update_container_by_number(
    container_number: str,
    container: Container,
    collection
) -> bool:
    """
    Update a container by its container_number.
    Returns True if update was successful, False if container not found.
    """

    update_data = container.model_dump()
    update_data["updated_at"] = datetime.utcnow()

    result: UpdateResult = await collection.update_one(
        {"container_number": container_number},
        {"$set": update_data},
        upsert=True   # ❗ do NOT create new container
    )

    return result.matched_count > 0



async def update_containers_bulk(
    filter_criteria: dict,
    container: Container,
    collection
) -> int:
    """
    Update multiple containers matching the filter criteria
    using values from a Container object.
    Returns the number of documents updated.
    """

    # Convert Pydantic model → dict, skip None values
    update_data = container.model_dump(exclude_none=True)

    # Never allow overwriting the identifier
    update_data.pop("container_number", None)

    # Audit timestamp
    update_data["updated_at"] = datetime.utcnow()

    result = await collection.update_many(
        filter_criteria,
        {"$set": update_data},
        upsert=True  # ❗ do NOT create new containers
    )

    return result.modified_count

# # ==================== DELETE OPERATIONS ====================

# def delete_container_by_id(container_id: str) -> bool:
#     """
#     Delete a container by its MongoDB _id.
#     Returns True if deletion was successful, False if container not found.
#     """
#     pass


# def delete_container_by_number(container_number: str) -> bool:
#     """
#     Delete a container by its container_number.
#     Returns True if deletion was successful, False if container not found.
#     """
#     pass


# def delete_containers_by_terminal(terminal: TerminalName) -> int:
#     """
#     Delete all containers for a specific terminal.
#     Returns the number of documents deleted.
#     """
#     pass


# def delete_containers_bulk(filter_criteria: dict) -> int:
#     """
#     Delete multiple containers matching the filter criteria.
#     Returns the number of documents deleted.
#     """
#     pass


# # ==================== UTILITY OPERATIONS ====================

# def container_exists(container_number: str) -> bool:
#     """
#     Check if a container with the given container_number exists.
#     Returns True if exists, False otherwise.
#     """
#     pass


# def count_containers(filter_criteria: Optional[dict] = None) -> int:
#     """
#     Count containers matching optional filter criteria.
#     Returns the total count.
#     """
#     pass


# def get_containers_statistics() -> dict:
#     """
#     Get aggregated statistics about containers.
#     Returns a dictionary with statistics (e.g., counts by terminal, availability, etc.).
#     """
#     pass