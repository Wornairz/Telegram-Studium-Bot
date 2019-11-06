CREATE TABLE IF NOT EXISTS `Iscrizioni` (
    `chat_id` int NOT NULL,
    `codice_corso` int NOT NULL,
    `username` varchar(32) NULL,
    PRIMARY KEY(`chat_id`, `codice_corso`)
)

