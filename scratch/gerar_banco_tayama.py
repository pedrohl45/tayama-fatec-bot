import json

conteudo = {
    "quotes": [
        "Chegou na hora certa. Pega leve aí no trabalho, ninguém é de ferro.",
        "Tá precisando de uma pausa? Às vezes respirar 5 minutos resolve metade dos bugs.",
        "Você passa tempo demais olhando pra essa tela... mas fazer o que, né? A gente tem que pagar os boletos.",
        "Não fica esquentando a cabeça com detalhe bobo. Foca no que importa e resolve o resto depois, ou chora no banho.",
        "Se o código quebrou de novo, dá um passo pra trás antes de quebrar o teclado. Acredite, teclados são caros.",
        "O café esfriou e o código não compila? Calma, acende um cigarro (ou toma uma água) que a lógica clareia.",
        "A faculdade cobra caro da sua sanidade. Tenta não gastar ela toda no primeiro semestre.",
        "Eu não ligo se você usa light theme, desde que você sofra em silêncio cego.",
        "O prazo de entrega é hoje à meia-noite? Legal. Vou colocar um disco de vinil aqui e ver você chorar.",
        "Tem coisas na vida que não tem solução. O erro 500 do seu backend, por outro lado, tem. Abre logo esse log.",
        "Você sabe que copiar do StackOverflow sem ler não te faz programador, né? Mas continua, tá engraçado.",
        "Eu durmo muito pouco para aturar código não documentado. Faça um favor pra mim e pra humanidade.",
        "Terapia é caro, reclamar do código no meu canal é de graça. Só não espere abraços.",
        "A vida é curta demais pra escrever em Java. Brincadeira... ou não.",
        "Se o deploy quebrou na sexta-feira, o problema é seu. Eu tô indo ouvir Deftones."
    ],
    "dev_tips": [
        "**Git**: Faça commits pequenos e descritivos. Salvar 'ajustes' em 30 arquivos de uma vez é pedir pra sofrer no merge.",
        "**Python**: Sempre use `venv`. Se você poluir o ambiente global da sua máquina, não venha chorar pra mim depois.",
        "**Engenharia de Software**: Menos é mais no MVP. Entregue algo simples que funciona antes de inventar 50 features que ninguém vai usar.",
        "**Debug**: Colocar `print('CHEGOU AQUI')` no código inteiro é fofo, mas que tal você aprender a usar um debugger de verdade?",
        "**Documentação**: Eu sei que dá preguiça, mas escreve a droga do README. O você do futuro vai agradecer.",
        "**CSS**: Não sabe centralizar uma div? `flexbox` resolve 90% da sua ansiedade. Os outros 10% são terapia.",
        "**Mentalidade**: Todo código escrito há mais de 6 meses é legado. E adivinha? A culpa provavelmente é sua.",
        "**Arquitetura**: Acoplamento forte é como ex tóxico. Você acha que consegue lidar, até precisar mudar uma regra de negócio.",
        "**Logs**: Tratamento silencioso de erro (`except pass`) devia dar cadeia. Loga isso pelo menos, por favor.",
        "**SQL**: Nunca confie no input do usuário. Parameterize as queries ou vá arrumar o banco depois do Drop Table."
    ],
    "musicas": [
        {"nome": "Lebanon Hanover - Gallowdance", "genre": "Darkwave", "spotify": "https://open.spotify.com/track/74SUn8w4lYSwgOGPvVZiEo", "youtube": "https://www.youtube.com/watch?v=WPw7nlluKk8", "soundcloud": "https://soundcloud.com/lebanon-hanover/gallowdance"},
        {"nome": "She Wants Revenge - Tear You Apart", "genre": "Post-Punk Revival", "spotify": "https://open.spotify.com/track/3urJUvRhgMrwy5TMBJRjHN", "youtube": "https://www.youtube.com/watch?v=ixw_bLVUL34", "soundcloud": "https://soundcloud.com/she-wants-revenge-official/tear-you-apart"},
        {"nome": "Molchat Doma - Sudno", "genre": "Sovietwave", "spotify": "https://open.spotify.com/track/3WS7spXVlbeC5kveVLFOPG", "youtube": "https://www.youtube.com/watch?v=HR5zpFs7YpY", "soundcloud": "https://soundcloud.com/molchatdoma/sudno"},
        {"nome": "Deftones - Be Quiet and Drive", "genre": "Alt Metal / Shoegaze", "spotify": "https://open.spotify.com/track/4Uiw0Sl9yskBaC6P4DcdVD", "youtube": "https://www.youtube.com/watch?v=KvknOXGPzCQ", "soundcloud": "https://soundcloud.com/deftones_official/be-quiet-and-drive-far-away"},
        {"nome": "Boy Harsher - Pain", "genre": "Darkwave", "spotify": "https://open.spotify.com/track/13HKm5ZYugOuuQ8d6N8tIf", "youtube": "https://www.youtube.com/watch?v=H1Zm6E6Sy4Y", "soundcloud": "https://soundcloud.com/boy-harsher/pain"},
        {"nome": "Kino - Spokoynaya Noch", "genre": "Sovietwave / Rock", "spotify": "https://open.spotify.com/track/4jVn4wOedSOP0hK89rUaYg", "youtube": "https://www.youtube.com/watch?v=1b-3RkXp6bQ", "soundcloud": ""},
        {"nome": "Twin Tribes - Shadows", "genre": "Darkwave / Post-Punk", "spotify": "https://open.spotify.com/track/59i9B5q3B08z5F5U3gGz8s", "youtube": "https://www.youtube.com/watch?v=Xh0wz6g9R-A", "soundcloud": ""},
        {"nome": "The Cure - A Forest", "genre": "Goth Rock / Post-Punk", "spotify": "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh", "youtube": "https://www.youtube.com/watch?v=xik-y0piweY", "soundcloud": ""},
        {"nome": "Joy Division - Disorder", "genre": "Post-Punk", "spotify": "https://open.spotify.com/track/5fbQCQwNCsYbEEBABMCYc1", "youtube": "https://www.youtube.com/watch?v=fhCLalLXHP4", "soundcloud": ""},
        {"nome": "Bauhaus - Bela Lugosi's Dead", "genre": "Goth Rock", "spotify": "https://open.spotify.com/track/145g2jA-yZ21nF1m1p1G12", "youtube": "https://www.youtube.com/watch?v=zq7xyjUWps8", "soundcloud": ""},
        {"nome": "Mareux - The Perfect Girl", "genre": "Darkwave", "spotify": "https://open.spotify.com/track/5RBOcBpJXaNlNq9vP6R9b", "youtube": "https://www.youtube.com/watch?v=VbjJqXk6ZUg", "soundcloud": ""},
        {"nome": "Ploho - Novosadki", "genre": "Sovietwave / Post-Punk", "spotify": "https://open.spotify.com/track/3074m6c7cO2Dk2O5T4VfO2", "youtube": "https://www.youtube.com/watch?v=Y7w4w7R8f44", "soundcloud": ""},
        {"nome": "Buerak - Strast", "genre": "Russian Post-Punk", "spotify": "https://open.spotify.com/track/25L4g3U1Q3sZ3fV3R3L3X3", "youtube": "https://www.youtube.com/watch?v=4Yv3r3w6H2k", "soundcloud": ""},
        {"nome": "Sisters of Mercy - Lucretia My Reflection", "genre": "Goth Rock", "spotify": "https://open.spotify.com/track/3J6sD5L4h9z1vL0eR1K6pY", "youtube": "https://www.youtube.com/watch?v=IuezNswtRfo", "soundcloud": ""},
        {"nome": "Pastel Ghost - Dark Beach", "genre": "Dream pop / Darkwave", "spotify": "https://open.spotify.com/track/5Qzm0Q8Q4F0yG99y1H9w3Q", "youtube": "https://www.youtube.com/watch?v=3n9M9A5qE2U", "soundcloud": ""},
        {"nome": "She Past Away - Kasvetli Kutlama", "genre": "Darkwave", "spotify": "https://open.spotify.com/track/2B7T1bX1v9k1n2k6b1u1V2", "youtube": "https://www.youtube.com/watch?v=x211x1f3E2c", "soundcloud": ""}
    ]
}

with open("database/tayama_content.json", "w", encoding="utf-8") as f:
    json.dump(conteudo, f, ensure_ascii=False, indent=4)

print("Banco da Tayama gerado com sucesso!")
