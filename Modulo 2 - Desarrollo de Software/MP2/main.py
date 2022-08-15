from pprint import pprint
import parametros as p
import random

###### INICIO PUNTO 1 ######
### Rellenar Clase Automóvil ###
class Automovil:
	def __init__(self, kilometraje, año) -> None:
		self.__kilometraje = kilometraje
		self.ano = año
		self.ruedas = list()
		self.aceleracion = 0
		self.velocidad = 0

	#NOTE: Debug only
	def __call__(self) -> dict: return pprint({k:v for k,v in self.__dict__.items()})

	def avanzar(self, tiempo: int) -> None:
		self.kilometraje = self.velocidad*tiempo
	
	def acelerar(self, tiempo: int) -> None:
		self.aceleracion = tiempo*0.5
		self.velocidad += self.aceleracion*tiempo*3.6
		self.avanzar(tiempo)
		self.aceleracion = 0

	def frenar(self, tiempo: int) -> None:
		self.aceleracion -=  tiempo*0.5
		self.velocidad += self.aceleracion*tiempo*3.6
		self.velocidad = 0 if self.velocidad < 0 else self.velocidad
		self.avanzar(tiempo)
		self.aceleracion = 0
	
	def obtener_kilometros(self) -> int:
		return self.kilometraje
	
	def reemplazar_rueda(self) -> None:
		self.ruedas.pop(self.ruedas.index(min(self.ruedas, key=lambda x: x.resistencia_actual)))
		self.ruedas.append(Rueda())

###### FIN PUNTO 1 ######


###### INICIO PUNTO 2 ######
### Rellenar Clase Moto ###
class Moto(Automovil): 
	def __init__(self, kilometraje, año, cilindrada) -> None:
		self.cilindrada = cilindrada
		super().__init__(kilometraje, año)
		for _ in range(2): self.ruedas.append(Rueda())

	def acelerar(self, tiempo: int) -> None:
		super().acelerar(tiempo)
		for rueda in self.ruedas: rueda.gastar('acelerar')

	def frenar(self, tiempo: int) -> None:
		super().frenar(tiempo)
		for rueda in self.ruedas: rueda.gastar('frenar')	

	def __str__(self):
		return f"Moto del año {self.ano}."

	def estado(self):
		estado_vehiculo = f"----- Moto -----\nInformación:\n - Año: {self.ano}\n - Velocidad: {self.velocidad} km/s\n"
		estado_vehiculo += f" - Kilometraje: {self._Automovil__kilometraje} km\n - Cilindrada: {self.cilindrada}\n"
		estado_ruedas = "Estado Ruedas:\n"+"".join([f" - Rueda {i+1} - Resistencia Actual: {str(rueda.resistencia_actual)}\n" for i, rueda in enumerate(self.ruedas)])
		return estado_vehiculo+estado_ruedas+"----------------"
###### FIN PUNTO 2 ######


###### INICIO PUNTO 3 ######
### Rellenar Clase Camión ###
class Camion(Automovil):
	def __init__(self, kilometraje, año, carga) -> None:
		self.carga = carga
		super().__init__(kilometraje, año)
		for _ in range(6): self.ruedas.append(Rueda())

	def acelerar(self, tiempo: int) -> None:
		super().acelerar(tiempo)
		for rueda in self.ruedas: rueda.gastar('acelerar')

	def frenar(self, tiempo: int) -> None:
		super().frenar(tiempo)
		for rueda in self.ruedas: rueda.gastar('frenar')

	def __str__(self):
		return f"Camión del año {self.ano}."

	def estado(self):
		estado_vehiculo = f"----- Camión -----\nInformación:\n - Año: {self.ano}\n - Velocidad: {self.velocidad} km/s\n"
		estado_vehiculo += f" - Kilometraje: {self._Automovil__kilometraje} km\n - Carga Máxima: {self.carga} kg\n"
		estado_ruedas = "Estado Ruedas:\n"+"".join([f" - Rueda {i} - Resistencia Actual: {str(rueda.resistencia_actual)}\n" for i, rueda in enumerate(self.ruedas)])
		return estado_vehiculo+estado_ruedas+"------------------"
###### FIN PUNTO 3 ######


