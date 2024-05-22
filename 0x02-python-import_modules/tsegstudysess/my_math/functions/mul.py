import uuid

class Person:
    def __init__(self, name, age, address):
        self.uuid = uuid.uuid4()
        self.name = name
        self.age = age
        self.address = address

    def get_uuid(self):
        return str(self.uuid)

# Create instances of Person
person1 = Person("John Doe", 30, "123 Main St")
person2 = Person("Jane Smith", 25, "456 Elm St")

# Access the UUIDs of the Person objects
print(person1.get_uuid())
print(person2.get_uuid())