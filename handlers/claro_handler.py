#claro_handler.py
async def claro_auto_atendimento(event):
    await event.reply(
        "💬 **Auto Atendimento Claro** 💬\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Selecione uma das opções abaixo para obter ajuda:\n\n"
        "1️⃣ **Não Conecta**\n"
        "2️⃣ **Não Gera Dados**\n"
        "🔙 Escreva `Voltar` para retornar ao menu anterior",
        parse_mode='md'
    )

async def handle_claro_auto_atendimento(event, text, user_state):
    user_id = event.sender_id
    if text == '1':
        await problema_conexao_claro(event)
    elif text == '2':
        await nao_gera_dados_claro(event)
    elif text == 'voltar' or text == 'menu':
        user_state[user_id] = 'auto_atendimento'
        await claro_auto_atendimento(event)
    else:
        await event.reply(
            "⚠️ Opção inválida. Por favor, selecione uma das opções do menu de autoatendimento Claro.\n"
            "🔙 Escreva `Voltar` para retornar ao menu anterior",
            parse_mode='md'
        )

async def problema_conexao_claro(event):
    await event.reply(
        "🌐 **Problema de Conexão Claro** 🌐\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "1. **Plano Necessário:** Na Claro, é necessário ter algum plano contratado (Pré, Pós, Flex, Controle ou qualquer plano mensal).\n"
        "   Você pode utilizar o aplicativo após terminar a franquia do seu plano ou, em alguns casos, com o plano expirado.\n\n"
        "2. **Modo Avião:** Em poucos DDDs funciona sem plano. Use o modo avião até encontrar o IP específico (Nosso aplicativo força o modo avião se não conectar de primeira).\n\n"
        "🔙 Escreva `Voltar` para retornar ao menu anterior",
        parse_mode='md'
    )

async def nao_gera_dados_claro(event):
    await event.reply(
        "🌐 **Não Gera Dados Claro** 🌐\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "1. **IPV4:** Na Claro, normalmente, basta mudar para IPV4.\n"
        "2. **Usar 3G:** Teste se conectar e gerar dados usando o 3G.\n"
        "🔙 Escreva `Voltar` para retornar ao menu anterior",
        parse_mode='md'
    )
