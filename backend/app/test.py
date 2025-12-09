
from app.models.container import Container
from app.repositories.container_repo import add_container
from datetime import datetime

def test_add_container():
    test_container = Container(
        LFD=datetime(2025, 2, 1),
        container_number="TEST1234567",
        customer_release=True,
        freight_release=False
    )

    inserted_id = add_container(test_container)
    print("Inserted ID:", inserted_id)


if __name__ == "__main__":
    test_add_container()