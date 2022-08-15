import mysql.connector as db, mysql, os, sys
from prettytable import PrettyTable

to_insert = [
  {
    'id': 39340, 
    'ident': 'SHCC', 
    'type': 'heliport', 
    'name': 'Clinica Las Condes Heliport',
    'elevation_ft': 2461,
    'municipality': 'Santiago',
    'iata_code': '',
    'score': 25,
  },
  {
    'id': 39379, 
    'ident': 'SHMA', 
    'type': 'heliport', 
    'name': 'Clinica Santa Maria Heliport',
    'elevation_ft': 2028,
    'municipality': 'Santiago',
    'iata_code': '',
    'score': 25,
  },
  {
    'id': 39390, 
    'ident': 'SHPT', 
    'type': 'heliport', 
    'name': 'Portolio Heliport',
    'elevation_ft': 9000,
    'municipality': 'Los Andes',
    'iata_code': '',
    'score': 25,
  }
]


class MySQL():
  user = os.environ.get('MYSQL_USER', default='nico') #NOTE: MySQL Username
  passwd = os.environ.get('MYSQL_PASSWD', default='19989791') # MySQL Password
  port = os.environ.get('MYSQL_PORT',default=3306) # MySQL Port
  mysql_db = os.environ.get('MYSQL_DB', default='InfoAeropuertos') #MySQL DB

  def __init__(self, my_db: str) -> None:
    #NOTE: Item N°4 -> a)
    try:
      #MySQL Connection
      self.db = db.connect(user=self.user, password=self.passwd, db=self.mysql_db, port=self.port)
      self.__is_connected()
    except mysql.connector.errors.InterfaceError as e:
      print('FATAL: MySQL Interface Error\n', e)
    except Exception as e:
      print('FATAL: Another not catched exeption raised\n', e)
      sys.exit(1)

  def __is_connected(self) -> None:
    if self.db.is_connected(): print(f"INFO: Running on {self.db.get_server_info()}")

  def __from_dict(self, data: dict) -> list:
    return [tuple(item.values()) for item in data]

  def insert_data(self, sql_sent: str, data: list) -> bool:
    if data and len(data):
      #NOTE: Item N°4 -> b)
      rtv, cursor = False, self.db.cursor()
      data = self.__from_dict(data)

      cursor.executemany(sql_sent, data)
      self.db.commit()
      count = cursor.rowcount
      if count: rtv = True
      cursor.close()
    return count, rtv
  
  def fetch_data(self, sql_sent: str) -> list:
    #NOTE: Item N°4 -> b)
    cursor = self.db.cursor()
    cursor.execute(sql_sent)
    schema = {k[0]:None for k in cursor.description}
    data = cursor.fetchall()
    return self.__my_encoder(data, schema)


  def __my_encoder(self, obj: any, schema: dict = None) -> any:
    if isinstance(obj, tuple):
      for a in obj: print(a)
    elif isinstance(obj, list):
      rtv, keys = [], list(schema.keys())
      for row in obj: rtv.append({keys[i]:row[i] for i in range(len(keys))})
    return rtv

def main(table: str):
  if table:
    mySQL = MySQL(table)
    table_columns = ", ".join(to_insert[0].keys())
    value_count = ", ".join('%s' for i in range(len(to_insert[0].values())))
    sql_insert = f"INSERT INTO {table}({table_columns}) VALUES({value_count})"
    #NOTE: Item N°4 c)
    count, success = mySQL.insert_data(sql_insert, to_insert)
    if success: 
      pt_i = PrettyTable()
      pt_i.field_names = to_insert[0].keys()
      pt_i.add_rows([list(row.values()) for row in to_insert])
      print(f"INFO: Los datos fueron insertados exitosamente en la tabla {table}.")
      print(f"INFO: {count} filas fueron añadidas.")
      print(pt_i)

    #NOTE: Item N°5
    elevation_ft = 5000
    data = mySQL.fetch_data(f"SELECT name, type, municipality, elevation_ft, iata_code FROM {table} WHERE elevation_ft > {elevation_ft}")
    print(f"INFO: La cantidad de aeropuertos que estan a más de {elevation_ft} pies de altura es: {len(data)}.")
    pt = PrettyTable()
    pt.field_names = data[0].keys()
    pt.add_rows([list(row.values()) for row in data])
    print(pt)
if __name__ == "__main__":
  if(sys.argv[1]):
    main(sys.argv[1])
  else: print('ERROR: Table was not provided.')