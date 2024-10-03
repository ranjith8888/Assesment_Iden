import json
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize the Faker instance
fake = Faker()

# Function to generate fake data
def generate_fake_data(num_entries):
    data = []
    for _ in range(num_entries):
        entry = {
            "Name": fake.name(),
            "Email": fake.email(),
            "Role": random.choice(["Admin", "User", "Editor", "Viewer"]),
            "Is Admin": random.choice([True, False]),
            "Created At": fake.date_time_this_decade().isoformat()
        }
        data.append(entry)
    return data

# Generate 100 entries
fake_data = generate_fake_data(100)

# Print the JSON data
print(json.dumps(fake_data, indent=2))

# Optionally, save to a file
with open("fake_data.json", "w") as f:
    json.dump(fake_data, f, indent=2)
