-- Create table with training data.

drop table iris;

create table iris (sepal_length dec(2,1),
                   sepal_width  dec(2,1),
                   petal_length dec(2,1),
                   petal_width  dec(2,1),
                   class_name   char(10));

import from iris_species_with_header.csv of del skipcount 1 insert into iris;

select count(*) from iris;
select * from iris fetch first 5 rows only;
