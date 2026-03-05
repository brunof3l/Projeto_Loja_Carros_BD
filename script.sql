CREATE DATABASE IF NOT EXISTS loja_carros;
USE loja_carros;

CREATE TABLE marca (
    id_marca INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    logo_url VARCHAR(255) DEFAULT NULL,
    pais VARCHAR(80) DEFAULT NULL
) ENGINE=InnoDB; [cite: 12]

CREATE TABLE modelo (
    id_modelo INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    id_marca INT NOT NULL,
    tipo_carroceria VARCHAR(60) DEFAULT NULL,
    CONSTRAINT fk_modelo_marca FOREIGN KEY (id_marca) 
        REFERENCES marca(id_marca) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB; [cite: 7, 16]

CREATE TABLE combustivel (
    id_combustivel INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB; [cite: 19]

CREATE TABLE cambio (
    id_cambio INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB; [cite: 22]

CREATE TABLE cor (
    id_cor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    hex_code CHAR(7) DEFAULT NULL
) ENGINE=InnoDB; [cite: 25]

CREATE TABLE categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao VARCHAR(255) DEFAULT NULL
) ENGINE=InnoDB; [cite: 28]

CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    cpf_cnpj VARCHAR(20) UNIQUE DEFAULT NULL,
    foto_perfil VARCHAR(255) DEFAULT NULL,
    tipo ENUM('cliente', 'concessionaria', 'admin') NOT NULL DEFAULT 'cliente',
    ativo TINYINT(1) NOT NULL DEFAULT 1,
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB; [cite: 33]

CREATE TABLE veiculo (
    id_veiculo INT AUTO_INCREMENT PRIMARY KEY,
    id_modelo INT NOT NULL,
    ano_fabricacao YEAR NOT NULL,
    ano_modelo YEAR NOT NULL,
    km INT UNSIGNED NOT NULL DEFAULT 0,
    valor DECIMAL(12,2) NOT NULL,
    descricao TEXT DEFAULT NULL,
    portas TINYINT DEFAULT NULL,
    placa VARCHAR(10) UNIQUE DEFAULT NULL,
    renavam VARCHAR(20) UNIQUE DEFAULT NULL,
    id_combustivel INT NOT NULL,
    id_cambio INT NOT NULL,
    id_cor INT NOT NULL,
    id_categoria INT NOT NULL,
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_veiculo_modelo FOREIGN KEY (id_modelo) REFERENCES modelo(id_modelo) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_veiculo_combustivel FOREIGN KEY (id_combustivel) REFERENCES combustivel(id_combustivel) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_veiculo_cambio FOREIGN KEY (id_cambio) REFERENCES cambio(id_cambio) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_veiculo_cor FOREIGN KEY (id_cor) REFERENCES cor(id_cor) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_veiculo_categoria FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB; [cite: 7, 37]

CREATE TABLE imagem (
    id_imagem INT AUTO_INCREMENT PRIMARY KEY,
    id_veiculo INT NOT NULL,
    url VARCHAR(255) NOT NULL,
    CONSTRAINT fk_imagem_veiculo FOREIGN KEY (id_veiculo) 
        REFERENCES veiculo(id_veiculo) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB; [cite: 7, 41]

CREATE TABLE avaliacao (
    id_avaliacao INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_veiculo INT NOT NULL,
    nota TINYINT NOT NULL CHECK (nota BETWEEN 1 AND 5),
    comentario TEXT DEFAULT NULL,
    data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_usuario, id_veiculo),
    CONSTRAINT fk_avaliacao_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_avaliacao_veiculo FOREIGN KEY (id_veiculo) REFERENCES veiculo(id_veiculo) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB; [cite: 7, 44]

CREATE TABLE favoritos (
    id_usuario INT NOT NULL,
    id_veiculo INT NOT NULL,
    data_adicionado DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_usuario, id_veiculo),
    CONSTRAINT fk_favoritos_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_favoritos_veiculo FOREIGN KEY (id_veiculo) REFERENCES veiculo(id_veiculo) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB; [cite: 7, 49]

CREATE TABLE concessionaria (
    id_concessionaria INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    razao_social VARCHAR(200) NOT NULL,
    cnpj VARCHAR(20) NOT NULL UNIQUE,
    endereco VARCHAR(255) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    cep VARCHAR(50) NOT NULL,
    site VARCHAR(255) DEFAULT NULL,
    CONSTRAINT fk_concessionaria_usuario FOREIGN KEY (id_usuario) 
        REFERENCES usuario(id_usuario) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB; [cite: 7, 53]
