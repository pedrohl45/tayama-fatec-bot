-- ====================================================
-- TayamaBot — Script SQL para criação das tabelas
-- Execute este script no seu banco MySQL antes de ligar o bot
-- ====================================================

-- Tabela de perfil dos alunos
CREATE TABLE IF NOT EXISTS alunos (
    discord_id    VARCHAR(30) PRIMARY KEY,
    nome          VARCHAR(150) NOT NULL,
    curso         VARCHAR(100) DEFAULT 'Desenvolvimento de Software Multiplataforma (DSM)',
    semestre      INT DEFAULT 1,
    turno         VARCHAR(20) DEFAULT 'Manhã',
    instituicao   VARCHAR(150) DEFAULT 'FATEC São José dos Campos',
    status_matricula VARCHAR(30) DEFAULT 'Matriculado',
    horas_cumpridas INT DEFAULT 0,
    horas_exigidas  INT DEFAULT 120,
    progresso_curso FLOAT DEFAULT 0.0,
    criado_em     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de notas e faltas por disciplina (vinculada ao aluno)
CREATE TABLE IF NOT EXISTS notas_faltas (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    discord_id          VARCHAR(30) NOT NULL,
    codigo_disciplina   VARCHAR(20) NOT NULL,
    p1                  FLOAT DEFAULT NULL,
    p2                  FLOAT DEFAULT NULL,
    projeto             FLOAT DEFAULT NULL,
    exame_final         FLOAT DEFAULT NULL,
    faltas              INT DEFAULT 0,
    FOREIGN KEY (discord_id) REFERENCES alunos(discord_id) ON DELETE CASCADE,
    UNIQUE KEY uk_aluno_disciplina (discord_id, codigo_disciplina)
);

-- Tabela de sessões de estudo (estudos_foco)
CREATE TABLE IF NOT EXISTS sessoes_estudo (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    discord_id      VARCHAR(30) NOT NULL,
    disciplina      VARCHAR(100) NOT NULL,
    minutos         INT DEFAULT 0,
    anotacao        TEXT,
    registrado_em   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (discord_id) REFERENCES alunos(discord_id) ON DELETE CASCADE
);
