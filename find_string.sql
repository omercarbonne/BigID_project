select articleID, POSITION('search_string' IN body) AS position
from Articles
where body LIKE '%search_string%';