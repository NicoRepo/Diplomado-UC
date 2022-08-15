from CargaBD import MySQL
from Queries import QUERIES
from prettytable import PrettyTable
import pandas as pd

def main():
  #NOTE: Pregunta 3 - Item 4
  mySQL = MySQL('Cine')
  data = mySQL.fetch_data(QUERIES[2])
  df1 = pd.DataFrame(data)
  print(df1[['Movie', 'Ranking']].loc[0:10])
  print(df1.iloc[20:50])

if __name__ == "__main__":
  main()