
create table if not exists posts (
  id integer primary key autoincrement,
  author text not null,
  heading text not null,
  content text not null,
  timestamp date not null
);
