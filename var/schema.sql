drop table if exists users;
  create table users (
  email text not null,
  password text not null
);

drop table if exists profiles;
  create table profiles (
  username text not null,
  location text not null,
  bio text not null,
  gender text not null,
  prof_img text
);

