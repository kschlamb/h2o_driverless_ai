-- Run command: db2 -tvf call_function.sh

CONNECT TO TESTDB;

-- These statements will return NULL.
VALUES (NULL, 2.3, 3.0, 1.0, SCORE_WITH_REST_API(NULL, 2.3, 3.0, 1.0));
VALUES (4.8, NULL, 3.0, 1.0, SCORE_WITH_REST_API(4.8, NULL, 3.0, 1.0));
VALUES (4.8, 2.3, NULL, 1.0, SCORE_WITH_REST_API(4.8, 2.3, NULL, 1.0));
VALUES (4.8, 2.3, 3.0, NULL, SCORE_WITH_REST_API(4.8, 2.3, 3.0, NULL));

-- These statements will return a valid prediction/score result
-- (the iris species name).
VALUES (4.8, 2.3, 3.0, 1.0, SCORE_WITH_REST_API(4.8, 2.3, 3.0, 1.0));
VALUES (5.2, 2.7, 1.7, 1.0, SCORE_WITH_REST_API(5.2, 2.7, 1.7, 1.0));
VALUES (6.4, 3.0, 5.8, 2.3, SCORE_WITH_REST_API(6.4, 3.0, 5.8, 2.3));
VALUES (5.7, 2.8, 4.2, 1.2, SCORE_WITH_REST_API(5.7, 2.8, 4.2, 1.2));
VALUES (5.1, 2.5, 3.0, 1.2, SCORE_WITH_REST_API(5.1, 2.5, 3.0, 1.2));
VALUES (6.3, 2.8, 5.6, 1.7, SCORE_WITH_REST_API(6.3, 2.8, 5.6, 1.7));
VALUES (7.5, 3.0, 6.6, 2.0, SCORE_WITH_REST_API(7.5, 3.0, 6.6, 2.0));
VALUES (5.2, 2.0, 1.5, 0.3, SCORE_WITH_REST_API(5.2, 2.0, 1.5, 0.3));
VALUES (7.2, 3.0, 5.9, 2.0, SCORE_WITH_REST_API(7.2, 3.0, 5.9, 2.0));
VALUES (5.0, 2.8, 1.0, 0.2, SCORE_WITH_REST_API(5.0, 2.8, 1.0, 0.2));

CONNECT RESET;
