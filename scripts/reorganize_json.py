import json
import os
import re

path = 'data/gages.json'
if not os.path.exists(path):
    print(f"File {path} not found.")
    exit(1)

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Nettoyage préventif des erreurs de syntaxe JSON courantes
content = re.sub(r'\}\s*\{', '},\n  {', content) # Virgules manquantes
content = re.sub(r',(\s*[\]\}])', r'\1', content) # Virgules traînantes
content = re.sub(r'//.*', '', content) # Supprimer les anciens commentaires

try:
    gages = json.loads(content)
except Exception as e:
    print(f"Error parsing JSON: {e}")
    exit(1)

# Tri par phase puis par hotness
gages.sort(key=lambda x: (int(x.get('phase', 0)), int(x.get('hot', 0))))

# Réattribution des IDs
for i, g in enumerate(gages):
    g['id'] = i + 1

# Groupement par phase pour l'insertion des commentaires
phases = {}
for g in gages:
    p = g.get('phase', 0)
    if p not in phases:
        phases[p] = []
    phases[p].append(g)

# Construction manuelle du fichier JSON avec commentaires
output = ["[\n"]
sorted_phases = sorted(phases.keys())
max_p = sorted_phases[-1] if sorted_phases else 0

for p in sorted_phases:
    output.append(f"  // ==========================================\n")
    output.append(f"  // PHASE {p}\n")
    output.append(f"  // ==========================================\n")
    
    phase_gages = phases[p]
    for i, gage in enumerate(phase_gages):
        gage_str = json.dumps(gage, ensure_ascii=False, indent=2)
        # Indentation pour le fichier final
        indented = "\n".join("  " + line for line in gage_str.split("\n"))
        output.append(indented)
        
        # Virgule sauf pour le tout dernier élément absolu
        if not (p == max_p and i == len(phase_gages) - 1):
            output.append(",")
        output.append("\n")

output.append("]")

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(output)

print(f"Successfully reorganized {len(gages)} gages with phase comments.")
