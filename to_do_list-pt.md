# Lista de Tarefas

## Seguindo Passo a Passo
- [x] Gpc - Acesso
- [x] Big Query - Configuração do Datario
- [x] Fazer Fork do Repositório
- [x] Responder `perguntas_sql.md` com SQL
    - [x] `analise_sql.sql` - Criar Arquivo
- [x] Responder `perguntas_sql.md` com Python e Pandas
    - [x] `analise_python.py` - Criar Arquivo
- [x] Autenticação na API
- [x] Responder `perguntas_api.md` com Python e Pandas
    - [x] `analise_api.py` - Criar Arquivo 
- [x] Visualizar Dados da API
    - [x] `preview_data.py` - Criar Arquivo
- [x] Criar arquivo `to-do-list.md`
- [x] Criar arquivo `image_running_scripts.pdf`

`preview_data.py` - Visualização com Streamlit

## Apresentação 
    - Explicando passos 
        - Explicando acesso 
            - Para acessar o Google Cloud, tive facilidade por já fazer uso dele em projetos de automação com consumo de dados.
        - Explicando respostas em `perguntas_sql.md` 
            - Para as perguntas respondidas em SQL, iniciei com a visualização das tabelas e identificação dos atributos que precisaria consultar. As tabelas seguem um padrão lógico de consulta e informações disponibilizadas.
        - Explicando script Python com SQL 
            - Para as consultas em Python, optei por criar funções que representassem cada uma das perguntas. Além disso, inseri as queries dentro de cada uma delas. Retornei os resultados com uma chamada para cada uma das funções.
        - Explicando bibliotecas usadas 
            - Utilizei `basedosdados` para a consulta em SQL com Python. Para o script de consumo das APIs, utilizei `requests`, `datetime` e `statistics`.
        - Explicando API utilizada 
            - Para o consumo das APIs, segui atentamente a documentação de cada uma delas, o que me permitiu consultar os dados para as perguntas com certa facilidade.
        - Explicando visualização com Streamlit  
            - Optei pelo Streamlit View por ser uma biblioteca de fácil demonstração e visualização de dados, além de ser esteticamente agradável.
