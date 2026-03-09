"""
Banco de dados SQLite para a aplicação de venda de carros usados.
Este módulo é responsável por criar a estrutura do banco de dados, incluindo as tabelas e suas

Resolvemos criar e usar o sqlite somente para testes mais praticos, a estrutura principal foi pensada em MySQL, pois é mais 
segura e robusta para um ambiente de produção, além de oferecer melhor suporte a concorrência e escalabilidade. O SQLite é 
uma ótima opção para desenvolvimento local e testes, mas para um sistema em produção, o MySQL é a escolha mais adequada.
""" 

import sqlite3
import os

# Caminho do arquivo do banco de dados
# os.path.dirname(__file__) pega a pasta onde este arquivo está
DB_PATH = os.path.join(os.path.dirname(__file__), 'LojaCarros.db')


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS marca (
            id_marca INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            logo_url TEXT,
            pais TEXT
        );

        CREATE TABLE IF NOT EXISTS modelo (
            id_modelo INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            id_marca INTEGER NOT NULL,
            tipo_carroceria TEXT,
            FOREIGN KEY (id_marca)
                REFERENCES marca(id_marca)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        );

        CREATE TABLE IF NOT EXISTS combustivel (
            id_combustivel INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS cambio (
            id_cambio INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS cor (
            id_cor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            hex_code TEXT
        );

        CREATE TABLE IF NOT EXISTS categoria (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT
        );

        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            telefone TEXT NOT NULL,
            cpf_cnpj TEXT UNIQUE,
            foto_perfil TEXT,
            tipo TEXT NOT NULL DEFAULT 'cliente'
                CHECK (tipo IN ('cliente','concessionaria','admin')),
            ativo INTEGER NOT NULL DEFAULT 1,
            data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS veiculo (
            id_veiculo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_modelo INTEGER NOT NULL,
            ano_fabricacao INTEGER NOT NULL,
            ano_modelo INTEGER NOT NULL,
            km INTEGER NOT NULL DEFAULT 0,
            valor REAL NOT NULL,
            descricao TEXT,
            portas INTEGER,
            placa TEXT UNIQUE,
            renavam TEXT UNIQUE,
            id_combustivel INTEGER NOT NULL,
            id_cambio INTEGER NOT NULL,
            id_cor INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL,
            data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_modelo) REFERENCES modelo(id_modelo) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (id_combustivel) REFERENCES combustivel(id_combustivel) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (id_cambio) REFERENCES cambio(id_cambio) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (id_cor) REFERENCES cor(id_cor) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria) ON DELETE RESTRICT ON UPDATE CASCADE
        );

        CREATE TABLE IF NOT EXISTS imagem (
            id_imagem INTEGER PRIMARY KEY AUTOINCREMENT,
            id_veiculo INTEGER NOT NULL,
            url TEXT NOT NULL,
            FOREIGN KEY (id_veiculo)
                REFERENCES veiculo(id_veiculo)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );

        CREATE TABLE IF NOT EXISTS avaliacao (
            id_avaliacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_veiculo INTEGER NOT NULL,
            nota INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 5),
            comentario TEXT,
            data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(id_usuario, id_veiculo),

            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (id_veiculo) REFERENCES veiculo(id_veiculo) ON DELETE CASCADE ON UPDATE CASCADE
        );

        CREATE TABLE IF NOT EXISTS favoritos (
            id_usuario INTEGER NOT NULL,
            id_veiculo INTEGER NOT NULL,
            data_adicionado DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

            PRIMARY KEY (id_usuario, id_veiculo),

            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (id_veiculo) REFERENCES veiculo(id_veiculo) ON DELETE CASCADE ON UPDATE CASCADE
        );

        CREATE TABLE IF NOT EXISTS concessionaria (
            id_concessionaria INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL UNIQUE,
            razao_social TEXT NOT NULL,
            cnpj TEXT NOT NULL UNIQUE,
            endereco TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL,
            cep TEXT NOT NULL,
            site TEXT,

            FOREIGN KEY (id_usuario)
                REFERENCES usuario(id_usuario)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    """)

    conn.commit()
    conn.close()
    
def dados_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    # MARCAS
    marcas = [
        ("Toyota",),
        ("Honda",),
        ("Ford",),
        ("Chevrolet",),
        ("Volkswagen",),
        ("BMW",),
        ("Mercedes-Benz",),
        ("Audi",),
        ("Hyundai",),
        ("Kia",)
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO marca (nome) VALUES (?)",
        marcas
    )

    # COMBUSTIVEL
    combustiveis = [
        ("Gasolina",),
        ("Etanol",),
        ("Flex",),
        ("Diesel",),
        ("Elétrico",),
        ("Híbrido",)
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO combustivel (nome) VALUES (?)",
        combustiveis
    )

    # CAMBIO
    cambios = [
        ("Manual",),
        ("Automático",),
        ("CVT",),
        ("Automatizado",)
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO cambio (nome) VALUES (?)",
        cambios
    )

    # CORES
    cores = [
        ("Preto", "#000000"),
        ("Branco", "#FFFFFF"),
        ("Prata", "#C0C0C0"),
        ("Cinza", "#808080"),
        ("Vermelho", "#FF0000"),
        ("Azul", "#0000FF")
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO cor (nome, hex_code) VALUES (?, ?)",
        cores
    )

    # CATEGORIAS
    categorias = [
        ("Hatch", "Carros compactos urbanos"),
        ("Sedan", "Carros com porta-malas separado"),
        ("SUV", "Veículos utilitários esportivos"),
        ("Pickup", "Veículos com caçamba"),
        ("Esportivo", "Carros de alta performance")
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO categoria (nome, descricao) VALUES (?, ?)",
        categorias
    )

    # MODELOS
    modelos = [
        ("Corolla", 1, "Sedan"),
        ("Hilux", 1, "Pickup"),
        ("Civic", 2, "Sedan"),
        ("HR-V", 2, "SUV"),
        ("Ranger", 3, "Pickup"),
        ("Mustang", 3, "Esportivo"),
        ("Onix", 4, "Hatch"),
        ("Cruze", 4, "Sedan"),
        ("Golf", 5, "Hatch"),
        ("Jetta", 5, "Sedan")
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO modelo (nome, id_marca, tipo_carroceria) VALUES (?, ?, ?)",
        modelos
    )

    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    init_db()
    dados_db()
    print("Banco de dados inicializado com sucesso!")