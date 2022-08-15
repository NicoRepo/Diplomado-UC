##############################################################
from random import randint
from platos import Comestible, Bebestible
## Si necesita agregar imports, debe agregarlos aquí arriba ##

### INICIO PARTE 2.1 ###
class Persona:
	def __init__(self, nombre: str) -> None:
		self.nombre = nombre
### FIN PARTE 2.1 ###

### INICIO PARTE 2.2 ###
class Repartidor(Persona):
	def __init__(self, nombre: str, tiempo_entrega: int) -> None:
		super().__init__(nombre)
		self.tiempo_entrega = tiempo_entrega 
		self.energia = randint(75, 100)
	
	def repartir(self, pedido: list) -> int:
		factor_tamaño, factor_velocidad = self.__calculate_factors(len(pedido))
		self.energia -= factor_tamaño
		tiempo_demora = factor_velocidad*self.tiempo_entrega
		print(f"El repartidor {self.nombre} se ha demorado {tiempo_demora} y perdiendo {factor_tamaño} de energia.")
		return tiempo_demora

	def __calculate_factors(self, pedido_len: int):
		f_tam, f_vel = None, None
		if pedido_len <= 2:
			f_tam, f_vel = 5, 1.25
		elif pedido_len >= 3:
			f_tam, f_vel = 15, 0.85
		return f_tam, f_vel
### FIN PARTE 2.2 ###

### INICIO PARTE 2.3 ###
class Cocinero(Persona):
	def __init__(self, nombre: str, habilidad: int) -> None:
		super().__init__(nombre)
		self.nombre = nombre
		self.habilidad = habilidad
		self.energia = randint(50, 80)

	def cocinar(self, informacion_plato: list):
		plato = self.__classify_dish(informacion_plato)
		if isinstance(plato, Comestible): coste_energia = 15
		elif isinstance(plato, Bebestible): 
			coste_energia = self.__bebestible_logic(plato)
		factor_calidad = 0.7 if plato.dificultad > self.habilidad else 1.5
		plato.calidad *= factor_calidad
		self.energia -= coste_energia
		print(f"El cocinero {self.nombre} ha cocinado {plato} perdiendo {coste_energia} de energía.")
		return plato

	def __bebestible_logic(self, plato: Bebestible) -> None:
		bebestible_energy_map = {"Pequeño": 5, "Mediano": 8, "Grande": 10}
		try:
			coste_energia = bebestible_energy_map.get(plato.tamano, 0)
		except TypeError as e:
			print(f"La energia requerida para un plato de tamaño {plato.tamano} no esta registrada.", e)
		finally: return coste_energia

	def __classify_dish(self, informacion_plato: list) -> any:
		nombre_plato, tipo_plato = informacion_plato
		if tipo_plato == "Bebestible": return Bebestible(nombre_plato)
		elif tipo_plato == "Comestible": return Comestible(nombre_plato)

### FIN PARTE 2.3 ###

### INICIO PARTE 2.4 ###
class Cliente(Persona):
	def __init__(self, nombre: str, platos_preferidos: list) -> None:
		super().__init__(nombre)
		self.platos_preferidos = platos_preferidos #["PLato a", "platob"]

	def recibir_pedido(self, pedido: list, demora: int):
		calificacion = 10
		if len(pedido) < len(self.platos_preferidos) or demora >= 20:
			calificacion = calificacion/2
		for plato in pedido:
			if plato.calidad >= 11:
				calificacion += 1.5
			elif plato.calidad <= 8:
				calificacion -= 3
			else: pass
		print(f"El cliente {self.nombre} ha recibido su pedido y le puso una calificacion {calificacion}.")
		return calificacion

		
### FIN PARTE 2.4 ###

if __name__ == "__main__":

    ### Código para probar que tu clase haya sido creada correctamente  ###
    ### Corre directamente este archivo para que este código se ejecute ###
    try:
        PLATOS_PRUEBA = {
        "Jugo Natural": ["Jugo Natural", "Bebestible"],
        "Empanadas": ["Empanadas", "Comestible"],
        }
        un_cocinero = Cocinero("Cristian", randint(1, 10))
        un_repartidor = Repartidor("Tomás", randint(20, 30))
        un_cliente = Cliente("Alberto", PLATOS_PRUEBA)
        print(f"El cocinero {un_cocinero.nombre} tiene una habilidad: {un_cocinero.habilidad}")
        print(f"El repatidor {un_repartidor.nombre} tiene una tiempo de entrega: {un_repartidor.tiempo_entrega} seg")
        print(f"El cliente {un_cliente.nombre} tiene los siguientes platos favoritos:")
        for plato in un_cliente.platos_preferidos.values():
            print(f" - {plato[1]}: {plato[0]}")
    except TypeError:
        print("Hay una cantidad incorrecta de argumentos en algún inicializador y/o todavía no defines una clase")
    except AttributeError:
        print("Algún atributo esta mal definido y/o todavia no defines una clase")
