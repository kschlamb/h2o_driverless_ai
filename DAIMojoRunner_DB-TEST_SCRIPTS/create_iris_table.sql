-- Create table to use for scoring. This is likely using
-- the same data as what was used to train the model, but
-- that's okay... it's more about just having something
-- to test with.

drop table iris;

create table iris (row_id int not null generated always as identity,
                   sepal_length dec(2,1),
                   sepal_width  dec(2,1),
                   petal_length dec(2,1),
                   petal_width  dec(2,1),
                   species      char(10));

import from iris_species_with_header.csv of del skipcount 1
  insert into iris (sepal_length, sepal_width,
                    petal_length, petal_width, species);

select count(*) from iris;
select * from iris fetch first 5 rows only;

DROP TABLE IRIS_RESULTS;
CREATE TABLE IRIS_RESULTS (ROW_ID INT, "SPECIES.0" FLOAT, "SPECIES.1" FLOAT);
SELECT * FROM IRIS_RESULTS;
