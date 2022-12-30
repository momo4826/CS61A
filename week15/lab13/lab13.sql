.read data.sql


CREATE TABLE bluedog AS
  SELECT color, pet from students 
  where color == "blue" and pet == "dog";

CREATE TABLE bluedog_songs AS
  SELECT color, pet, song from students
  where color == "blue" and pet == "dog";


CREATE TABLE smallest_int_having AS
  SELECT time, smallest from students
  where smallest >= 0
  group by smallest having count(smallest) == 1;


CREATE TABLE matchmaker AS
  SELECT a.pet as pet, a.song as song, a.color as first_person_coloc, b.color as second_person_color
  from students as a, students as b 
  where a.time < b.time
  and a.pet == b.pet
  and a.song == b.song;


CREATE TABLE sevens AS
  SELECT a.seven as seven
  from students as a, numbers as b 
  where a.time == b.time
  and a.number == 7
  and b.'7' == 'True';


CREATE TABLE average_prices AS
  SELECT category, avg(MSRP) as average_price
  from products
  group by category;


CREATE TABLE lowest_prices AS
  SELECT b.store as store, a.name as product, min(b.price) as price
  from products as a, inventory as b
  where a.name == b.item 
  group by a.name;


CREATE TABLE shopping_list AS
  SELECT b.product as product, b.store as store
  from products as a, lowest_prices as b
  where a.name == b.product
  group by a.category having a.MSRP/a.rating == min(a.MSRP/a.rating);


CREATE TABLE total_bandwidth AS
  SELECT sum(Mbs) as bandwith 
  from shopping_list as a, stores as b 
  where a.store == b.store;

