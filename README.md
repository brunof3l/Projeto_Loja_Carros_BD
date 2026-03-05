# 🚗 Loja de Carros — Dicionário de Dados

Documentação do modelo de banco de dados do portal de **compra, venda e comparação de veículos**, projetado para **MySQL** com suporte a integridade referencial, transações ACID e índices eficientes para filtros complexos.

---

## 📑 Índice

- [Visão Geral](#visão-geral)
- [Diagrama de Entidades e Relacionamentos](#diagrama-de-entidades-e-relacionamentos)
- [Dicionário de Dados](#dicionário-de-dados)
  - [Tabelas de Domínio (Auxiliares)](#tabelas-de-domínio-auxiliares)
  - [Tabelas Principais](#tabelas-principais)
  - [Tabelas Associativas](#tabelas-associativas)
  - [Tabela de Concessionária](#tabela-de-concessionária)
- [Código dbdiagram.io](#código-dbdiagramio)

---

## Visão Geral

Este banco de dados sustenta um portal completo de veículos com as seguintes funcionalidades:

- Cadastro e listagem de veículos com filtros por marca, modelo, combustível, câmbio, cor e categoria
- Gerenciamento de usuários (clientes, concessionárias e administradores)
- Sistema de favoritos (lista de desejos)
- Avaliações de veículos por usuários
- Perfil estendido para concessionárias
- Galeria de imagens por veículo

---

## Diagrama de Entidades e Relacionamentos

| Tabela A | Cardinalidade | Tabela B | Via / Chave | Política FK |
|---|---|---|---|---|
| `marca` | 1 : N | `modelo` | `modelo.id_marca` | RESTRICT / CASCADE |
| `modelo` | 1 : N | `veiculo` | `veiculo.id_modelo` | RESTRICT / CASCADE |
| `combustivel` | 1 : N | `veiculos` | `veiculos.id_combustivel` | RESTRICT / CASCADE |
| `cambio` | 1 : N | `veiculos` | `veiculos.id_cambio` | RESTRICT / CASCADE |
| `cor` | 1 : N | `veiculos` | `veiculos.id_cor` | RESTRICT / CASCADE |
| `categoria` | 1 : N | `veiculos` | `veiculos.id_categoria` | RESTRICT / CASCADE |
| `veiculos` | 1 : N | `imagem` | `imagem.id_veiculo` | CASCADE / CASCADE |
| `usuario` | N : N | `veiculo` | `favoritos(id_usuario, id_veiculos)` | CASCADE / CASCADE |
| `usuario` | 1 : N | `veiculo` | `avaliacao.id_usuario` | CASCADE / CASCADE |
| `comparacao` | N : N | `veiculo` | `comparacao_item` | CASCADE / CASCADE |
| `usuario` | 1 : 1 | `concessionaria` | `concessionaria.id_usuario` | CASCADE / CASCADE |
| `veiculos` | 1 : N | `avaliacao` | `avaliacao.id_veiculo` | CASCADE / CASCADE |

---

## Dicionário de Dados

### Tabelas de Domínio (Auxiliares)

#### `marca`
> Cadastro de fabricantes de veículos (ex.: Toyota, Ford, Volkswagen). Serve como raiz da hierarquia **Marca → Modelo → Veículo**.

| Campo | Tipo / Tam. | Obrig. | Chave | Default | Constraint | Descrição |
|---|---|---|---|---|---|---|
| `id_marca` | INT | Sim | PK / AI | AUTO_INCREMENT | NOT NULL | Identificador único da marca |
| `nome` | VARCHAR(100) | Sim | UNIQUE | — | NOT NULL, UNIQUE | Nome da fabricante (sem duplicatas) |
| `logo_url` | VARCHAR(255) | Não | — | NULL | — | URL do logotipo da marca |
| `pais` | VARCHAR(80) | Não | — | NULL | — | País de origem da fabricante |

---

#### `modelo`
> Modelos de veículos vinculados a uma marca (ex.: Corolla, Civic, Gol). Um modelo pode ter múltiplos veículos cadastrados com variações de ano, cor e opcionais.

| Campo | Tipo / Tam. | Obrig. | Chave | Default | Constraint | Descrição |
|---|---|---|---|---|---|---|
| `id_modelo` | INT | Sim | PK / AI | AUTO_INCREMENT | NOT NULL | Identificador único do modelo |
| `nome` | VARCHAR(150) | Sim | — | — | NOT NULL | Nome do modelo |
| `id_marca` | INT | Sim | FK | — | NOT NULL | Referência para `marca.id_marca` |
| `tipo_carroceria` | VARCHAR(60) | Não | — | NULL | — | Ex.: Sedan, Hatch, SUV, Picape |

---

#### `combustivel`
> Tipos de combustível disponíveis. Deve ser pré-populada com: **Gasolina, Etanol, Flex, Diesel, Elétrico, Híbrido**.

| Campo | Tipo / Tam. | Obrig. | Chave | Default | Constraint | Descrição |
|---|---|---|---|---|---|---|
| `id_combustivel` | INT | Sim | PK / AI | AUTO_INCREMENT | NOT NULL | Identificador único |
| `nome` | VARCHAR(50) | Sim | UNIQUE | — | NOT NULL, UNIQUE | Nome do combustível |

---

#### `cambio`
> Tipos de câmbio disponíveis. Deve ser pré-populada com: **Manual, Automático, CVT, Automatizado**.

| Campo | Tipo / Tam. | Obrig. | Chave | Default | Constraint | Descrição |
|---|---|---|---|---|---|---|
| `id_cambio` | INT | Sim | PK / AI | AUTO_INCREMENT | NOT NULL | Identificador único |
| `nome` | VARCHAR(50) | Sim | UNIQUE | — | NOT NULL, UNIQUE | Descrição do câmbio |

---

#### `cor`
> Cores disponíveis para cadastro de veículos.

| Campo | Tipo / Tam. | Obrig. | Chave | Default | Constraint | Descrição |
|---|---|---|---|---|---|---|
| `id_cor` | INT | Sim | PK / AI | AUTO_INCREMENT | NOT NULL | Identificador único |
| `nome` | VARCHAR(50) | Sim | UNIQUE | — | NOT NULL, UNIQUE | Nome da cor (ex.: Branco Polar) |
| `hex_code` | CHAR(7) | Não | — | NULL | — | Código hexadecimal para UI (`#FFFFFF`) |

---

#### `categoria`
> Classificação dos veículos por segmento (ex.: Compacto, SUV, Esportivo, Utilitário). Usado em filtros de busca.

| Campo | Tipo / Tam. | Obrig. | Chave | Default | Constraint | Descrição |
|---|---|---|---|---|---|---|
| `id_categoria` | INT | Sim | PK / AI | AUTO_INCREMENT | NOT NULL | Identificador único |
| `nome` | VARCHAR(100) | Sim | UNIQUE | — | NOT NULL, UNIQUE | Rótulo da categoria |
| `descricao` | VARCHAR(255) | Não | — | NULL | — | Descrição auxiliar |

---

### Tabelas Principais

#### `usuario`
> Armazena todos os usuários do sistema. Um usuário pode ser cliente, representante de concessionária ou administrador. O campo `tipo` controla permissões e exibição de funcionalidades.

| Campo | Tipo / Tam. | Obrig. | Chave | Default | Constraint | Descrição |
|---|---|---|---|---|---|---|
| `id_usuario` | INT | Sim | PK / AI | AUTO_INCREMENT | NOT NULL | Identificador único do usuário |
| `nome` | VARCHAR(150) | Sim | — | — | NOT NULL | Nome completo |
| `email` | VARCHAR(150) | Sim | UNIQUE | — | NOT NULL, UNIQUE | E-mail para autenticação |
| `senha` | VARCHAR(255) | Sim | — | — | NOT NULL | Hash seguro (bcrypt/Argon2) |
| `telefone` | VARCHAR(20) | Não | — | — | NOT NULL | Telefone de contato |
| `cpf_cnpj` | VARCHAR(20) | Não | UNIQUE | NULL | NOT NULL, UNIQUE | CPF (pessoa física) ou CNPJ (concessionária) |
| `foto_perfil` | VARCHAR(255) | Não | — | NULL | — | URL da foto de perfil |
| `tipo` | ENUM | Sim | — | `'cliente'` | NOT NULL | Perfil: `cliente` \| `concessionaria` \| `admin` |
| `ativo` | TINYINT(1) | Sim | — | `1` | NOT NULL, DEFAULT 1 | Soft delete: `1`=ativo, `0`=inativo |
| `data_cadastro` | DATETIME | Sim | — | CURRENT_TIMESTAMP | NOT NULL | Data e hora do primeiro cadastro |
| `data_atualizacao` | DATETIME | Não | — | ON UPDATE NOW() | ON UPDATE CURRENT_TIMESTAMP | Última atualização do registro |

---

#### `veiculo`
> Entidade central do sistema. Representa um veículo específico com todas as suas características técnicas. Cada veículo pertence a um modelo e pode ter múltiplos anúncios, imagens e avaliações.

| Campo | Tipo / Tam. | Obrig. | Chave | Default | Constraint | Descrição |
|---|---|---|---|---|---|---|
| `id_veiculo` | INT | Sim | PK / AI | AUTO_INCREMENT | NOT NULL | Identificador único do veículo |
| `id_modelo` | INT | Sim | FK | — | NOT NULL | Referência para `modelo.id_modelo` |
| `ano_fabricacao` | YEAR | Sim | — | — | NOT NULL | Ano de fabricação |
| `ano_modelo` | YEAR | Sim | — | — | NOT NULL | Ano do modelo (pode diferir do fab.) |
| `km` | INT UNSIGNED | Sim | — | `0` | NOT NULL | Quilometragem rodada |
| `valor` | DECIMAL(12,2) | Sim | — | — | NOT NULL | Preço de venda em R$ |
| `descricao` | TEXT | Não | — | NULL | — | Observações e opcionais |
| `portas` | TINYINT | Não | — | NULL | — | Número de portas |
| `placa` | VARCHAR(10) | Não | UNIQUE | NULL | UNIQUE | Placa (mascarada / criptografada) |
| `renavam` | VARCHAR(20) | Não | UNIQUE | NULL | UNIQUE | RENAVAM do veículo |
| `id_combustivel` | INT | Sim | FK | — | NOT NULL | Referência para `combustivel` |
| `id_cambio` | INT | Sim | FK | — | NOT NULL | Referência para `cambio` |
| `id_cor` | INT | Sim | FK | — | NOT NULL | Referência para `cor` |
| `id_categoria` | INT | Sim | FK | — | NOT NULL | Referência para `categoria` |
| `data_cadastro` | DATETIME | Sim | — | CURRENT_TIMESTAMP | NOT NULL | Data de cadastro no sistema |

---

#### `imagem`
> Armazena as imagens associadas a cada veículo. Um veículo pode ter múltiplas fotos. O campo `principal` indica qual foto será exibida nos cards de listagem.

| Campo | Tipo / Tam. | Obrig. | Chave | Default | Constraint | Descrição |
|---|---|---|---|---|---|---|
| `id_imagem` | INT | Sim | PK / AI | AUTO_INCREMENT | NOT NULL | Identificador único da imagem |
| `id_veiculo` | INT | Sim | FK | — | NOT NULL | Referência para `veiculo.id_veiculo` |
| `url` | VARCHAR(255) | Sim | — | — | NOT NULL | Caminho completo ou URL da imagem |

---

#### `avaliacao`
> Avaliações feitas por usuários sobre veículos. A constraint `UNIQUE(id_usuario, id_veiculo)` impede múltiplas avaliações do mesmo usuário para o mesmo veículo.

| Campo | Tipo / Tam. | Obrig. | Chave | Default | Constraint | Descrição |
|---|---|---|---|---|---|---|
| `id_avaliacao` | INT | Sim | PK / AI | AUTO_INCREMENT | NOT NULL | Identificador único |
| `id_usuario` | INT | Sim | FK | — | NOT NULL | Referência para `usuario.id_usuario` |
| `id_veiculo` | INT | Sim | FK | — | NOT NULL | Referência para `veiculo.id_veiculo` |
| `nota` | TINYINT | Sim | — | — | NOT NULL, CHECK 1-5 | Nota de 1 (péssimo) a 5 (ótimo) |
| `comentario` | TEXT | Não | — | NULL | — | Texto descritivo da avaliação |
| `data` | DATETIME | Sim | — | CURRENT_TIMESTAMP | NOT NULL | Data da avaliação |

---

### Tabelas Associativas

#### `favoritos`
> Tabela associativa N:N entre usuário e veículo para a funcionalidade de lista de desejos. A PK composta `(id_usuario, id_veiculo)` garante que não haja duplicatas.

| Campo | Tipo / Tam. | Obrig. | Chave | Default | Constraint | Descrição |
|---|---|---|---|---|---|---|
| `id_usuario` | INT | Sim | PK / FK | — | NOT NULL | Referência para `usuario.id_usuario` |
| `id_veiculo` | INT | Sim | PK / FK | — | NOT NULL | Referência para `veiculo.id_veiculo` |
| `data_adicionado` | DATETIME | Sim | — | CURRENT_TIMESTAMP | NOT NULL | Data em que o favorito foi salvo |

---

### Tabela de Concessionária

#### `concessionaria`
> Perfil estendido para usuários do tipo `concessionaria`. Contém dados comerciais, endereço e horário de funcionamento.

| Campo | Tipo / Tam. | Obrig. | Chave | Default | Constraint | Descrição |
|---|---|---|---|---|---|---|
| `id_concessionaria` | INT | Sim | PK / AI | AUTO_INCREMENT | NOT NULL | Identificador único |
| `id_usuario` | INT | Sim | FK / UNIQUE | — | NOT NULL, UNIQUE | Referência 1:1 com `usuario` |
| `razao_social` | VARCHAR(200) | Sim | — | — | NOT NULL | Razão social da empresa |
| `cnpj` | VARCHAR(20) | Sim | UNIQUE | — | NOT NULL, UNIQUE | CNPJ (sem máscara) |
| `endereco` | VARCHAR(255) | Sim | — | — | NOT NULL | Endereço completo |
| `cidade` | VARCHAR(100) | Sim | — | — | NOT NULL | Cidade |
| `estado` | VARCHAR(100) | Sim | — | — | NOT NULL | UF (ex.: SP, RJ) |
| `cep` | VARCHAR(50) | Sim | — | — | NOT NULL | CEP no formato `00000-000` |
| `site` | VARCHAR(255) | Não | — | NULL | — | URL do site da concessionária |

---

## Código dbdiagram.io

Cole o código abaixo em [dbdiagram.io](https://dbdiagram.io) para visualizar o diagrama:

```
Table marca {
  id_marca integer [primary key]
  nome varchar(100) [unique, not null]
  logo_url varchar(255)
  pais varchar(80)
}

Table modelo {
  id_modelo integer [primary key]
  nome varchar(150) [unique, not null]
  id_marca integer [ref: > marca.id_marca, not null]
  tipo_carroceria varchar(60)
}

Table combustivel {
  id_combustivel integer [primary key]
  nome varchar(50) [unique, not null]
}

Table cambio {
  id_cambio integer [primary key]
  nome varchar(50) [unique, not null]
}

Table cor {
  id_cor integer [primary key]
  nome varchar(50) [unique, not null]
  hex_code char(7)
}

Table categoria {
  id_categoria integer [primary key]
  nome varchar(100) [unique, not null]
  descricao varchar(255)
}

Table usuarios {
  id integer [primary key]
  nome varchar(150) [not null]
  email varchar(150) [not null]
  senha varchar(150) [not null]
  telefone varchar(20) [not null]
  cpf_cnpj varchar(20) [unique, not null]
  foto_perfil varchar(255)
  tipo enum [not null]
  ativo tinyint(1) [increment] // valor padrão 1
  data_cadastro datetime [not null]
  data_atualizacao datetime // ON UPDATE NOW()
}

Table veiculos {
  id integer [primary key]
  id_modelo integer [ref: < modelo.id_modelo]
  ano_fabricado year [not null]
  ano_modelo year [not null]
  km int [not null]
  valor decimal [not null]
  descricao varchar(255)
  portas tinyint
  placa varchar(10) [unique]
  renavam varchar(20) [unique]
  id_combustivel integer [ref: < combustivel.id_combustivel, not null]
  id_cambio integer [ref: < cambio.id_cambio, not null]
  id_cor integer [ref: < cor.id_cor, not null]
  id_categoria integer [ref: < categoria.id_categoria, not null]
  data_cadastro datetime [not null]
}

table imagens {
  id_imagem integer [primary key]
  id_veiculo integer [ref: < veiculos.id, not null]
  url varchar(255) [not null]
}

table avaliacao {
  id_avaliacao integer [primary key]
  id_usuario integer [ref: - usuarios.id, not null]
  id_veiculo integer [ref: < veiculos.id, not null]
  nota tinyint [not null]
  comentario varchar(255)
  data datetime [not null]
}

table favoritos {
  id_usuario integer [ref: - usuarios.id]
  id_veiculos integer [ref: - veiculos.id]
  data datetime
}

table concessionarias {
  id_concessionaria integer [primary key]
  id_usuario integer [ref: - usuarios.id, not null]
  razao_social varchar(200) [not null]
  cnpj varchar(20) [unique, not null]
  endereco varchar(255) [not null]
  cidade varchar(100) [not null]
  estado varchar(100) [not null]
  cep varchar(50) [not null]
  site varchar(255)
}
```
