import json, requests, datetime, logging, sys, pymongo
from shutil import ExecError
from bson import ObjectId
from pymongo import MongoClient, InsertOne

userAgent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
URL = "https://apis.digital.gob.cl/fl/feriados/2020"

def printLog(message, logfile=open('mp_3.log', 'w'), level=None):
  """
  Can print the list of provided messages to stdout and to a file handler.
  It can also add at the beginnig a severity word based on the level.
  Levels are defined as following -> [0:'INFO:', 1:"WARNING:", 2:"ERROR:", 3:"FATAL:", 9:"DEBUG:"]
  """
  lvl_msg = ""
  levels={0:'INFO:', 1:"WARNING:", 2:"ERROR:", 3:"FATAL:", 9:"DEBUG:"}
  if level is not None and level in levels:
    lvl_msg = levels[level]
  
  if lvl_msg:
    print('====', lvl_msg, message, '====')
  else: 
    print('====', message, '====')
  
  print('====', lvl_msg, message, '====', file=logfile)


class MyDB(MongoClient):
  database = "feriados2020"
  def __init__(self):
    mongoString =  "mongodb://localhost:27017/?retryWrites=true&w=majority"
    super(MyDB, self).__init__(mongoString)
    try:
      printLog('Connected to MongoDB instance', level=0)
    except:
      printLog('Connection to MongoDB instance failed', level=3)
      sys.exit(1)

  def __call__(self, collection: str = None):
    if collection: return self[self.database][collection]
    else: return self[self.database]

  def bulkInsert(self, coll: str, data: list = []):
    if data and len(data) and coll:
      #NOTE: Could be useful turning elem["fecha"] into datetime type
      to_insert = [InsertOne(elem) for elem in data]
      result = self(coll).bulk_write(to_insert)
      if result.inserted_count: printLog(f"{result.inserted_count} elements were added to collection", level=0)
    else: printLog(f"No elements were added to collection {coll}", level=2)

  def fetchData(self, url: str) -> any:
    rtv = None
    try:
      headers = {'Content-Type': 'application/json', 'User-Agent': userAgent}
      request = requests.get(url, headers=headers)
      rtv = request.json()
      if isinstance(rtv, list): printLog(f"Fetched {len(rtv)} elements from {URL}", level=0)
      else: printLog(f"Fetched one document from {URL}", level=0)
    except:
      printLog(f"Failed fetching data from {url}", level=2)
    return rtv
  
  def daysQuery(self, coll: str, query: dict = {}, proj: dict = None) -> list:
    return self.__toDict(self(coll).find(query, proj)) 

  def __mongoEncoder(self, x):
    #print(">>>", type(x))
    if isinstance(x, pymongo.command_cursor.CommandCursor):
      rtv = [self.__toDict(v) for v in x]
    elif isinstance(x, pymongo.results.InsertOneResult):
      rtv = {'_id': str(x.inserted_id)}
    elif isinstance(x, pymongo.cursor.Cursor):
      rtv = [self.__toDict(v) for v in x]
    elif isinstance(x, datetime.datetime):
      rtv = x.strftime("%d.%m.%Y %H:%M:%S")
    elif isinstance(x, ObjectId):
      rtv = str(x)
    elif hasattr(x, '__str__'):
      rtv = str(x)
    else:
      raise TypeError(x)
    return rtv

  def __toDict(self, data: dict = {}): return json.loads(self.__toJson(data))
  
  def __toJson(self, data: dict = {}): return json.dumps(data, ensure_ascii=False, default=self.__mongoEncoder)


def main(insertData: bool = False):
  db, coll = MyDB(), 'dias_feriados'
  #NOTE: Fetch Data from API and write it on DB
  if insertData:
    feriados_data = db.fetchData(URL)
    db.bulkInsert(coll, feriados_data)
  
  printLog("Todos los Feriados de 2020")
  query, proj = {}, {'fecha': 1, 'tipo': 1, 'nombre': 1}
  allDays = db.daysQuery(coll, query, proj)
  for day in allDays:
    printLog(f"El día de {day['nombre']} es un feriado de tipo {day['tipo']} y se celebra el {day['fecha']}")

  printLog("Solo los Feriados Civiles de 2020")
  query = {'tipo': {'$eq': 'Civil'}}
  allDays = db.daysQuery(coll, query, proj)
  for day in allDays:
    printLog(f"El día de {day['nombre']} es un feriado de tipo {day['tipo']} y se celebra el {day['fecha']}")

  printLog("Solo los Feriados Irrenunciables de 2020")
  query = {'irrenunciable': {'$eq': '1'}}
  allDays = db.daysQuery(coll, query, proj)
  for day in allDays:
    printLog(f"El día de {day['nombre']} es un feriado de tipo {day['tipo']} y se celebra el {day['fecha']}")

  printLog('Solo los Feriados que incluyen "Santo" o "Santos"')
  query = {'nombre':  {'$regex': "Santo"}}
  allDays = db.daysQuery(coll, query, proj)
  for day in allDays:
    printLog(f"El día de {day['nombre']} es un feriado de tipo {day['tipo']} y se celebra el {day['fecha']}")

  printLog("Leyes relacionadas con el Plebiscito de Abril")
  query = {'leyes': {'$elemMatch': {'$or': [{'nombre': 'Ley 21.200'}, {'nombre': 'Ley 18.700'}]}}}
  allDays = db.daysQuery(coll, query, proj)
  for day in allDays:
    printLog(f"El día de {day['nombre']} es un feriado de tipo {day['tipo']} y se celebra el {day['fecha']}")

if __name__ == "__main__":
  insertData = False
  if len(sys.argv) >= 2:
    insertData = sys.argv[1]
    if insertData == 'insert': insertData = True
  main(insertData)