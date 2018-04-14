CREATE TABLE IF NOT EXISTS Users (
 user_id integer PRIMARY KEY,
 username text NOT NULL,
 api_token text
)