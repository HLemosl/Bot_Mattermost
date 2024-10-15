## Mattermost Alert Bot

Este projeto é um **bot de alertas para o Mattermost**, projetado para analisar dados de instâncias e gerar alertas de uso de recursos. O bot busca dados em bancos de dados externos, verifica instâncias com desperdício de recursos e envia mensagens para canais do Mattermost informando os administradores sobre esses casos.

## Estrutura do Projeto

```plaintext
.
├── analysis
│   └── analyser_simulation.py   # Simulação de análise de uso de RAM
├── bot
│   └── bot.py                   # Lógica principal do bot
├── communication
│   └── communicator.py          # Comunicação com o servidor do Mattermost
├── data_fetcher
│   ├── auxiliar_database
│   │   └── auxiliar_database.py  # Conexão com o banco de dados auxiliar
│   ├── auxiliar_database_api.py  # API para interagir com o banco de dados auxiliar
│   └── database_actions.py       # Operações de inserção, atualização e busca no banco
├── message
│   ├── alert_checker.py          # Verificação de alertas pendentes
│   ├── alert_generator.py        # Geração de novos alertas
│   └── message_generator.py      # Geração de mensagens de alerta
├── tools
│   └── utils.py                  # Utilitários, incluindo sistema de logs
├── .env                          # Variáveis de ambiente
├── README.md                     # Arquivo de documentação
├── bot-mattermost.log            # Arquivo de log do bot
└── main.py                       # Script principal que inicia o bot
```

## Funcionalidades

*   **Análise de Instâncias**: O bot realiza uma análise de instâncias a partir de um banco de dados externo, identificando casos de desperdício de recursos.
*   **Geração de Alertas**: Para instâncias que apresentem problemas, o bot cria e armazena alertas no banco de dados auxiliar.
*   **Envio de Mensagens no Mattermost**: O bot envia mensagens detalhadas sobre os alertas encontrados diretamente para canais do Mattermost, baseado nos projetos afetados.
*   **Logs**: Toda atividade do bot é registrada no arquivo `bot-mattermost.log`.

## Como Funciona

1.  O script `main.py` carrega as variáveis de ambiente e inicializa o bot.
2.  O bot analisa os dados das instâncias usando o analisar contido em `analysis/` (caso não tenha, configure um antes).
3.  Se forem encontrados problemas de desperdício, ele cria alertas no banco de dados auxiliar (`data_fetcher/database_actions.py`).
4.  Em seguida, o bot verifica os alertas e envia mensagens para os canais correspondentes no Mattermost (importante criar os canais antes).

## Instalação

### 1\. Clone o Repositório

```plaintext
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### 2\. Dependências

Certifique-se de ter o **Python 3.8+** instalado. Instale as dependências listadas em `requirements.txt`:

```plaintext
pip install -r requirements.txt
```

Ou instale manualmente, se necessário:

```plaintext
pip install python-dotenv requests Flask psycopg2
```

### 3\. Configuração do Ambiente

Complete o arquivo `.env` na raiz do projeto em suas respectivas variáveis:

```plaintext
MATTERMOST_BOT_TOKEN='Seu_Token_Aqui'
MATTERMOST_SERVER_URL='https://mattermost.server.com' # Sem /api/v4
TEAM_MATTERMOST_NAME='Nome_do_Time'

EXTERNAL_DATABASE_URL='URL_do_Banco_Externo'

AUX_DB_NAME='bot_auxiliar_database'
AUX_DB_USER='seu_usuario'
AUX_DB_PASSWORD='sua_senha'
AUXILIARY_DATABASE_URL='http://localhost:5001'
```

### 4\. Inicializando o Banco de Dados Auxiliar

O banco de dados auxiliar é utilizado para armazenar os alertas. Para configurar o banco:

1.  Certifique-se de que o PostgreSQL esteja instalado e rodando.
2.  No diretório `data_fetcher/auxiliar_database/`, execute:

```plaintext
python auxiliar_database.py
```

Isso criará o banco de dados auxiliar e a tabela necessária.

### 5\. Criação dos Channels

É importante que o os canais dos projetos sejam criados antes, pois o script busca os canais específicos pelo nome do projeto.  
  
Exemplo:   
  
**Projeto:** example  
**O script irá buscar o canal por:** project-example

Esse modo de busca pelo canal pode ser alterado no arquivo `bot.py`.

### 6\. Executando o Bot

Para iniciar o bot, execute o script principal:

```plaintext
python main.py
```

O bot começará a analisar os dados e a gerar alertas. As mensagens de alerta serão enviadas automaticamente para os canais configurados no Mattermost.

## Exemplo de Log

```plaintext
2024-08-21 13:23:04,061 - DEBUG - Starting new HTTPS connection (1): mattermost.server.com.br:443
2024-08-21 13:23:04,581 - INFO - Usuário example.test encontrado com sucesso
2024-08-29 18:50:43,824 - ERROR - Erro ao buscar canais com o termo 'test-channel': Invalid URL 'None/channels': No scheme supplied. Perhaps you meant https://None/channels?
```

## Contribuição

Contribuições são bem-vindas! Para propor melhorias, siga o fluxo padrão de **fork** e **pull request**.
