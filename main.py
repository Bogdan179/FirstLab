import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class PetManagerError(Exception):
    pass

class InvalidAgeError(PetManagerError):
    pass

class Entity(ABC):
    def __init__(self, id: int):
        self.id = id

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

class Animal(Entity):
    def __init__(self, id: int, name: str, age: int): # ИСПРАВЛЕНО: age теперь int
        super().__init__(id)
        if age < 0:
            raise InvalidAgeError(f"Возраст не может быть отрицательным: {age}")
        self.name = name
        self.age = age

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name, "age": self.age, "type": self.__class__.__name__}

class Dog(Animal):
    def __init__(self, id: int, name: str, age: int, breed: str):
        super().__init__(id, name, age)
        self.breed = breed
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["breed"] = self.breed
        return data

class Cat(Animal):
    def __init__(self, id: int, name: str, age: int, color: str):
        super().__init__(id, name, age)
        self.color = color

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["color"] = self.color
        return data

class Bird(Animal):
    def __init__(self, id: int, name: str, age: int, wingspan: float):
        super().__init__(id, name, age)
        self.wingspan = wingspan

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["wingspan"] = self.wingspan
        return data

class Owner(Entity):
    def __init__(self, id: int, full_name: str, phone: str):
        super().__init__(id)
        self.full_name = full_name
        self.phone = phone
    
    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "full_name": self.full_name, "phone": self.phone}

class Vaccination(Entity):
    def __init__(self, id: int, vaccine_name: str, date: str):
        super().__init__(id)
        self.vaccine_name = vaccine_name
        self.date = date
    
    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "vaccine_name": self.vaccine_name, "date": self.date}

class VetClinic(Entity):
    def __init__(self, id: int, name: str, address: str):
        super().__init__(id)
        self.name = name
        self.address = address

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name, "address": self.address}

class Shelter(Entity):
    def __init__(self, id: int, name: str, capacity: int):
        super().__init__(id)
        self.name = name
        self.capacity = capacity
        
    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name, "capacity": self.capacity}

class DataSerializer:
    
    @staticmethod
    def save_to_json(data: List[Entity], filename: str) -> None:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([item.to_dict() for item in data], f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка записи JSON: {e}")

    @staticmethod
    def load_from_json(filename: str) -> List[Dict[str, Any]]:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Файл {filename} не найден. Возвращен пустой список.")
            return []
        except json.JSONDecodeError:
            print("Ошибка формата JSON.")
            return []

    @staticmethod
    def save_to_xml(data: List[Entity], filename: str) -> None:
        root = ET.Element("Entities")
        for item in data:
            elem = ET.SubElement(root, item.__class__.__name__)
            for key, value in item.to_dict().items():
                child = ET.SubElement(elem, key)
                child.text = str(value)
        
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)

class PetManager:
    def __init__(self) -> None:
        self.animals: List[Animal] = []
        self.owners: List[Owner] = []

    def add_animal(self, animal: Animal) -> None:
        if any(a.id == animal.id for a in self.animals):
            raise PetManagerError(f"Животное с ID {animal.id} уже существует.")
        self.animals.append(animal)
        print(f"Успешно добавлено: {animal.name}")

    def get_animal(self, animal_id: int) -> Optional[Animal]:
        for animal in self.animals:
            if animal.id == animal_id:
                return animal
        return None

    def update_animal_age(self, animal_id: int, new_age: int) -> None:
        animal = self.get_animal(animal_id)
        if animal:
            animal.age = new_age
            print(f"Возраст {animal.name} обновлен на {new_age}.")
        else:
            raise PetManagerError("Животное не найдено.")

    def delete_animal(self, animal_id: int) -> None:
        animal = self.get_animal(animal_id)
        if animal:
            self.animals.remove(animal)
            print(f"{animal.name} удален.")
        else:
            raise PetManagerError("Животное не найдено.")


if __name__ == "__main__":
    try:
        manager = PetManager()
        dog = Dog(1, "Buddy", 3, "Golden Retriever")
        cat = Cat(2, "Murka", 2, "White")
        manager.add_animal(dog)
        manager.add_animal(cat)
        DataSerializer.save_to_json(manager.animals, "pets.json")
        DataSerializer.save_to_xml(manager.animals, "pets.xml")

        loaded_data = DataSerializer.load_from_json("pets.json")
        print(f"Загружено записей: {len(loaded_data)}")
        
    except InvalidAgeError as e:
        print(f"Ошибка валидации: {e}")
    except PetManagerError as e:
        print(f"Ошибка менеджера: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
