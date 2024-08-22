-- file created -- ok 
-- answer questions - init


-- question 1 
-- Conta o número total de chamados abertos em 01/04/2023
SELECT COUNT(*) AS total_chamados
FROM datario.adm_central_atendimento_1746.chamado
WHERE DATE(data_inicio) = '2023-04-01';

-- answer: 1756 


-- question 2 
-- Seleciona o tipo de chamado mais frequente em 01/04/2023
SELECT tipo, COUNT(*) AS quantidade
FROM datario.adm_central_atendimento_1746.chamado
WHERE DATE(data_inicio) = '2023-04-01'
GROUP BY tipo
ORDER BY quantidade DESC
LIMIT 1;

-- answer: Estacionamento irregular 

-- question 3 
-- Seleciona os 3 bairros com maior número de chamados abertos em 01/04/2023
SELECT b.nome, COUNT(*) AS quantidade
FROM datario.adm_central_atendimento_1746.chamado c
JOIN datario.dados_mestres.bairro b ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = '2023-04-01'
GROUP BY b.nome
ORDER BY quantidade DESC
LIMIT 3;

-- answer: Campo Grande 113, Tijuca 89, Barra da Tijuca 59 


-- question 4 
-- Seleciona a subprefeitura com mais chamados abertos em 01/04/2023
SELECT b.subprefeitura, COUNT(*) AS quantidade
FROM datario.adm_central_atendimento_1746.chamado c
JOIN datario.dados_mestres.bairro b ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = '2023-04-01'
GROUP BY b.subprefeitura
ORDER BY quantidade DESC
LIMIT 1;

-- answer: Zona Norte 510 


-- question 5 
-- Verifica se há chamados em 01/04/2023 sem associação a um bairro ou subprefeitura
SELECT c.id_chamado
FROM datario.adm_central_atendimento_1746.chamado c
LEFT JOIN datario.dados_mestres.bairro b ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = '2023-04-01' AND b.id_bairro IS NULL;

-- answer: Sim, 50 chamados. Isso pode ocorrer por falhas na associação dos chamados com os bairros, 
-- como um código de bairro incorreto ou ausência do bairro na tabela de bairros.

-- question 6 
-- Conta o número total de chamados com o subtipo "Perturbação do sossego" abertos entre 01/01/2022 e 31/12/2023
SELECT COUNT(*) AS total_chamados
FROM datario.adm_central_atendimento_1746.chamado
WHERE subtipo = 'Perturbação do sossego' 
  AND DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31';
-- answer: 42830 chamados 


-- question 7 
-- Seleciona chamados com o subtipo "Perturbação do sossego" abertos durante eventos específicos
SELECT c.*
FROM datario.adm_central_atendimento_1746.chamado c
JOIN datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos e 
  ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
WHERE c.subtipo = 'Perturbação do sossego' 
  AND e.evento IN ('Reveillon', 'Carnaval', 'Rock in Rio');

-- answer : 50 chamados. Não estou listando eles nesse arquivo para não poluir. -- listar posteriormente - pendente 

-- question 8 
-- Conta o número de chamados com o subtipo "Perturbação do sossego" para cada evento específico
SELECT e.evento, COUNT(*) AS total_chamados
FROM datario.adm_central_atendimento_1746.chamado c
JOIN datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos e 
  ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
WHERE c.subtipo = 'Perturbação do sossego' 
  AND e.evento IN ('Reveillon', 'Carnaval', 'Rock in Rio')
GROUP BY e.evento;


-- answer: Rock in Rio 834, Carnaval 241, Reveillon 139. 

-- question 9 
-- Calcula a média diária de chamados com o subtipo "Perturbação do sossego" para cada evento e seleciona o evento com a maior média
SELECT 
    e.evento, 
    COUNT(*) / (DATE_DIFF(MAX(e.data_final), MIN(e.data_inicial), DAY) + 1) AS media_diaria
FROM 
    datario.adm_central_atendimento_1746.chamado c
JOIN 
    datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos e 
ON 
    DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
WHERE 
    c.subtipo = 'Perturbação do sossego' 
    AND e.evento IN ('Reveillon', 'Carnaval', 'Rock in Rio')
GROUP BY 
    e.evento
ORDER BY 
    media_diaria DESC
LIMIT 1;

-- answer: 83.4 


-- question 10 
-- Calcula as médias diárias de chamados com o subtipo "Perturbação do sossego" durante os eventos e no período total
WITH media_eventos AS (
    SELECT 
        e.evento, 
        COUNT(*) / (DATE_DIFF(MAX(e.data_final), MIN(e.data_inicial), DAY) + 1) AS media_diaria_evento
    FROM 
        datario.adm_central_atendimento_1746.chamado c
    JOIN 
        datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos e 
    ON 
        DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
    WHERE 
        c.subtipo = 'Perturbação do sossego' 
        AND e.evento IN ('Reveillon', 'Carnaval', 'Rock in Rio')
    GROUP BY 
        e.evento
),
media_total AS (
    SELECT 
        COUNT(*) / (DATE_DIFF(DATE '2023-12-31', DATE '2022-01-01', DAY) + 1) AS media_diaria_total
    FROM 
        datario.adm_central_atendimento_1746.chamado
    WHERE 
        subtipo = 'Perturbação do sossego' 
        AND DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
)
SELECT 
    e.evento, 
    e.media_diaria_evento, 
    t.media_diaria_total
FROM 
    media_eventos e, 
    media_total t;

-- answer: Rock in Rio media_diaria_evento: 83.4. Carnaval media_diaria_evento: 60.25. Reveillon media_diaria_evento: 46.33. media_diaria_total: 58.67