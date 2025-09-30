# Implementação de Servidores Concorrentes

Este repositório contém a implementação e análise de três modelos de servidores concorrentes: Forked, Multithread e Orientado a Eventos (Assíncrono). O objetivo do projeto é comparar as diferentes abordagens para lidar com múltiplas conexões de clientes simultaneamente em um servidor de eco simples.

## Modelos Implementados

Foram desenvolvidas três versões do servidor de eco, cada uma utilizando um modelo de concorrência distinto:

### 1. Servidor Forked

Para cada cliente que se conecta, o servidor cria um novo processo (utilizando

`os.fork()`) para gerenciar a comunicação. O processo pai continua a escutar por novas conexões, enquanto o processo filho se dedica exclusivamente a um cliente.

-   **Código-fonte:** `server_forked/server-fork.py`
    

### 2. Servidor Multithread

Nesta abordagem, cada nova conexão de cliente é gerenciada por uma thread separada dentro do mesmo processo. O módulo

`threading` do Python é utilizado para criar e gerenciar as threads.

-   **Código-fonte:** `server_multithread/server-multithread.py`
    

### 3. Servidor Orientado a Eventos (Assíncrono)

Este modelo utiliza um único processo e uma única thread para lidar com múltiplas conexões de forma não-bloqueante. Com o uso da biblioteca

`asyncio` do Python, o servidor gerencia as conexões de forma assíncrona, otimizando o tempo de espera por operações de I/O (Entrada/Saída).

-   **Código-fonte:** `server_event_driven/server-assincrono.py`
    

## Como Executar o Projeto

O ambiente para execução dos servidores é gerenciado com Docker e Docker Compose, facilitando a configuração e execução.

### Pré-requisitos

-   Docker
    
-   Docker Compose
    

### Execução

1.  Clone o repositório.
    
2.  Navegue até a raiz do projeto e execute o comando abaixo para construir as imagens e iniciar os contêineres:
    
    Bash
    
    ```
    docker-compose up --build
    
    ```
    
3.  Os servidores estarão disponíveis nas seguintes portas:
    
    -   **Servidor Forked:** `localhost:8001`
        
    -   **Servidor Multithread:** `localhost:8002`
        
    -   **Servidor Orientado a Eventos:** `localhost:8003`
        

## Como Testar os Servidores

O projeto inclui dois scripts de cliente para testes: um cliente interativo e um script para teste de carga.

### Cliente Interativo

Para se conectar e enviar mensagens manualmente para um dos servidores:

Bash

```
python cliente/cliente.py <host> <porta>

```

**Exemplo:**

Bash

```
python cliente/cliente.py localhost 8001

```

### Teste de Carga

Para avaliar o desempenho dos servidores sob carga, utilize o script `teste_carga.py`, que simula múltiplos clientes enviando mensagens simultaneamente.

Bash

```
python cliente/teste_carga.py <host> <porta> <num_clientes> <msgs_por_cliente>

```

**Exemplo:**

Bash

```
# Simula 100 clientes enviando 10 mensagens cada para o servidor Forked
python cliente/teste_carga.py localhost 8001 100 10

```

## Resultados do Teste de Desempenho

Os servidores foram submetidos a testes de carga leve e média. Os resultados, medidos em Requisições por Segundo (RPS), consumo de CPU e memória, estão resumidos abaixo:

| Cenário de Teste | Métrica | Servidor Forked | Servidor Multithread | Servidor Orientado a Eventos |
|---|---|---|---|---|
| **Carga Leve** (100 clientes, 10 msgs) | **RPS** | 1553.50 | 1693.69 | 2778.06 |
| | **Consumo Máx. CPU** | ~9% | ~8% | ~11% |
| | **Consumo Máx. Memória** | ~9 MiB | -8 MiB | ~10 MiB |
| **Carga Média** (1000 clientes, 10 msgs) | **RPS** | ~750 | ~1250 | ~2600 |
| | **Consumo Máx. CPU** | ~85% | ~70% | ~45% |
| | **Consumo Máx. Memória** | ~90 MiB | ~30 MiB | ~18 MiB |

## Conclusões

A análise dos resultados dos testes permite destacar as seguintes vantagens e desvantagens de cada abordagem:

### Servidor Forked

-   **Vantagens**: Oferece bom isolamento entre clientes, pois um erro em um processo filho não afeta os demais. Sua implementação é relativamente simples para tarefas básicas.
    
-   **Desvantagens**: Apresenta alto consumo de CPU e memória, uma vez que a criação de processos é uma operação custosa para o sistema operacional. Não escala bem para um grande número de conexões e não é portável para Windows, pois `os.fork()` não está disponível.
    

### Servidor Multithread

-   **Vantagens**: Consome menos recursos que o modelo Forked, pois threads são mais "leves" que processos. O compartilhamento de memória pode facilitar a comunicação interna, embora exija mecanismos de sincronização.
    
-   **Desvantagens**: A complexidade aumenta com a necessidade de gerenciar condições de corrida e usar travas (locks) para sincronização de dados. O custo da troca de contexto entre um número elevado de threads pode degradar o desempenho.
    

### Servidor Orientado a Eventos

-   **Vantagens**: Extremamente eficiente no uso de recursos (CPU e memória), pois utiliza um único processo/thread. É altamente escalável, capaz de lidar com milhares de conexões simultâneas com baixa sobrecarga, sendo a abordagem mais moderna para aplicações com uso intensivo de I/O (I/O-bound).
    
-   **Desvantagens**: A lógica de programação assíncrona pode ser mais complexa para iniciantes. Não é ideal para tarefas que exigem uso intensivo da CPU, pois uma tarefa longa pode bloquear todo o loop de eventos.
