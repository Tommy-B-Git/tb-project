drop table if exists users;
create table users (
  id integer primary key autoincrement,
  email text unique not null,
  password text not null
);
