DROP DATABASE IF EXISTS airline;
CREATE DATABASE airline;

\connect airline

CREATE TABLE aircraft (
    id serial PRIMARY KEY,
    type text NOT NULL
);

CREATE TABLE crew_member (
    id serial PRIMARY KEY,
    name text NOT NULL,
    birth_date date NOT NULL
);

CREATE TABLE crew_member_aircraft (
  aircraft_id int REFERENCES aircraft (id) ON UPDATE CASCADE,
  crew_member_id int REFERENCES crew_member (id) ON UPDATE CASCADE,
  CONSTRAINT id PRIMARY KEY (aircraft_id, crew_member_id)
);

INSERT INTO aircraft(type) VALUES ('Boeing 747');
INSERT INTO aircraft(type) VALUES ('Boeing 767');
INSERT INTO aircraft(type) VALUES ('Boeing 777');
INSERT INTO aircraft(type) VALUES ('Airbus A300');
INSERT INTO aircraft(type) VALUES ('Airbus A380');

INSERT INTO crew_member(name, birth_date) VALUES ('John', '12-10-1985');
INSERT INTO crew_member(name, birth_date) VALUES ('Oliver', '11-01-1988');
INSERT INTO crew_member(name, birth_date) VALUES ('Jane', '05-05-1989');
INSERT INTO crew_member(name, birth_date) VALUES ('Michael', '27-03-1990');
INSERT INTO crew_member(name, birth_date) VALUES ('Donald', '20-12-1993');

INSERT INTO crew_member_aircraft (crew_member_id, aircraft_id) values (1, 1);
INSERT INTO crew_member_aircraft (crew_member_id, aircraft_id) values (1, 2);
INSERT INTO crew_member_aircraft (crew_member_id, aircraft_id) values (1, 3);
INSERT INTO crew_member_aircraft (crew_member_id, aircraft_id) values (1, 4);
INSERT INTO crew_member_aircraft (crew_member_id, aircraft_id) values (2, 1);
INSERT INTO crew_member_aircraft (crew_member_id, aircraft_id) values (3, 4);
INSERT INTO crew_member_aircraft (crew_member_id, aircraft_id) values (3, 5);
INSERT INTO crew_member_aircraft (crew_member_id, aircraft_id) values (4, 2);
INSERT INTO crew_member_aircraft (crew_member_id, aircraft_id) values (4, 3);
INSERT INTO crew_member_aircraft (crew_member_id, aircraft_id) values (4, 4);

-- select oldest crew member
SELECT name FROM crew_member ORDER BY birth_date LIMIT 1;

-- select 3rd (or n-th where offset determines n with 0 being first) oldest crew member
SELECT name FROM crew_member ORDER BY birth_date LIMIT 1 OFFSET 2;

-- select name of the most experienced crew member
SELECT name FROM (SELECT name, count(crew_member_aircraft.crew_member_id) as experience FROM crew_member JOIN crew_member_aircraft
  ON id=crew_member_aircraft.crew_member_id  GROUP BY name ORDER BY experience DESC LIMIT 1) as most_experienced;

-- select name of the least experienced crew member
SELECT name FROM (SELECT name, COUNT(crew_member_aircraft.crew_member_id) as exp_count FROM crew_member
  LEFT JOIN crew_member_aircraft ON id=crew_member_aircraft.crew_member_id  GROUP BY name ORDER BY exp_count LIMIT 1)
  as least_experienced;
