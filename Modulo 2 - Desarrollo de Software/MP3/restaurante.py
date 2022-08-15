##############################################################
## Si necesita agregar imports, debe agregarlos aquí arriba ##

### INICIO PARTE 3 ###
class Restaurante:
	def __init__(self, nombre: str, platos: dict, cocineros: list, repartidores: list) -> None:
		self.nombre = nombre
		self.platos = platos
		self.cocineros = cocineros
		self.repartidores = repartidores
		self.calificacion = 0

	def recibir_pedidos(self, clientes: list):
		avaialble_cocineros = self.__check_cocineros()
		if avaialble_cocineros:
			for cliente in clientes:
				pedido, platos_fav = [], cliente.platos_preferidos
				for plato in platos_fav:
					cocinero_designado, avaialble_cocineros = self.__get_cocinero()
					if not avaialble_cocineros: 
						print(f"El plato {plato.nombre} no se cocinará ya que no quedan cocineros con energia disponible.")
					else:
						pedido.append(cocinero_designado.cocinar(self.platos.get(plato)))

				calificacion = None
				if self.__check_repartidores():
					repartidor,_ = self.__get_repartidor()
					#print(f"{pedido}", repartidor.repartir(pedido))
					calificacion = cliente.recibir_pedido(pedido, repartidor.repartir(pedido))
				else:
					calificacion = cliente.recibir_pedido([], 0)
					print("No quedan repartidores con suficiente energía para procesar el pedido.")
				#print('PRE CALIF', self.calificacion)
				self.calificacion = self.calificacion + calificacion
				#print('BEF CALIF', self.calificacion)

		self.calificacion = self.calificacion/len(clientes)

	def __get_cocinero(self) -> any:
		energia_check = sum([cocinero.energia for cocinero in self.cocineros])
		if energia_check > 0:
			return max(self.cocineros, key=lambda c: c.habilidad), True
		else:
			return None, False

	def __get_repartidor(self) -> any:
		energia_check = sum([repartidor.energia for repartidor in self.repartidores])
		if energia_check:
			return min(self.repartidores, key=lambda c: c.tiempo_entrega), True
		else:
			return None, False
	
	def __check_cocineros(self) -> bool: return bool(sum([cocinero.energia for cocinero in self.cocineros]))
	def __check_repartidores(self) -> bool: return bool(sum([repartidor.energia for repartidor in self.repartidores]))
### FIN PARTE 3 #

if __name__ == "__main__":
	### Código para probar que tu clase haya sido creada correctamente  ###
	### Corre directamente este archivo para que este código se ejecute ###
	try:
		PLATOS_PRUEBA = {
			"Pepsi": ["Pepsi", "Bebestible"],
			"Mariscos": ["Mariscos", "Comestible"],
		}
		un_restaurante = Restaurante("Bon Appetit", PLATOS_PRUEBA, [], [])
		print(f"El restaurante {un_restaurante.nombre}, tiene los siguientes platos:")
		for plato in un_restaurante.platos.values():
			print(f" - {plato[1]}: {plato[0]}")
	except TypeError:
		print("Hay una cantidad incorrecta de argumentos en algún inicializador y/o todavía no defines una clase")
	except AttributeError:
		print("Algún atributo esta mal definido y/o todavia no defines una clase")
