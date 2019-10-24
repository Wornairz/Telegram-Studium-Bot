-- chat_id_list
CREATE TABLE IF NOT EXISTS `Utenti` (
  `chat_id` int(11) NOT NULL,
  `username` text NOT NULL,
  PRIMARY KEY(`chat_id`)
);

-- materie
CREATE TABLE IF NOT EXISTS `Materie` (
    `codice_corso` int NOT NULL,
    `nome` text NOT NULL,
    `anno_accademico` int NOT NULL,
    `anno` int NULL,
    `semestre` text NULL,
    `docente` text NULL,
    PRIMARY KEY(`codice_corso`, `anno_accademico`)
);

--iscrizioni
CREATE TABLE IF NOT EXISTS `Iscrizioni` (
    `id` int AUTO_INCREMENT,
    `chat_id` int(11) NOT NULL,
    'codice_corso' int NOT NULL,
    `anno_accademico` int NOT NULL,
    PRIMARY KEY(`id`, `chat_id`, `codice_corso`, `anno_accademico`),
    FOREIGN KEY(`chat_id`) REFERENCES Utenti(`chat_id`),
    FOREIGN KEY(`codice_corso`) REFERENCES Utenti(`codice_corso`),
    FOREIGN KEY(`anno_accademico`) REFERENCES Utenti(`anno_accademico`)
);

CREATE TABLE IF NOT EXISTS `Dipartimenti` (
  `id` varchar(5) NOT NULL,
  `nome` text NOT NULL,
  `anno_accademico` int NOT NULL
  PRIMARY KEY(`id`)
)

CREATE TABLE IF NOT EXISTS `CdS` (
  `id` int(11) NOT NULL,
  `nome` text,
  `id_dipartimento` varchar(5) DEFAULT NULL,
  `anno` int(11) NOT NULL,
  PRIMARY KEY(`id`, `anno`),
  FOREIGN KEY(`id_dipartimento`) REFERENCES Dipartimenti(`id`)
)
