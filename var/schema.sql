DROP TABLE if EXISTS users;
CREATE TABLE users (
email text UNIQUE,
password text
);
