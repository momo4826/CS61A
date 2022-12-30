CREATE TABLE parents AS
  SELECT "abraham" AS parent, "barack" AS child UNION
  SELECT "abraham"          , "clinton"         UNION
  SELECT "delano"           , "herbert"         UNION
  SELECT "fillmore"         , "abraham"         UNION
  SELECT "fillmore"         , "delano"          UNION
  SELECT "fillmore"         , "grover"          UNION
  SELECT "eisenhower"       , "fillmore";

CREATE TABLE dogs AS
  SELECT "abraham" AS name, "long" AS fur, 26 AS height UNION
  SELECT "barack"         , "short"      , 52           UNION
  SELECT "clinton"        , "long"       , 47           UNION
  SELECT "delano"         , "long"       , 46           UNION
  SELECT "eisenhower"     , "short"      , 35           UNION
  SELECT "fillmore"       , "curly"      , 32           UNION
  SELECT "grover"         , "short"      , 28           UNION
  SELECT "herbert"        , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT parents.child as name from dogs, parents
  where dogs.name == parents.parent
  order by dogs.height DESC;


-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT dogs.name as name, sizes.size as size from dogs, sizes
  where dogs.height > sizes.min and dogs.height <= sizes.max;


-- Filling out this helper table is optional

CREATE TABLE info AS
SELECT size_of_dogs.name as name, size_of_dogs.size as size, parents.parent as parent from (size_of_dogs inner join parents on size_of_dogs.name == parents.child); 

CREATE TABLE siblings AS
  SELECT  a.name as sibling_1, b.name as sibling_2, a.size as size
  from info as a, info as b
  where a.name < b.name
  and a.parent == b.parent
  and a.size == b.size;


-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT "The two siblings, " || sibling_1 || " plus " || sibling_2 || " have the same size: " || size
  from siblings;

