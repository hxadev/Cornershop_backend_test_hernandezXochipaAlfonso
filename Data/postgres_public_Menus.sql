create table "Menus"
(
    "Id"            serial not null
        constraint pk_menu
            primary key,
    "PublishedDate" timestamp,
    "CreatedByUser" smallint
        constraint fk_create_by_user
            references "Users",
    "CreatedAt"     timestamp
);

alter table "Menus"
    owner to postgres;

INSERT INTO public."Menus" ("Id", "PublishedDate", "CreatedByUser", "CreatedAt") VALUES (61, '2021-07-26 04:00:00.000000', null, null);