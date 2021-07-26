create table "Permissions"
(
    "Id"          serial not null
        constraint pk_permission
            primary key,
    "Permission"  varchar(50),
    "Description" varchar(200)
);

alter table "Permissions"
    owner to postgres;

INSERT INTO public."Permissions" ("Id", "Permission", "Description") VALUES (1, 'SEND MESSAGE', 'SEND MESSAGES');
INSERT INTO public."Permissions" ("Id", "Permission", "Description") VALUES (2, 'ROOT', 'ALL PERMISSIONS');
INSERT INTO public."Permissions" ("Id", "Permission", "Description") VALUES (3, 'CREATE MENUS', 'CREATE MENU');
INSERT INTO public."Permissions" ("Id", "Permission", "Description") VALUES (4, 'READ MENUS', 'READ');
INSERT INTO public."Permissions" ("Id", "Permission", "Description") VALUES (5, 'UPDATE MENUS', 'UPDATE');
INSERT INTO public."Permissions" ("Id", "Permission", "Description") VALUES (6, 'DELETE MENUS', 'DELETE');
INSERT INTO public."Permissions" ("Id", "Permission", "Description") VALUES (7, 'CREATE ORDER', 'CREATE ORDER BY WHATSAPP');