#auto_atendimento.py
async def auto_atendimento(event):
    await event.reply(
        "💬 **Auto Atendimento** 💬\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔹 Nosso autoatendimento resolve **90%** dos possíveis problemas, como:\n"
        "  • Não conseguir conectar\n"
        "  • Conectar e não gerar dados\n"
        "  • Entre outros!\n\n"
        "Entre em contato com @netdez_suporte_bot!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 **Digite** `Menu` **para solicitar o menu de alternativas novamente**",
        parse_mode='md'
    )
