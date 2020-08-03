SELECT m.id AS movie_id,
       m.original_title,
       m.release_date,
       g.name AS genre
FROM   movie AS m
       INNER JOIN movie_genre AS mg
               ON mg.movie_id = m.id
       INNER JOIN genre AS g
               ON mg.genre_id = g.id
LIMIT 5;
