drop database if exists station;

create database station;

use station;

create table building (
    building_id int auto_increment,
    last_maintenance date,
    primary key (building_id)
);

create table employee (
    employee_id int auto_increment,
    name text,
    salary int,
    dob date,
    works_in_building int,
    primary key (employee_id),
    foreign key (works_in_building) references building (building_id)
        on delete set null on update cascade
);

create table passenger (
    passenger_id int auto_increment,
    sex enum ('F','M', 'O'),

    primary key (passenger_id)
);

create table train (
    train_number int,
    train_name text,
    train_type enum ('superfast', 'local', 'express'),
    num_coach int,
    last_maintenance date,

    primary key (train_number)
);

create table ticket (
    train_number int,
    ticket_number int auto_increment,
    berth enum ('L', 'U', 'M'),
    coach int,
    journey_date date,
    cost int,

    primary key (ticket_number),
    foreign key (train_number) references train(train_number)
        on delete restrict on update cascade
);

create table cleaning_staff (
    employee_id int,

    primary key (employee_id)
);

create table platform (
    platform_no int,
    len int,
    last_cleaning date,
    cleaning_staff_id int,
    primary key (platform_no),
    foreign key (cleaning_staff_id) references cleaning_staff(employee_id)
        on delete set null on update cascade
);

create table time_table (
    train_number int,
    platform_number int,
    arrival_time time,
    departure_time time,

    primary key (train_number, platform_number),
    foreign key (train_number) references train(train_number)
        on delete cascade on update cascade,
    foreign key (platform_number) references platform(platform_no)
        on delete cascade on update cascade
);

create table checked_by (
    employee_id int,
    ticket_number int,
    time_checked timestamp,

    primary key (employee_id, ticket_number),
    foreign key (employee_id) references ticket_checker(employee_id)
        on delete restrict on update cascade,
    foreign key (ticket_number) references ticket(ticket_number)
        on delete restrict on update cascade
);

create table assigned_buildings(
    staff_id int,
    building_id int,

    primary key (staff_id, building_id),
    foreign key (staff_id) references cleaning_staff(employee_id)
        on delete cascade on update cascade,
    foreign key (building_id) references building(building_id)
        on delete cascade on update cascade
);

create table usable_by (
    platform_id int,
    train_type enum('local', 'superfast', 'express'),

    primary key (platform_id, train_type),
    foreign key (platform_id) references platform(platform_no)
        on delete cascade on update cascade
);

create table manager (
    employee_id int primary key,

    foreign key (employee_id) references employee(employee_id)
    on delete cascade on update cascade
);

alter table employee
    add column manager_id int;

alter table employee 
    add constraint foreign key (manager_id) references manager (employee_id);

create table engineer (
    employee_id int primary key,

    foreign key (employee_id) references employee(employee_id)
    on delete cascade on update cascade
);

create table station_master (
    employee_id int primary key,

    foreign key (employee_id) references employee(employee_id)
    on delete cascade on update cascade
);

create table ticket_checker (
    employee_id int primary key,

    foreign key (employee_id) references employee(employee_id)
    on delete cascade on update cascade
);

create table food_store (
    building_id int primary key,

    foreign key (building_id) references building(building_id)
    on delete cascade on update cascade
);

create table enquiry (
    building_id int primary key,

    foreign key (building_id) references building(building_id)
    on delete cascade on update cascade
);

create table toilet (
    building_id int primary key,

    foreign key (building_id) references building(building_id)
     on delete cascade on update cascade   
);

create table ticket_counter (
    building_id int primary key,

    foreign key (building_id) references building(building_id)
    on delete cascade on update cascade
);

