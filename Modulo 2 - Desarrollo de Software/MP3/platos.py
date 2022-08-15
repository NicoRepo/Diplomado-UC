##############################################################
from random import randint, choice
## Si necesita agregar imports, debe agregarlos aquí arriba ##

SIZES = ["Pequeño", "Mediano", "Grande"]

### INICIO PARTE 1.1 ###
class Plato:
	def __init__(self, nombre: str):
		self.nombre = nombre
		self.calidad = 0

### FIN PARTE 1.1 ###

### INICIO PARTE 1.2 ###

class Bebestible(Plato):
	def __init__(self, nombre: str) -> None:
		super().__init__(nombre)
		self.tamano = choice(SIZES)
		self.__class_logic()

	def __class_logic(self) -> None:
		size_to_difficult = {"Pequeño": 3, "Mediano": 6, "Grande": 9}
		self.dificultad = size_to_difficult[str(self.tamano)]
		self.calidad = randint(3, 8)

	def __str__(self) -> str:
		return f"Bebestible - {self.nombre} | Tamaño {self.tamano} - Calidad {self.calidad} - Dificultad {self.dificultad}"
### FIN PARTE 1.2 ###

### INICIO PARTE 1.3 ###
class Comestible(Plato):
	def __init__(self, nombre: str) -> None:
		super().__init__(nombre)
		self.dificultad = randint(1, 10)
		self.calidad = randint(5, 10)
	
	def __str__(self) -> str:
		return f"Comestible - {self.nombre} | Calidad {self.calidad} - Dificultad {self.dificultad}"
### FIN PARTE 1.3 ###

if __name__ == "__main__":
    ### Código para probar que tu clase haya sido creada correctamente  ###
    ### Corre directamente este archivo para que este código se ejecute ###
    try:
        un_bebestible = Bebestible("Coca-Cola")
        un_comestible = Comestible("Sopa")
        print(f"Esto es una {un_bebestible.nombre} de tamaño {un_bebestible.tamano} y calidad {un_bebestible.calidad}.")
        print(f"Esto es una {un_comestible.nombre} de dificultad {un_comestible.dificultad} y calidad {un_comestible.calidad}.")
    except TypeError:
        print("Hay una cantidad incorrecta de argumentos en algún inicializador y/o todavía no defines una clase")
    except AttributeError:
        print("Algún atributo esta mal definido y/o todavia no defines una clase")
