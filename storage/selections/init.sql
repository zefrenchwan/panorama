create schema auth;

create table auth.users (
    user_id serial primary key, 
    name text not null unique, 
    email text not null unique,
    activity bool not null default true, 
    hashed_pwd text not null
);


create schema collections;


create table collections.sources (
    source_id serial primary key, 
    name text not null, 
    url text unique not null     
);

create table collections.requests (
    request_id serial not null,
    user_id int not null references auth.users(user_id),
    source_id int references collections.sources(source_id),
    reload_minutes int not null, 
    activity bool not null default true, 
    keywords text[] default null
);

create table connections.processors (
    processor_id serial primary key,
    request_id int references collections.requests(request_id), 
    endpoint string not null,
    last_run timestamp without time zone,
    last_status bool
);