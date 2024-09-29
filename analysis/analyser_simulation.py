def ram_analyser(conn):

    alert_data = {
        "project_name": "Projeto Alpha",
        "creator_name": "João Silva",
        "instance_name": "Joao-VM",
        "instance_id": "i-1234567890abcdef",
        "flavor_name": "general.large",
        "uptime": "2 dias, 4 horas, 12 minutos",
        "alert_reason": "Baixo uso de RAM para a quantidade alocada para a instância"
    }
    
    return [alert_data]
