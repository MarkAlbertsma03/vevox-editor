import os

import Modules.file as fl

cwd = os.getcwd()
templates = os.path.join(cwd, "Templates")
template = fl.TXT(os.path.join(templates, "document.tex"))

# Verzamel alle JSON-bestanden
polls = []

for file in os.listdir():
    if file.endswith(".json"):
        polls.append(fl.JSON(os.path.join(cwd, file)))

# Maak voor alle vragenlijsten bijbehorende TeX-bestanden
for poll in polls:
    # Maak een leeg bestand
    document = "\n".join(template.read())
    
    VAR_TITLE = str(input(f"Voer een titel van {poll.filename} in: "))
    VAR_AUTHOR = str(input(f"Voer een auteur van {poll.filename} in: "))
    
    # Voeg alle vragen aan het bestand toe
    VAR_CONTENT = ""
    questions = poll.read()
    
    for x in range(len(questions)):
        question = f"\\subsection*{{Vraag {str(x + 1)}}}\n"
        question += questions[x]["text"] + "\n\n"
        question += "\\begin{itemize}\n"
        
        # Voeg alle keuzes aan de vraag toe
        for y in range(len(questions[x]["choices"])):
            choice = f"({chr(y + 97)})"
            if questions[x]["choices"][y]["isCorrectAnswer"]:
                choice = f"{{\\red {choice}}}"
            question += f"\\item[{choice}]" + "{" + questions[x]["choices"][y]["text"] + "}\n"
        
        question += "\\end{itemize}\n\n"
        VAR_CONTENT += question
    
    # Vervang dubbele dollartekens met een enkele
    VAR_CONTENT = VAR_CONTENT.replace("$$", "$")
    
    # Plaats de nieuwe informatie in het bestand
    document = document.replace("VAR_TITLE", VAR_TITLE)
    document = document.replace("VAR_AUTHOR", VAR_AUTHOR)
    document = document.replace("VAR_CONTENT", VAR_CONTENT)
    
    fl.TXT(os.path.join(cwd, poll.filename[:-4] + "tex")).write(document.split("\n"))

print("De gegenereerde TeX-bestanden kunnen nu worden gebruikt om een LaTeX-bestand te genereren.")
print("Soms werken de bestanden niet meteen; kijk of het fouten bevat.")
input("Klaar!")

