import basedosdados as bd

# Function to count the total number of calls on a specific date
# Question 1 
def get_total_chamados_by_date(date):
    query = f"""
    SELECT COUNT(*) AS total_chamados
    FROM `datario.adm_central_atendimento_1746.chamado`
    WHERE DATE(data_inicio) = '{date}';
    """
    return bd.read_sql(query=query, billing_project_id="dados-rio-433018")

# Function to find the most frequent type of call on a specific date
# Question 2
def get_most_frequent_tipo_by_date(date):
    query = f"""
    SELECT tipo, COUNT(*) AS quantidade
    FROM `datario.adm_central_atendimento_1746.chamado`
    WHERE DATE(data_inicio) = '{date}'
    GROUP BY tipo
    ORDER BY quantidade DESC
    LIMIT 1;
    """
    return bd.read_sql(query=query, billing_project_id="dados-rio-433018")

# Function to get the top 3 neighborhoods with the most calls on a specific date
# Question 3
def get_top_3_bairros_by_date(date):
    query = f"""
    SELECT b.nome, COUNT(*) AS quantidade
    FROM `datario.adm_central_atendimento_1746.chamado` c
    JOIN `datario.dados_mestres.bairro` b ON c.id_bairro = b.id_bairro
    WHERE DATE(c.data_inicio) = '{date}'
    GROUP BY b.nome
    ORDER BY quantidade DESC
    LIMIT 3;
    """
    return bd.read_sql(query=query, billing_project_id="dados-rio-433018")

# Function to find the subprefecture with the most calls on a specific date
# Question 4
def get_top_subprefeitura_by_date(date):
    query = f"""
    SELECT b.subprefeitura, COUNT(*) AS quantidade
    FROM `datario.adm_central_atendimento_1746.chamado` c
    JOIN `datario.dados_mestres.bairro` b ON c.id_bairro = b.id_bairro
    WHERE DATE(c.data_inicio) = '{date}'
    GROUP BY b.subprefeitura
    ORDER BY quantidade DESC
    LIMIT 1;
    """
    return bd.read_sql(query=query, billing_project_id="dados-rio-433018")

# Function to find calls without an associated neighborhood or subprefecture on a specific date
# Question 5
def get_chamados_without_bairro_or_subprefeitura(date):
    query = f"""
    SELECT c.id_chamado
    FROM `datario.adm_central_atendimento_1746.chamado` c
    LEFT JOIN `datario.dados_mestres.bairro` b ON c.id_bairro = b.id_bairro
    WHERE DATE(c.data_inicio) = '{date}' AND b.id_bairro IS NULL;
    """
    return bd.read_sql(query=query, billing_project_id="dados-rio-433018")

# Function to count the total number of calls with a specific subtype in a date range
# Question 6
def get_total_chamados_by_subtype_and_date_range(subtype, start_date, end_date):
    query = f"""
    SELECT COUNT(*) AS total_chamados
    FROM `datario.adm_central_atendimento_1746.chamado`
    WHERE subtipo = '{subtype}' 
      AND DATE(data_inicio) BETWEEN '{start_date}' AND '{end_date}';
    """
    return bd.read_sql(query=query, billing_project_id="dados-rio-433018")

# Function to get calls with a specific subtype during specific events
# Question 7 
def get_chamados_during_events(subtype, events):
    query = f"""
    SELECT c.*
    FROM `datario.adm_central_atendimento_1746.chamado` c
    JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e 
      ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
    WHERE c.subtipo = '{subtype}' 
      AND e.evento IN ({', '.join([f"'{event}'" for event in events])});
    """
    return bd.read_sql(query=query, billing_project_id="dados-rio-433018")

# Function to count the total number of calls for each specific event
# Question 8
def get_total_chamados_for_each_event(subtype, events):
    query = f"""
    SELECT e.evento, COUNT(*) AS total_chamados
    FROM `datario.adm_central_atendimento_1746.chamado` c
    JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e 
      ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
    WHERE c.subtipo = '{subtype}' 
      AND e.evento IN ({', '.join([f"'{event}'" for event in events])})
    GROUP BY e.evento;
    """
    return bd.read_sql(query=query, billing_project_id="dados-rio-433018")

# Function to calculate the daily average of calls for each event
# Question 9
def get_daily_average_calls_for_each_event(subtype, events):
    query = f"""
    SELECT 
        e.evento, 
        COUNT(*) / (DATE_DIFF(MAX(e.data_final), MIN(e.data_inicial), DAY) + 1) AS media_diaria
    FROM 
        `datario.adm_central_atendimento_1746.chamado` c
    JOIN 
        `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e 
    ON 
        DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
    WHERE 
        c.subtipo = '{subtype}' 
        AND e.evento IN ({', '.join([f"'{event}'" for event in events])})
    GROUP BY 
        e.evento
    ORDER BY 
        media_diaria DESC
    LIMIT 1;
    """
    return bd.read_sql(query=query, billing_project_id="dados-rio-433018")

# Function to calculate the daily average of calls during events and for the total period
# Question 10
def get_daily_average_calls_during_events_and_total(subtype, events, start_date, end_date):
    query = f"""
    WITH media_eventos AS (
        SELECT 
            e.evento, 
            COUNT(*) / (DATE_DIFF(MAX(e.data_final), MIN(e.data_inicial), DAY) + 1) AS media_diaria_evento
        FROM 
            `datario.adm_central_atendimento_1746.chamado` c
        JOIN 
            `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e 
        ON 
            DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
        WHERE 
            c.subtipo = '{subtype}' 
            AND e.evento IN ({', '.join([f"'{event}'" for event in events])})
        GROUP BY 
            e.evento
    ),
    media_total AS (
        SELECT 
            COUNT(*) / (DATE_DIFF(DATE '{end_date}', DATE '{start_date}', DAY) + 1) AS media_diaria_total
        FROM 
            `datario.adm_central_atendimento_1746.chamado`
        WHERE 
            subtipo = '{subtype}' 
            AND DATE(data_inicio) BETWEEN '{start_date}' AND '{end_date}'
    )
    SELECT 
        e.evento, 
        e.media_diaria_evento, 
        t.media_diaria_total
    FROM 
        media_eventos e, 
        media_total t;
    """
    return bd.read_sql(query=query, billing_project_id="dados-rio-433018")

# Execute the functions and print the results
if __name__ == "__main__":
    print("Question 1:", get_total_chamados_by_date('2023-04-01'))
    print("Question 2:", get_most_frequent_tipo_by_date('2023-04-01'))
    print("Question 3:", get_top_3_bairros_by_date('2023-04-01'))
    print("Question 4:", get_top_subprefeitura_by_date('2023-04-01'))
    print("Question 5:", get_chamados_without_bairro_or_subprefeitura('2023-04-01'))
    print("Question 6:", get_total_chamados_by_subtype_and_date_range('Perturbação do sossego', '2022-01-01', '2023-12-31'))
    print("Question 7:", get_chamados_during_events('Perturbação do sossego', ['Reveillon', 'Carnaval', 'Rock in Rio']))
    print("Question 8:", get_total_chamados_for_each_event('Perturbação do sossego', ['Reveillon', 'Carnaval', 'Rock in Rio']))
    print("Question 9:", get_daily_average_calls_for_each_event('Perturbação do sossego', ['Reveillon', 'Carnaval', 'Rock in Rio']))
    print("Question 10:", get_daily_average_calls_during_events_and_total('Perturbação do sossego', ['Reveillon', 'Carnaval', 'Rock in Rio'], '2022-01-01', '2023-12-31'))
