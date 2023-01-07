DROP TABLE IF EXISTS texts;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS dialogs;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE dialogs (
    dialog_id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE texts (
    text_id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    language TEXT NOT NULL,
    customer_id INTEGER NOT NULL,
    dialog_id INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    FOREIGN KEY (dialog_id) REFERENCES dialogs (dialog_id)
);

