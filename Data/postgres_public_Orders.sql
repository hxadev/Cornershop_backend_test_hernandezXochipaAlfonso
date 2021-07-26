create table "Orders"
(
    "Id"       serial  not null
        constraint pk_order
            primary key,
    "IdMeal"   integer not null
        constraint fk_order_meal
            references "Meals",
    "Comments" text,
    "Status"   char,
    "IdUser"   integer not null
        constraint fk_user_order
            references "Users",
    idmenu     integer
        constraint orders_fk
            references "Menus"
);

comment on column "Orders"."Id" is 'Order Identifier';

comment on column "Orders"."Status" is 'S=SAVED, O=ORDERED';

alter table "Orders"
    owner to postgres;

INSERT INTO public."Orders" ("Id", "IdMeal", "Comments", "Status", "IdUser", idmenu) VALUES (9, 66, 'i want more sauce', 'O', 3, 61);