from collections import defaultdict
import os, sys

def def_value():
  return "No es una opción"

## Definición funciones ##

CRITERIOS = {'HP': 1, 'Ataque': 2, 'Defensa': 3}
def orden_segun(tipo, criterio):
  if criterio not in CRITERIOS.keys(): print('Criterio no valido');return;
  else:
    types, pkmnIds = pokemon_por_tipo.get(tipo, None), []
    for _type in types:
      for id in _type: pkmnIds.append(info_pokemon.get(id, None))
    theSort = lambda data: data[CRITERIOS[criterio]]
    pkmnIds.sort(key=theSort, reverse=True)
    return [pkmn[0] for pkmn in pkmnIds]

def estadisticas(tipo, criterio):
  if criterio not in CRITERIOS.keys(): print('Criterio no valido');return;
  else:
    types, pkmnIds = pokemon_por_tipo.get(tipo, None), []
    for _type in types:
      for id in _type: pkmnIds.append(info_pokemon.get(id, None))
    selectedCriteria = [pkmn[CRITERIOS[criterio]] for pkmn in pkmnIds]
    _max, _min, _prom = max(selectedCriteria), min(selectedCriteria),  sum(selectedCriteria)/len(pkmnIds)
    return {'min': _min, 'max': _max, 'prom': _prom}

def tipo_segun_nombre(nombre):
  target = None
  for id, value in info_pokemon.items():
    if nombre == value[0]: target = id

  if target:
    tmp_found = ['', '']
    for tipo, pkmns_grp in pokemon_por_tipo.items():
      for i, grp in enumerate(pkmns_grp): 
        if target in grp:
          tmp_found[i] = tipo
    return tuple(tmp_found)



splitCells = lambda row: row.split(',')
splitPkmnType = lambda typeCell: [pkmnType for pkmnType in typeCell.split(';') if pkmnType]
stripCellValue = lambda cellValue: cellValue.strip()

def parseInteger(cellValue: str) -> any:
  try:
    return int(cellValue)
  except ValueError:
    #print(f"{cellValue} was not an integer, returning original value")
    return cellValue

## Lectura archivo y definicion estructuras ##

tipos_de_pokemon, pokemon_por_tipo, info_pokemon = set(), dict(), dict()

csv_path = os.path.join('pokemon.csv')
if not(os.path.exists(csv_path) and os.path.isfile(csv_path)): 
  print('El archivo no existe, saliendo');
  sys.exit(1)
with open(csv_path, 'r', encoding='utf-8') as f:
  csv_headers = f.readline()
  csv_data = f.readlines()
  for line in csv_data:
    cleanedLine = [parseInteger(cellValue) for cellValue in splitCells(line)]
    #print(cleanedLine)
    pkmnTypes = splitPkmnType(cleanedLine[2]) 
    for pkmnType in pkmnTypes:
      tipos_de_pokemon.add(pkmnType)
      pokemon_por_tipo.update({pkmnType: [[],[]]})
    cleanedLine[2] = pkmnTypes  
    info_pokemon.update({str(cleanedLine.pop(0)): cleanedLine})

for id, value in info_pokemon.items():
  pkmnTypes = value.pop(1)
  for i, pkmnType in enumerate(pkmnTypes):
    pokemon_por_tipo.get(pkmnType)[i].append(id)

## Menu flujo principal ##

acciones = defaultdict(def_value)
acciones["1"] = "orden segun"
acciones["2"] = "estadisticas"
acciones["3"] = "encontrar tipo"
acciones["4"] = "revisar"
acciones["0"] = "salir"

continuar = True
while continuar:
    
    print('''
¿Que desea hacer?

1.- Ordenar segun criterio
2.- Obtener estadísticas
3.- Saber el tipo de un pokemon
4.- Revisar Estructuras
0.- Salir
    ''')

    accion = input()
    accion = acciones[accion]

    if accion == "orden segun":
        tipo = input()
        criterio = input()

        orden = orden_segun(tipo, criterio)

        print(f"Ordenando pokemon de tipo {tipo} segun {criterio}:")
        for elem in orden:
            print(f"  - {elem}")

    elif accion == "estadisticas":
        tipo = input()
        criterio = input()

        datos = estadisticas(tipo, criterio)

        print(f"Informacion de {criterio} en pokemon de tipo {tipo}")
        print(f"  - Máximo: {datos['max']}")
        print(f"  - Mínimo: {datos['min']}")
        print(f"  - Promedio: {round(datos['prom'],1)}")

    elif accion == "encontrar tipo":

        nombre = input()

        tipos = tipo_segun_nombre(nombre)
        print(f"El tipo principal de {nombre} es {tipos[0]}")

        if tipos[1] == "":
            print(f"{nombre} no tiene tipo secundario")
        else:
            print(f"El tipo secundario de {nombre} es {tipos[1]}")

    elif accion == "revisar":
        try:
            print("Tipos Encontrados:")
            for tipo in sorted(list(tipos_de_pokemon)):
                print(f"  - {tipo}")

            print("")

            p = pokemon_por_tipo["Electric"]
            print(f"Revisando Primarios: {'25' in p[0]}")
            print(f"Revisando Secundarios: {'170' in p[1]}")

            print("")

            print("Pokemon Ejemplo:")
            i = info_pokemon["25"]
            esta = "Electric" in i
            print(f"  - ID: 25")
            print(f"  - Nombre: {i[0]}")
            print(f"  - Esta Tipo: {esta}")
        except NameError:
            print("Esta parte no se puede ejecutar ya que aún no has definido todas las estructuras")
            

    elif accion == "salir":
        continuar = False

    else:
        print(accion)