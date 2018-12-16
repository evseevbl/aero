/*1	Выбрать все рейсы, которые идут из определенного города.*/

SELECT f.code
  FROM eflight f
  JOIN daeroports a
    ON f.loc_from = a.code
  WHERE a.city = 'Moscow' --Здесь можно указать любой город
;


/*2	Выбрать всех пассажиров, которые летят на определенном рейсе.*/

SELECT p.surname, p.name, p.passport_id
  FROM eflight f
  JOIN epassenger e
    ON f.code = e.flight
  JOIN dpassengers p
    ON e.passport_id = p.passport_id
;


/*3	Выбрать все города, в которые есть рейсы из Москвы.*/

SELECT r.city
  FROM eflight f
  JOIN daeroports a
    ON a.code = f.loc_from
  JOIN daeroports r
    ON r.code = f.loc_to
  WHERE a.city = 'Moscow'
;


/*4	Выбрать всех пассажиров данного рейса, которым < 18 лет*/

SELECT p.surname, p.name, p.passport_id
  FROM eflight f
  JOIN epassenger e
    ON f.code = e.flight
  JOIN dpassengers p
    ON e.passport_id = p.passport_id
  WHERE age(p.birthdate) < interval '18 years'
;


/*5	Выбрать терминалы, в которых будет регистрация на определенный рейс.*/

SELECT t.number
  FROM eflight f
  JOIN dterminals t
    ON f.terminalfrom = t.id
  WHERE f.code = 'S7 178'
;


/*6	Выбрать Компанию, которой принадлежит определенный рейс.*/

SELECT c.name
  FROM rcompany2flight r2f
  JOIN eflight f
    ON r2f.flight_code = f.code
  JOIN dcompnames c
    ON r2f.comp_code = c.iata_code
  WHERE f.code = 'S7 178'
;


/*7	Выбрать компанию, город отправления, город прибытия для определенного рейса.*/

SELECT c.name, d.city AS departure, a.city AS arrival
  FROM rcompany2flight r2f
  JOIN eflight f
    ON r2f.flight_code = f.code
  JOIN dcompnames c
    ON r2f.comp_code = c.iata_code
  JOIN daeroports d
    ON d.code = f.loc_from
  JOIN daeroports a
    ON a.code = f.loc_to
  WHERE f.code = 'S7 178'
;


/*8	Выбрать компанию, город отправления, город прибытия для всех рейсов*/

SELECT c.name, d.city AS departure, a.city AS arrival
  FROM rcompany2flight r2f
  RIGHT JOIN eflight f
    ON r2f.flight_code = f.code
  JOIN dcompnames c
    ON r2f.comp_code = c.iata_code
  JOIN daeroports d
    ON d.code = f.loc_from
  JOIN daeroports a
    ON a.code = f.loc_to
;


/*9	Выбрать всех пассажиров, которые полетят на рейсах определенной компании.*/

WITH f AS (
SELECT f.code
  FROM rcompany2flight r2f
  JOIN dcompnames c
    ON r2f.comp_code = c.iata_code
  JOIN eflight f
    ON r2f.flight_code = f.code
  WHERE c.iata_code = 'S7'
)

SELECT f.code, p.name, p.surname, p.passport_id
  FROM f
  JOIN epassenger ep
    ON ep.flight = f.code
  JOIN dpassengers p
    ON ep.passport_id = p.passport_id
;


/*10	Выбрать пассажиров, которые регистрируются в конкретном терминале.*/

SELECT p.name, p.surname, p.passport_id
  FROM epassenger ep
  JOIN e_regcounter reg
    ON reg.code = ep.counter_reg
  JOIN dpassengers p
    ON ep.passport_id = p.passport_id
  WHERE reg.in_what_terminal = 'A'
;


/*11	Выбрать рейсы, на которые регистрация в конкретном терминале.*/

SELECT f.code
  FROM eflight f
  JOIN dterminals t
    ON t.id = f.terminalfrom
  WHERE t.number = 'A'
;


/*12	Выбрать все рейсы, и для каждого из них количество пассажиров.*/

SELECT f.code, COUNT(ep.passport_id) AS passengers
  FROM eflight f
  LEFT JOIN epassenger ep
    ON f.code = ep.flight
  GROUP BY f.code
;


/*13	Выбрать все компании, и для каждой из них количество рейсов.*/

SELECT c.name, COUNT(f.code) AS flights
  FROM rcompany2flight r2f
  JOIN eflight f
    ON r2f.flight_code = f.code
  RIGHT JOIN dcompnames c
    ON c.iata_code = r2f.comp_code
  GROUP BY c.name
;


/*14	Выбрать все аэропорты, и для каждого из них количество исходящих рейсов и количество входящих рейсов.*/

SELECT ea.name, COUNT(fa.code) AS arrivals, COUNT(fd.code) AS departure
  FROM eaeroports ea
  LEFT JOIN eflight fa
    ON ea.code = fa.loc_to
  LEFT JOIN eflight fd
    ON ea.code = fd.loc_from
  GROUP BY ea.name
;


/*15	Выбрать все города, и для каждого из них количество аэропортов.*/

SELECT a.city, COUNT(a.code) AS aeroports
  FROM daeroports a
  GROUP BY a.city
;


/*16	Выбрать национальности пассажиров для определенного рейса, и для каждой национальности количество пассажиров.*/

SELECT ep.country, COUNT(ep.country) AS passengers
  FROM epassenger ep
    WHERE ep.flight = 'S7 178'
  GROUP BY ep.country
;


/*17	Выбрать все рейсы, которые сейчас в пути.*/

SELECT f.code
  FROM eflight f
    WHERE f.status = 'departed' --'departed' -это статус, он может быть другим
;


/*18	Выбрать рейсы и количество пассажиров, где количество пассажиров < 20.*/

SELECT f.code, COUNT(ep.passport_id) AS passengers
  FROM eflight f
  JOIN epassenger ep
    ON f.code = ep.flight
  GROUP BY f.code
  HAVING COUNT(ep.passport_id) < 20
;


/*19	Выбрать всех пассажиров из России.*/

SELECT DISTINCT p.name, p.surname, p.passport_id
  FROM epassenger ep
  LEFT JOIN dpassengers p
    ON ep.passport_id = p.passport_id
  WHERE ep.country = 'Russia'
;
