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

insert into collections.sources(name, url) values ('Duck duck go', 'https://duckduckgo.com/');


create table collections.selectors (
    selector_id serial primary key,
    user_id int not null references auth.users(user_id),
    source_id int references collections.sources(source_id),
    reload_interval text not null, 
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
    task_id text not null primary key,
    starting_time timestamp with time zone not null, 
    ending_time timestamp with time zone, 
    failures text[],
    -- independant value because some page failures may be fine (no need to say that one load failure implies global failure)
    success bool 
);
 
create table collections.loads (
    task_id text not null references collections.tasks(task_id),
    load_id text primary key,
    destination text not null,
    starting_time timestamp with time zone not null, 
    ending_time timestamp with time zone,
    failures text[], 
    success bool 
);
 

create or replace view collections.dynamic_next_launch(processor, url, keywords) 
as 
with first_tasks_to_run as (
    select  PROC.processor_id 
    from collections.processors PROC
    where PROC.activity 
    and not exists (
        select 1 
        from collections.tasks TASK 
        where TASK.processor_id = PROC.processor_id
        and TASK.starting_time is not null 
    )
), last_tasks as (
    select  TASK.* 
    from collections.tasks TASK
    where TASK.starting_time is not null 
    and not exists (
        select 1 
        from collections.tasks RERUN 
        where TASK.processor_id = RERUN.processor_id
        and RERUN.starting_time > TASK.starting_time
    )
), failed_tasks_to_run as (
    select  TASK.processor_id 
    from last_tasks TASK
    where TASK.ending_time is not null 
    and not TASK.success 
), next_tasks_to_run as (
    select  TASK.processor_id 
    from last_tasks TASK
    join collections.processors PROC on PROC.processor_id = TASK.processor_id
    join collections.selectors SEL on SEL.selector_id = PROC.selector_id 
    where TASK.ending_time is not null 
    and TASK.success
    and now() >= TASK.ending_time + SEL.reload_interval::interval
), all_launches as (
    select FITR.processor_id
    from first_tasks_to_run FITR
    UNION
    select FATR.processor_id
    from failed_tasks_to_run FATR 
    UNION 
    select NTR.processor_id
    from next_tasks_to_run NTR
), all_selectors_to_run as (
    select 
    PRO.processor, -- to contact the right processor by name
    SOURCES.url, -- to connect to the sources starting point 
    SELECTORS.keywords -- to find keywords to look for 
    from all_launches ALAU 
    join collections.processors PRO on PRO.processor_id = ALAU.processor_id
    join  collections.selectors SELECTORS on PRO.selector_id = SELECTORS.selector_id 
    left outer join collections.SOURCES on SOURCES.source_id = SELECTORS.source_id
    where SELECTORS.activity
    and PRO.activity
)
select distinct *
from all_selectors_to_run;



create procedure collections.upsert_task(
    p_task_id text, 
    p_processor_name text, 
    p_starting_date timestamp with time zone , 
    p_ending_date timestamp with time zone , 
    p_success bool, 
    p_errors text[]
) language plpgsql as $$
declare
    l_processor_id int;
begin

    select P.processor_id into l_processor_id  from processor P where P.activity and P.processor = p_processor_name;
    if l_processor_id is null then 
        raise exception 'no active processor named %', p_processor_name;
    end if;

    insert into collections.tasks(processor_id,task_id,starting_time,ending_time,failures,success)
    values (l_processor_id, p_task_id, p_starting_date, p_ending_date, p_errors, p_success)
    on conflict (task_id) do update 
    set starting_time = p_starting_date, ending_time = p_ending_date, failures = p_errors, success = p_success;
end; $$