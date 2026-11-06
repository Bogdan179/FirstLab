from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, id: int):
        self.id = id

class Animal(Entity):
    def __init__(self, id: int, name: str, age: int):
        super().__init__(id)
        self.name = name
        self.age = age

class Dog(Animal):
    def __init__(self, id: int, name: str, age: str, breed: str):
        super().__init__(id, name, age)
        self.breed = breed

class Cat(Animal):
    def __init__(self, id: int, name: str, age: str, color: str):
        super().__init__(id, name, age)
        self.color = color

class Bird(Animal):
    def __init__(self, id: int, name: str, age: str, wingspan: float):
        super().__init__(id, name, age)
        self.wingspan = wingspan

class Owner(Entity):
    def __init__(self, id: int, full_name: str, phone: str):
        super().__init__(id)
        self.full_name = full_name
        self.phone = phone

class Vaccination(Entity): pass
class VetClinic(Entity): pass
class Shelter(Entity): pass
class DataSerializer:
    @staticmethod
    def save_to_json(data: list, filename: str):
        with open(filename, 'w') as f:
            json.dump([obj.__dict__ for obj in data], f)

    @staticmethod
    def load_from_json(filename: str):
        with open(filename, 'r') as f:
            return json.load(f)

class PetManager:
    def __init__(self):
        self.animals = []

    def add_animal(self, animal: Animal):
        self.animals.append(animal)
        print(f"Added {animal.name}")

manager = PetManager()
manager.add_animal(Dog(1, "Rex", "5", "Shepherd"))
DataSerializer.save_to_json(manager.animals, "data.json")
