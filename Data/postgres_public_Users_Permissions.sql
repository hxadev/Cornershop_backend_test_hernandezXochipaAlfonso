create table "Users_Permissions"
(
    "IdUser"       smallint not null
        constraint fk_user_permission
            references "Users"
            on update cascade on delete cascade,
    "IdPermission" smallint not null
        constraint fk_permission_users
            references "Permissions"
            on update cascade on delete cascade,
    id             serial   not null
        constraint users_permissions_pk
            primary key
);

alter table "Users_Permissions"
    owner to postgres;

INSERT INTO public."Users_Permissions" ("IdUser", "IdPermission", id) VALUES (2, 1, 1);
INSERT INTO public."Users_Permissions" ("IdUser", "IdPermission", id) VALUES (2, 2, 2);
INSERT INTO public."Users_Permissions" ("IdUser", "IdPermission", id) VALUES (3, 4, 3);
INSERT INTO public."Users_Permissions" ("IdUser", "IdPermission", id) VALUES (4, 4, 4);
INSERT INTO public."Users_Permissions" ("IdUser", "IdPermission", id) VALUES (3, 7, 5);
INSERT INTO public."Users_Permissions" ("IdUser", "IdPermission", id) VALUES (4, 7, 6);
INSERT INTO public."Users_Permissions" ("IdUser", "IdPermission", id) VALUES (6, 7, 7);