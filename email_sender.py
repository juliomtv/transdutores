import win32com.client as win32

def send_notification_email(config, transducers_to_notify):
    """
    Envia um e-mail de notificação sobre transdutores próximos do vencimento
    usando a integração com o Microsoft Outlook via win32com.client.
    
    Args:
        config (dict): Dicionário com as configurações de e-mail (apenas RECIPIENTS será usado).
        transducers_to_notify (list): Lista de dicionários de transdutores que precisam de notificação.
    """
    
    if not transducers_to_notify:
        return "Nenhum transdutor para notificar."

    try:
        # 1. Criar a integração com o Outlook
        outlook = win32.Dispatch('outlook.application')
        
        # 2. Criar um novo item de e-mail
        email = outlook.CreateItem(0)
        
        # 3. Configurar destinatários e assunto
        email.To = ", ".join(config['RECIPIENTS'])
        subject = f"ALERTA DE VENCIMENTO DE TRANSDUTORES - {len(transducers_to_notify)} Itens"
        email.Subject = subject
        
        # 4. Criar o corpo do e-mail em HTML
        table_rows = "".join([
            f"<tr>"
            f"<td>{t['id']}</td>"
            f"<td>{t['descricao']}</td>"
            f"<td>{t['numero_serie']}</td>"
            f"<td>{t['localizacao']}</td>"
            f"<td>{t['validade_formatada']}</td>"
            f"<td style='color: {'#ED1C24' if t['dias_restantes'] <= 10 else '#ffc107'}; font-weight: bold;'>{t['dias_restantes']} dias</td>"
            f"</tr>"
            for t in transducers_to_notify
        ])
        
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; color: #333; }}
                    .header {{ background-color: #4B1F68; color: white; padding: 10px; text-align: center; }}
                    .container {{ margin: 20px; }}
                    table {{ width: 100%; border-collapse: collapse; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>Alerta de Vencimento de Transdutores</h2>
                </div>
                <div class="container">
                    <p>Prezado(a) usuário(a),</p>
                    <p>Os seguintes transdutores estão próximos da data de validade:</p>
                    
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Descrição</th>
                                <th>Nº de Série</th>
                                <th>Localização</th>
                                <th>Validade (Dia/Mês/Ano)</th>
                                <th>Dias para Vencer</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows}
                        </tbody>
                    </table>
                    
                    <p>Por favor, tome as medidas necessárias.</p>
                    <p>Este é um e-mail automático enviado via Microsoft Outlook. Por favor, não responda.</p>
                </div>
            </body>
        </html>
        """
        
        email.HTMLBody = html_content
        
        # 5. Enviar o e-mail
        email.Send()
        
        return f"E-mail de notificação enviado com sucesso via Microsoft Outlook para {len(config['RECIPIENTS'])} destinatários."
        
    except Exception as e:
        return f"Erro ao enviar e-mail de notificação via Microsoft Outlook. Verifique se o Outlook está aberto e se a biblioteca pywin32 está instalada. Erro: {e}"

if __name__ == '__main__':
    print("Módulo de envio de e-mail pronto para usar win32com.client (Outlook).")