from faker import Faker; fake = Faker()
def user_payload(status="active", gender=None):
    return {
      "name": fake.name(),
      "email": f"{fake.user_name()}_{fake.uuid4()}@example.com",
      "gender": gender or fake.random_element(("male","female")),
      "status": status,
    }