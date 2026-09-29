class Animal:
    def __init__(self, nome: str):
        self.nome = nome

class Cachorro(Animal):
    def latir(self) -> str:
        return f"{self.nome} faz: Au Au!"
      
