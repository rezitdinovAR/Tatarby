CREATE TABLE books
(
    book_id   integer,

    title_ru  varchar(100),
    title_tat varchar(100),

    desc_ru   varchar(1000),
    desk_tat  varchar(1000),

    url       varchar(100),
    cover_utl varchar(100),

    vector    double precision[],

    CONSTRAINT book_pk PRIMARY KEY (book_id)
);


CREATE TABLE users
(
    user_id integer,
    CONSTRAINT user_pk PRIMARY KEY (user_id)
);

CREATE TABLE users_books_liked
(
    user_id int8,
    book_id int8,
    UNIQUE (user_id, book_id),
    CONSTRAINT users_fk FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT book_fk FOREIGN KEY (book_id) REFERENCES books (book_id)
)