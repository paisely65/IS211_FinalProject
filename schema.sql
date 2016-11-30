drop table if exists students;
create table students (
  id integer primary key autoincrement,
  first_name text not null,
  last_name text not null
);

drop table if exists quizzes;
create table quizzes (
  id integer primary key autoincrement,
  subject text not null,
  questions integer not null,
  date text not null
);

drop table if exists results;
create table results (
  s_id integer not null,
  q_id integer not null,
  score integer not null
);
