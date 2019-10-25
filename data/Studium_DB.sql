-- chat_id_list
CREATE TABLE IF NOT EXISTS `Utenti` (
  `chat_id` int NOT NULL,
  `username` text NULL,
  PRIMARY KEY(`chat_id`)
);

CREATE TABLE IF NOT EXISTS `Materie` (
    `codice_corso` int NOT NULL,
    `nome` text NOT NULL,
    `anno_accademico` int NULL,
    `anno` int NULL,
    `semestre` text NULL,
    `docente` text NULL,
    PRIMARY KEY(`codice_corso`)
);

CREATE TABLE IF NOT EXISTS `Iscrizioni` (
    `chat_id` int NOT NULL,
    `codice_corso` int NOT NULL,
    PRIMARY KEY(`chat_id`, `codice_corso`),
    FOREIGN KEY(`chat_id`) REFERENCES Utenti(`chat_id`),
    FOREIGN KEY(`codice_corso`) REFERENCES Materie(`codice_corso`)
);

CREATE TABLE IF NOT EXISTS `Dipartimenti` (
  `id` varchar(5) NOT NULL,
  `nome` text NOT NULL,
  `anno_accademico` int NOT NULL
  PRIMARY KEY(`id`, `anno_accademico`)
)

CREATE TABLE IF NOT EXISTS `CdS` (
  `id` int NOT NULL,
  `nome` text,
  `id_dipartimento` varchar(5) DEFAULT NULL,
  `anno_accademico` int NOT NULL,
  PRIMARY KEY(`id`, `anno_accademico`),
  FOREIGN KEY(`id_dipartimento`) REFERENCES Dipartimenti(`id`)
  FOREIGN KEY(`anno_accademico`) REFERENCES Dipartimenti(`anno_accademico`)
)

CREATE TABLE `Avvisi` (
  `id` int NOT NULL,
  `id_materia` int NOT NULL,
  `titolo` text,
  `contenuto` text,
  `docente` text,
  `data` text,
  `spammed` bit(1) DEFAULT NULL
  PRIMARY KEY(`id`, `id_materia`)
  FOREIGN KEY(`id_materia`) REFERENCES Materie(`id`)
)