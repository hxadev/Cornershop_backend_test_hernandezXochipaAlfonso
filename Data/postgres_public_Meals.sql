create table "Meals"
(
    "Id"          serial  not null
        constraint pk_menu_
            primary key,
    "Key"         varchar(100),
    "Description" text,
    "IdMenu"      integer not null
        constraint fk_meel_menu
            references "Menus",
    "Sort"        smallint
);

comment on column "Meals"."Key" is 'Key of menu : ex (M120121)';

comment on column "Meals"."IdMenu" is 'Relationship with the menu';

alter table "Meals"
    owner to postgres;

INSERT INTO public."Meals" ("Id", "Key", "Description", "IdMenu", "Sort") VALUES (66, 'Wings with rice ', '', 61, null);
INSERT INTO public."Meals" ("Id", "Key", "Description", "IdMenu", "Sort") VALUES (67, 'Tomatoe Soup ', '', 61, null);
INSERT INTO public."Meals" ("Id", "Key", "Description", "IdMenu", "Sort") VALUES (68, 'Porkchop', '', 61, null);
INSERT INTO public."Meals" ("Id", "Key", "Description", "IdMenu", "Sort") VALUES (69, 'Mexican Quesadilla', '', 61, null);