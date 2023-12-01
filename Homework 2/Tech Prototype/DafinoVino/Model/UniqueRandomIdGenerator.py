import random
import uuid


class UniqueRandomIdGenerator:
    def __init__(self):
        self.generated_ids = set()

    def generate_random_id(self):
        while True:
            random_id = str(uuid.uuid4())
            if random_id not in self.generated_ids:
                self.generated_ids.add(random_id)
                return random_id
