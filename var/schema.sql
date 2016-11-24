drop table if exists users;
  create table users (
  email text not null,
  password text not null
);

drop table if exists profiles;
  create table profiles (
  prof_email text not null,
  username text not null,
  location text not null,
  bio text not null,
  gender text not null,
  prof_img text
);

drop table if exists premium;
  create table premium (
  prem_email text not null,
  password text not null,
  cc_num integer not null,
  sec_code integer not null
);


