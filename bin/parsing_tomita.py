import asyncio
import subprocess
import time
import re

async def get_tomita(content):
    with open('input.txt', 'w', encoding='utf-8') as file:
        file.write(content)
    
    subprocess.run(["./tomita-parser", "config.proto"], check=True)
    time.sleep(2.0)


    with open('output.txt', 'r', encoding='utf-8') as file:
        new_content = file.read()

    pattern = r'\{[^}]+}'
    matches = re.findall(pattern, new_content)

    places = []
    persons = []

    for item in matches:
        match = re.search(r'(\w+)\s*=\s*([^\n]+)', item)
        if match:
            key = match.group(1)
            value = match.group(2)

            if key == 'Place':
                places.append(value)
            elif key == 'Person':
                persons.append(value)
    
    tone = 1
    if places == []:
        places.append('Нет упоминаний')   
    if persons == []:
        persons.append('Нет упоминаний')
    if 'Нет упоминаний' in persons and 'Нет упоминаний' in places:
        tone = 0
    return persons, places, tone

       

