drop table if exists users;
  create table users (
  username text not null,
  email text not null,
  password text not null
);

drop table if exists profiles;
  create table profiles (
  email text not null,
  username text not null,
  location text not null,
  bio text not null,
  gender text not null,
  prof_img text
);

drop table if exists premium;
  create table premium (
  username text not null,
  email text not null,
  password text not null,
  cc_num integer not null,
  sec_code integer not null
);


