create table "Users"
(
    "Id"       serial       not null
        constraint pk_id
            primary key,
    "Fullname" varchar(200),
    "Username" varchar(50)  not null
        constraint unique_username
            unique,
    "Password" varchar(100) not null,
    "Phone"    varchar(15)  not null,
    "Email"    varchar(100) not null
        constraint unique_email
            unique
);

alter table "Users"
    owner to postgres;

create index ix_username
    on "Users" ("Username");

INSERT INTO public."Users" ("Id", "Fullname", "Username", "Password", "Phone", "Email") VALUES (2, 'Broker', 'broker', '1234', '4155238886', 'ana@mail.com');
INSERT INTO public."Users" ("Id", "Fullname", "Username", "Password", "Phone", "Email") VALUES (3, 'Alfonso Hernandez', 'alfon123', '1234', '+5212461847899', 'alfonso_h_x@hotmail.com');
INSERT INTO public."Users" ("Id", "Fullname", "Username", "Password", "Phone", "Email") VALUES (4, 'Alfonso Xochipa', 'ch1234', '1234', '+5212461878506', 'hxa.dev@hotmail.com');
INSERT INTO public."Users" ("Id", "Fullname", "Username", "Password", "Phone", "Email") VALUES (6, 'Claudia Saavedra', 'ch12345', '1234', '+522411233057', 'chedu@hotmail.com');