### Esta clase está completa, NO MODIFICAR ###
class Rueda:
	def __init__(self):
		self.resistencia_actual = random.randint(*p.RESISTENCIA)
		self.resistencia_total = self.resistencia_actual
		self.estado = "Perfecto"

	def gastar(self, accion):
			if accion == "acelerar":
				self.resistencia_actual -= 5
			elif accion == "frenar":
				self.resistencia_actual -= 10
			self.actualizar_estado()

	def actualizar_estado(self):
		if self.resistencia_actual < 0:
				self.estado = "Rota"
		elif self.resistencia_actual < self.resistencia_total / 2:
				self.estado = "Gastada"
		elif self.resistencia_actual < self.resistencia_total:
				self.estado = "Usada"

### Esta funcion está completa, NO MODIFICAR ###
#NOTE: Modificado ya que en el codigo original no se estaba modificando el vehiculo seleccionado
def seleccionar():
	for indice in range(len(vehiculos)):
		print(f"[{indice}] {str(vehiculos[indice])}")

	elegido = int(input())
	if elegido >= 0 and elegido < len(vehiculos):
		vehiculo = vehiculos[elegido]
		print("Se seleccionó el vehículo", str(vehiculo))
	else:
		print("intentelo denuevo.")
	return vehiculo


###### INICIO PUNTO 4.2 ######
### Se debe completar cada opción según lo indicado en el enunciado ###
def accion(vehiculo, opcion):
	if opcion == 2: #Acelerar
		tiempo = get_time_input("Acelerar")
		vehiculo.acelerar(tiempo)
		print(f"Se ha acelerado por {tiempo} segundos llegando a una velocidad de {vehiculo.velocidad} km/h")
	elif opcion == 3: #Frenar
		tiempo = get_time_input("Frenar")
		vehiculo.frenar(tiempo)
		print(f"Se ha frenado por {tiempo} segundos llegando a una velocidad de {vehiculo.velocidad} km/h")
	elif opcion == 4: #Avanzar
		tiempo = get_time_input("Avanzar")
		vehiculo.avanzar(tiempo)
		print(f"Se ha avanzado por {tiempo} segundos a una velocidad de {vehiculo.velocidad} km/h")
	elif opcion == 5: #Cambiar Rueda
		vehiculo.reemplazar_rueda()
		print("Se ha reemplazado una rueda con exito")
	elif opcion == 6: #Mostrar Estado
		print(vehiculo.estado())

def get_time_input(action) -> int:
	valid = False
	while not valid:
		try:
			tiempo = int(input(f"Ingrese el tiempo (segundos) para {action} el vehículo: "))
			if not tiempo: raise ValueError
			valid = True
		except ValueError:
			print("El tiempo ingresado no es valido, ingresa un valor entero")
	return tiempo

###### FIN PUNTO 4.2 #####

if __name__ == "__main__":

	###### INICIO PUNTO 4.1 ######
	### Aca deben instanciar los vehiculos indicados
	moto, camion = Moto(80000, 2020, 1400), Camion(0, 2022, 11785)
	### en el enunciado y agregarlos a la lista vehiculos
	vehiculos = [moto, camion]

	###### FIN PUNTO 4.1 ######


	### El codigo de abajo NO SE MODIFICA ###
	vehiculo = vehiculos[0] # Por default comienza seleccionado el primer vehículo  

	dict_opciones = {1: ("Seleccionar Vehiculo", seleccionar),
										2: ("Acelerar", accion),
										3: ("Frenar", accion),
										4: ("Avanzar", accion),
										5: ("Reemplazar Rueda", accion),
										6: ("Mostrar Estado", accion),
										0: ("Salir", None)
									}

	op = -1
	while op != 0:
			
			for k, v in dict_opciones.items():
					print(f"{k}: {v[0]}")
			
			try:
					op = int(input("Opción: "))
			
			except ValueError:
					print(f"Ingrese opción válida.")
					op = -1
			
			if op != 0 and op in dict_opciones.keys():
					if op == 1:  #NOTE: Modificado ya que en el codigo original no se estaba modificando el vehiculo seleccionado
						vehiculo = dict_opciones[op][1]()
					else:
							dict_opciones[op][1](vehiculo, op)
			elif op == 0:
					pass
			else:
					print(f"Ingrese opción válida.")
					op = -1
