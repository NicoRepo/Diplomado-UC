from CargaBD import MySQL
from prettytable import PrettyTable
import pandas as pd

QUERIES = [
  """
    SELECT d.last_name, d.first_name, COUNT(movie_id) AS 'How Many' 
    FROM movies_directors as md
    JOIN directors AS d ON d.id = md.director_id
    GROUP by d.last_name, d.first_name HAVING COUNT(movie_id) > 3
    ORDER BY COUNT(MOVIE_ID) DESC;
  """,
  """
    SELECT a.last_name, a.first_name, COUNT(movie_id)
    FROM actors AS a
    JOIN movies_actors AS ma ON ma.actor_id = a.id
    GROUP BY a.last_name, a.first_name
    ORDER BY a.last_name, a.first_name;
  """,
  """
    SELECT m.name AS 'Movie', m.year AS 'Year', d.last_name AS 'Director', m.rank AS 'Ranking'
    FROM (movies_directors AS md JOIN movies AS m ON m.id = md.movie_id)
    JOIN directors AS d ON d.id = director_id WHERE m.rank > 8
    ORDER BY m.rank DESC;
  """
]

def main():
  mySQL = MySQL('Cine')
  #NOTE: Pregunta 3 - Items[1,2,3]
  for query in QUERIES:
    data = mySQL.fetch_data(query)
    pt = PrettyTable()
    pt.field_names = data[0].keys()
    pt.add_rows([list(row.values()) for row in data])
    print(pt)
if __name__ == "__main__":
  main()