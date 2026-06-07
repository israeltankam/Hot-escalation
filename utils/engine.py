import json
import random

class GameEngine:
    def __init__(self, gages_path='data/gages.json'):
        with open(gages_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Supprimer les commentaires // avant de parser le JSON
            import re
            content = re.sub(r'//.*', '', content)
            self.all_gages = json.loads(content)
            
    def filter_gages(self, accepted_tags):
        """Filtre les gages selon les tags acceptés."""
        filtered = []
        for gage in self.all_gages:
            # Un gage est accepté si TOUS ses tags sont dans la liste des tags acceptés
            if all(tag in accepted_tags for tag in gage['tags']):
                filtered.append(gage)
        return filtered

    def get_next_gage(self, current_phase, next_player, history, accepted_tags):
        """Sélectionne le prochain gage avec une montée progressive du niveau Hot."""
        # 1. Filtrage par tags et phase et genre
        available = [g for g in self.filter_gages(accepted_tags) 
                     if g['phase'] == current_phase 
                     and g['target'] == next_player
                     and g['id'] not in history]
        
        if not available:
            return None
            
        # 2. Montée progressive (Hot Smoothing)
        # On trie par niveau Hot
        available.sort(key=lambda x: x['hot'])
        
        # On définit une fenêtre de sélection basée sur la progression dans la phase
        # Si on a déjà fait beaucoup de gages dans cette phase, on pioche plus haut
        gages_done_in_phase = len([h for h in history if any(g['id'] == h and g['phase'] == current_phase for g in self.all_gages)])
        
        # Facteur de progression (0.0 à 1.0)
        # On suppose une dizaine de gages par phase en moyenne
        progression = min(gages_done_in_phase / 10.0, 1.0)
        
        # On prend une sous-liste qui s'élargit vers le haut
        # Au début (progression=0), on prend les 40% les plus bas
        # À la fin (progression=1), on prend toute la liste
        window_size = int(len(available) * (0.4 + 0.6 * progression))
        window_size = max(window_size, 1)
        
        selection_pool = available[:window_size]
        
        # On pioche au hasard dans le pool restreint
        return random.choice(selection_pool)

    def get_drink_suggestion(self):
        """Retourne une suggestion de boisson douce."""
        suggestions = [
            "Prenez une petite gorgée de votre boisson préférée ensemble.",
            "L'un de vous doit servir une gorgée à l'autre.",
            "Trinquez à votre complicité et buvez une gorgée.",
            "Une petite pause fraîcheur ? Une gorgée pour chacun.",
            "L'Homme embrasse la Femme, puis les deux boivent une gorgée."
        ]
        return random.choice(suggestions)
