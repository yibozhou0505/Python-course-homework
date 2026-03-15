class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print(f"I am {self.name} and I am {self.age} years old.")

    @staticmethod
    def eat():
        print("I am eating.")

cat = Animal("Kitty", 3)
cat.speak()
cat.eat()