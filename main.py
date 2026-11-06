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
class DataSerializer: pass
class PetManager: pass
