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

create table collections.selectors (
    selector_id serial primary key,
    user_id int not null references auth.users(user_id),
    source_id int references collections.sources(source_id),
    reload_minutes int not null, 
    activity bool not null default true, 
    keywords text[] default null
);

create table collections.processors (
    processor_id serial primary key,
    selector_id int references collections.selectors(selector_id), 
    processor text not null,
    activity bool default true
);

create table collections.tasks (
    processor_id int not null references collections.processors(processor_id),
    selector_id int not null references collections.selectors(selector_id),
    task_id text not null primary key,
    starting_time timestamp without time zone not null, 
    ending_time timestamp without time zone, 
    success bool 
);
 
create table collections.loads (
    task_id text not null references collections.tasks(task_id),
    load_id text primary key,
    destination text not null,
    starting_time timestamp without time zone not null, 
    ending_time timestamp without time zone, 
    success bool 
);
 