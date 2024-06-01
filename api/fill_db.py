import datetime
import random
import requests
import faker


# Clear db
def clear_db():
    for id in range(1, 11):
        requests.delete(f"http://127.0.0.1:8080/users/{id}/delete")

    for id in range(1, 6):
        requests.delete(f"http://127.0.0.1:8080/offices/{id}/delete")
        requests.delete(f"http://127.0.0.1:8080/services/{id}/delete")


# Create services
def create_services():
    requests.post("http://127.0.0.1:8080/services/create/all")


# Create users
def create_users():
    for _ in range(10):
        user = faker.Faker(locale="en")
        phone_number = faker.Faker(locale="ru").phone_number()
        data = {}
        data["first_name"] = user.name().split(" ")[1]
        data["last_name"] = user.name().split(" ")[0]
        data["email"] = user.email()
        data["phone_number"] = (
            phone_number.replace("+7", "8").replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        )
        # print(data)
        print(requests.post("http://127.0.0.1:8080/users/create", json=data).json())


# Create offices
def create_offices():
    for _ in range(5):
        office = faker.Faker(locale="ru")
        data = {}
        data["address"] = office.address()
        data["phone_number"] = (
            office.address().replace("+7", "8").replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        )
        # print(data)
        print(requests.post("http://127.0.0.1:8080/offices/create", json=data).json())


# Add services to offices
def add_services_offices():
    service_types = ["Gym", "Pool", "Sauna", "Yoga", "Crossfit"]

    for office_id in range(1, 6):
        indexes = set()
        while len(indexes) != 2:
            indexes.add(random.randint(0, 4))
        indexes = list(indexes)

        requests.put(
            f"http://127.0.0.1:8080/offices/{office_id}/add-service",
            params={"service_type": service_types[indexes[0]]},
        )
        requests.put(
            f"http://127.0.0.1:8080/offices/{office_id}/add-service",
            params={"service_type": service_types[indexes[1]]},
        )


# Create tariffs
def create_tariffs():
    periods = [30, 90, 180, 365]
    for i in range(4):
        data = {
            "period": periods[i],
            "price": random.randint(100, 1000),
        }
        print(requests.post("http://127.0.0.1:8080/tariffs/create", json=data).json())


# Create memberships
def create_memberships():
    for user_id in range(1, 11):
        office_id = random.randint(1, 5)
        start_date = datetime.date.today() + datetime.timedelta(days=random.randint(1, 30))
        data = {}
        data["user_id"] = user_id
        data["office_id"] = office_id
        data["start_date"] = str(start_date)
        data["period"] = random.choice([30, 90, 180, 365])
        # print(data)
        print(requests.post("http://127.0.0.1:8080/memberships/create", json=data).json())


if __name__ == "__main__":
    # clear_db()
    create_services()
    create_users()
    create_offices()
    add_services_offices()
    create_tariffs()
    create_memberships()
