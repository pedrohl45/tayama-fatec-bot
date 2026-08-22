import glob
import re

for f in glob.glob('cogs/*.py'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    content = re.sub(r'color=discord\.Color\.\w+\(\)', 'color=discord.Color.from_str("#c82245")', content)
    
    if 'fatec_aulas.py' in f:
        old_str = 'f"**Horário:** {aula[\'inicio\']} às {aula[\'fim\']}\\n**Sala:** {aula[\'sala\']}\\n**Professor:** {aula[\'professor\']}"'
        new_str = 'f"**Horário:** {aula[\'inicio\']} às {aula[\'fim\']}\\n**Sala:** {aula[\'sala\']}\\n**Professor:** {aula[\'professor\']}\\n\\u200b"'
        content = content.replace(old_str, new_str)
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
        
print('Cores e espaçamentos substituídos corretamente via Python!')

