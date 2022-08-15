import csv, mysql.connector as db, chardet, os, sys
from detect_delimiter import detect
from pathlib import Path 

CSV_PATH = os.path.join('data')
ENCODING_CONFIDENCE = 0.7

getTableCols = lambda headers: ", ".join(headers)
getInsertValues = lambda headers:  ", ".join('%s' for i in range(len(headers)))

#NOTE: Some class that helps to solve enconding/delimiters stuff
class CSVReader():
  def __init__(self, filename: str) -> None:
    self.filename = filename
    self.file_path = os.path.join(CSV_PATH, filename)
    self.csv_rows = None
    self.csv_headers = None
    self.__read_file()

  def __read_file(self):
    if os.path.isfile(self.file_path):
      file_meta = self.__charset_check()
      delimiter = self.__find_delimiter(encoding=file_meta['encoding'])
      if file_meta['confidence'] >= ENCODING_CONFIDENCE:
        with open(self.file_path, 'r', encoding=file_meta['encoding']) as f:
          read = csv.DictReader(f, delimiter=delimiter)
          self.csv_rows = [self.__row_cleanup(row) for row in list(read)]
          for i, f in enumerate(read.fieldnames):
            read.fieldnames[i] = f.rstrip().lstrip()
          self.csv_headers = read.fieldnames
      else: 
        print(f'FATAL: Confidence for file {self.filename} was too low')
        sys.exit(1)

  def __row_cleanup(self, row):
    if 'NULL' in row.values():
      for k in row.keys():
        if row[k] == 'NULL': row[k] = None
    return row

  def __charset_check(self) -> dict:
    encoding, confidence = None, 0
    try:
      path = Path(self.file_path)
      blob = path.read_bytes()
      detection = chardet.detect(blob)
      encoding = detection['encoding']
      confidence = detection['confidence']
      print(f'INFO: Charset {encoding} was identified for file {self.filename} with a confidence of {confidence}')
    except:
      print(f'ERROR: Failed to identify encoding for file {self.filename}')
    return {'encoding': encoding, 'confidence': confidence}
  
  def get_as_tuple(self) -> dict:
    return {'headers': self.csv_headers, 'data': [tuple(row.values()) for row in self.csv_rows]}
  
  def __find_delimiter(self, default_sep: str=',', encoding: str='utf-8'):
    delimiter = None
    with open(self.file_path, 'r', encoding=encoding) as f:
      row = f.readline()
      delimiter = detect(row, default=default_sep)
    return delimiter

class MySQL():
  user = os.environ.get('MYSQL_USER', default='root') #NOTE: MySQL username
  passwd = os.environ.get('MYSQL_PASSWD', default='19989791') # MySQL password
  port = os.environ.get('MYSQL_PORT',default=3306) # MySQL port
  mysql_db = os.environ.get('MYSQL_DB', default='Cine')

  def __init__(self, my_db: str) -> None:
    try:
      self.db = db.connect(user=self.user, password=self.passwd, db=my_db, port=self.port)
      self.__is_connected()
    except db.errors.InterfaceError as e:
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
      rtv, cursor = False, self.db.cursor()
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

def main():
  #NOTE: Start DB Connection
  mySQL = MySQL('Cine')
  #NOTE: Pregunta 2
  csv_list = [f for f in os.listdir(CSV_PATH) if os.path.isfile(os.path.join(CSV_PATH, f))]
  for file in csv_list: 
    table_name = os.path.splitext(file)[0]
    read = CSVReader(file)
    data = read.get_as_tuple()
    sql_sent = f"INSERT INTO {table_name}({getTableCols(data['headers'])}) VALUES({getInsertValues(data['headers'])})"
    count, success = mySQL.insert_data(sql_sent, data['data'])
    if success: print(f"INFO: Data was successfully inserted into table {table_name}, {count} rows were added.")

if __name__ == "__main__":
  main()