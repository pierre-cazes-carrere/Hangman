import pygame
import random
import sys
import json

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 800
HAUTEUR = 600
NOIR = (0, 0, 0)
CYAN = (0, 255, 255)
BLEU_FONCE = (0, 20, 40)
VERT_MATRIX = (0, 255, 0)
ROUGE_NEON = (255, 0, 100)

# Configuration de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("HACK'N'HANG")  

# Configuration du texte
police = pygame.font.Font(None, 36)
police_titre = pygame.font.Font(None, 50)

class JeuPendu:
    def __init__(self, difficulte='normal'):
        self.mot = ""
        self.lettres_trouvees = set()
        self.lettres_ratees = set()
        self.erreurs = 0
        self.max_erreurs = 7  # Toujours 7 erreurs
        self.en_cours = True
        self.message_systeme = "INITIALISATION DU SYSTÈME..."
        self.difficulte = difficulte
        
    def charger_mot(self):
        with open("mots.txt", "r", encoding="utf-8") as fichier:
            mots = fichier.read().splitlines()
            # En mode difficile, on prend des mots plus longs
            if self.difficulte == 'difficile':
                mots = [mot for mot in mots if len(mot) >= 8]
            # En mode facile, on prend des mots plus courts (5 lettres max)
            elif self.difficulte == 'facile':
                mots = [mot for mot in mots if len(mot) <= 5]
            # En mode normal, tous les mots sont possibles
        self.mot = random.choice(mots).lower()
        self.message_systeme = "MOT SÉLECTIONNÉ DANS LA BASE DE DONNÉES"
        
    def ajouter_mot(self, nouveau_mot):
        with open("mots.txt", "a", encoding="utf-8") as fichier:
            fichier.write(f"\n{nouveau_mot}")
            
    def afficher_mot_cache(self):
        return " ".join(lettre if lettre in self.lettres_trouvees else "█" for lettre in self.mot)
        
    def verifier_lettre(self, lettre):
        if not self.en_cours:
            return
            
        if lettre in self.mot:
            self.lettres_trouvees.add(lettre)
            # Message système uniquement si le jeu continue
            if not all(lettre in self.lettres_trouvees for lettre in self.mot):
                self.message_systeme = "SÉQUENCE CORRECTE DÉTECTÉE"
            else:
                self.en_cours = False
                self.message_systeme = "DÉCRYPTAGE RÉUSSI"
        else:
            self.lettres_ratees.add(lettre)
            self.erreurs += 1
            # Message système uniquement si le jeu continue
            if self.erreurs < self.max_erreurs:
                self.message_systeme = "ERREUR DE SÉQUENCE DÉTECTÉE"
            else:
                self.en_cours = False
                self.message_systeme = "SYSTÈME CORROMPU"

    def dessiner_pendu(self):
        # Grille de fond cyberpunk (plus subtile)
        for i in range(0, LARGEUR, 40):
            pygame.draw.line(fenetre, (0, 30, 30), (i, 0), (i, HAUTEUR), 1)
        for i in range(0, HAUTEUR, 40):
            pygame.draw.line(fenetre, (0, 30, 30), (0, i), (LARGEUR, i), 1)
            
        # Structure du pendu (potence futuriste)
        pygame.draw.line(fenetre, CYAN, (0, 500), (200, 500), 5)  # Base toujours visible
        
        if self.erreurs > 0:  # 1ère erreur : poteau vertical
            pygame.draw.line(fenetre, CYAN, (100, 500), (100, 100), 5)
        
        if self.erreurs > 1:  # 2ème erreur : poteau horizontal
            pygame.draw.line(fenetre, CYAN, (100, 100), (300, 100), 5)
        
        if self.erreurs > 2:  # 3ème erreur : corde
            pygame.draw.line(fenetre, CYAN, (300, 100), (300, 150), 5)
        
        if self.erreurs > 3:  # 4ème erreur : tête
            pygame.draw.rect(fenetre, CYAN, (275, 150, 50, 40), 2)
            if self.erreurs >= self.max_erreurs:
                # Yeux en X si perdu
                pygame.draw.line(fenetre, ROUGE_NEON, (285, 165), (295, 175), 2)
                pygame.draw.line(fenetre, ROUGE_NEON, (295, 165), (285, 175), 2)
                pygame.draw.line(fenetre, ROUGE_NEON, (305, 165), (315, 175), 2)
                pygame.draw.line(fenetre, ROUGE_NEON, (315, 165), (305, 175), 2)
            else:
                # Yeux normaux
                pygame.draw.rect(fenetre, VERT_MATRIX, (285, 165, 10, 10), 0)
                pygame.draw.rect(fenetre, VERT_MATRIX, (305, 165, 10, 10), 0)
        
        if self.erreurs > 4:  # 5ème erreur : corps et circuits
            pygame.draw.rect(fenetre, CYAN, (275, 190, 50, 60), 2)
            for y in range(200, 240, 10):
                pygame.draw.line(fenetre, VERT_MATRIX, (280, y), (320, y), 1)
        
        if self.erreurs > 5:  # 6ème erreur : bras
            pygame.draw.line(fenetre, CYAN, (275, 200), (250, 230), 2)  # Bras gauche
            pygame.draw.line(fenetre, CYAN, (325, 200), (350, 230), 2)  # Bras droit
        
        if self.erreurs > 6:  # 7ème erreur : jambes et circuits finaux
            pygame.draw.line(fenetre, CYAN, (285, 250), (275, 290), 2)  # Jambe gauche
            pygame.draw.line(fenetre, CYAN, (315, 250), (325, 290), 2)  # Jambe droite
            pygame.draw.line(fenetre, VERT_MATRIX, (275, 270), (280, 270), 1)  # Circuit jambe
            pygame.draw.line(fenetre, VERT_MATRIX, (320, 270), (325, 270), 1)  # Circuit jambe

    def calculer_score(self):
        # Base de points selon la difficulté
        if self.difficulte == 'facile':
            points_base = 100
        elif self.difficulte == 'difficile':
            points_base = 300
        else:  # normal
            points_base = 200
            
        # Bonus pour les lettres restantes
        bonus_erreurs = (self.max_erreurs - self.erreurs) * 50
        
        # Score final
        return points_base + bonus_erreurs if not self.erreurs >= self.max_erreurs else 0

def menu_principal():
    while True:
        fenetre.fill(BLEU_FONCE)
        # Grille de fond
        for i in range(0, LARGEUR, 20):
            pygame.draw.line(fenetre, (0, 50, 50), (i, 0), (i, HAUTEUR), 1)
        for i in range(0, HAUTEUR, 20):
            pygame.draw.line(fenetre, (0, 50, 50), (0, i), (LARGEUR, i), 1)
            
        titre = police_titre.render("HACK'N'HANG", True, CYAN)
        sous_titre = police.render("DÉCRYPTEZ LE CODE OU SOMBREZ", True, VERT_MATRIX)
        
        fenetre.blit(titre, (LARGEUR//2 - titre.get_width()//2, 80))
        fenetre.blit(sous_titre, (LARGEUR//2 - sous_titre.get_width()//2, 140))
        
        # Création des rectangles pour les boutons
        rect_jouer = pygame.Rect(LARGEUR//2 - 150, HAUTEUR//2, 300, 40)
        rect_scores = pygame.Rect(LARGEUR//2 - 150, HAUTEUR//2 + 50, 300, 40)
        rect_ajouter = pygame.Rect(LARGEUR//2 - 150, HAUTEUR//2 + 100, 300, 40)
        rect_quitter = pygame.Rect(LARGEUR//2 - 150, HAUTEUR//2 + 150, 300, 40)
        
        # Vérification si la souris est sur un bouton
        pos_souris = pygame.mouse.get_pos()
        couleur_jouer = ROUGE_NEON if rect_jouer.collidepoint(pos_souris) else VERT_MATRIX
        couleur_scores = ROUGE_NEON if rect_scores.collidepoint(pos_souris) else VERT_MATRIX
        couleur_ajouter = ROUGE_NEON if rect_ajouter.collidepoint(pos_souris) else VERT_MATRIX
        couleur_quitter = ROUGE_NEON if rect_quitter.collidepoint(pos_souris) else VERT_MATRIX
        
        texte_jouer = police.render("[ 1 ] LANCER SÉQUENCE", True, couleur_jouer)
        texte_scores = police.render("[ 2 ] SCORES", True, couleur_scores)
        texte_ajouter = police.render("[ 3 ] AJOUTER DONNÉES", True, couleur_ajouter)
        texte_quitter = police.render("[ 4 ] DÉCONNEXION", True, couleur_quitter)
        
        fenetre.blit(texte_jouer, (LARGEUR//2 - 100, HAUTEUR//2))
        fenetre.blit(texte_scores, (LARGEUR//2 - 100, HAUTEUR//2 + 50))
        fenetre.blit(texte_ajouter, (LARGEUR//2 - 100, HAUTEUR//2 + 100))
        fenetre.blit(texte_quitter, (LARGEUR//2 - 100, HAUTEUR//2 + 150))
        
        # Animation clignotante
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.rect(fenetre, VERT_MATRIX, (LARGEUR//2 - 120, HAUTEUR//2 + pygame.time.get_ticks()//1000 % 3 * 50, 10, 10))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "jouer"
                elif event.key == pygame.K_2:
                    return "scores"
                elif event.key == pygame.K_3:
                    return "ajouter"
                elif event.key == pygame.K_4:
                    return "quitter"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if rect_jouer.collidepoint(event.pos):
                        return "jouer"
                    elif rect_scores.collidepoint(event.pos):
                        return "scores"
                    elif rect_ajouter.collidepoint(event.pos):
                        return "ajouter"
                    elif rect_quitter.collidepoint(event.pos):
                        return "quitter"

def menu_difficulte():
    while True:
        fenetre.fill(BLEU_FONCE)
        # Grille de fond
        for i in range(0, LARGEUR, 20):
            pygame.draw.line(fenetre, (0, 50, 50), (i, 0), (i, HAUTEUR), 1)
        for i in range(0, HAUTEUR, 20):
            pygame.draw.line(fenetre, (0, 50, 50), (0, i), (LARGEUR, i), 1)
            
        titre = police_titre.render("SÉLECTION DIFFICULTÉ", True, CYAN)
        
        # Création des rectangles pour les boutons
        rect_facile = pygame.Rect(LARGEUR//2 - 150, HAUTEUR//2, 300, 40)
        rect_normal = pygame.Rect(LARGEUR//2 - 150, HAUTEUR//2 + 50, 300, 40)
        rect_difficile = pygame.Rect(LARGEUR//2 - 150, HAUTEUR//2 + 100, 300, 40)
        
        # Vérification si la souris est sur un bouton
        pos_souris = pygame.mouse.get_pos()
        couleur_facile = ROUGE_NEON if rect_facile.collidepoint(pos_souris) else VERT_MATRIX
        couleur_normal = ROUGE_NEON if rect_normal.collidepoint(pos_souris) else VERT_MATRIX
        couleur_difficile = ROUGE_NEON if rect_difficile.collidepoint(pos_souris) else VERT_MATRIX
        
        texte_facile = police.render("[ 1 ] FACILE", True, couleur_facile)
        texte_normal = police.render("[ 2 ] NORMAL", True, couleur_normal)
        texte_difficile = police.render("[ 3 ] DIFFICILE", True, couleur_difficile)
        
        fenetre.blit(titre, (LARGEUR//2 - titre.get_width()//2, 100))
        fenetre.blit(texte_facile, (LARGEUR//2 - 100, HAUTEUR//2))
        fenetre.blit(texte_normal, (LARGEUR//2 - 100, HAUTEUR//2 + 50))
        fenetre.blit(texte_difficile, (LARGEUR//2 - 100, HAUTEUR//2 + 100))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'facile'
                elif event.key == pygame.K_2:
                    return 'normal'
                elif event.key == pygame.K_3:
                    return 'difficile'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if rect_facile.collidepoint(event.pos):
                        return 'facile'
                    elif rect_normal.collidepoint(event.pos):
                        return 'normal'
                    elif rect_difficile.collidepoint(event.pos):
                        return 'difficile'

def ajouter_mot_interface():
    nouveau_mot = ""
    en_saisie = True
    
    while en_saisie:
        fenetre.fill(BLEU_FONCE)
        # Grille de fond
        for i in range(0, LARGEUR, 20):
            pygame.draw.line(fenetre, (0, 50, 50), (i, 0), (i, HAUTEUR), 1)
        for i in range(0, HAUTEUR, 20):
            pygame.draw.line(fenetre, (0, 50, 50), (0, i), (LARGEUR, i), 1)
            
        texte_instruction = police.render("ENTREZ NOUVELLE SÉQUENCE:", True, CYAN)
        texte_mot = police.render(f">{nouveau_mot}_", True, VERT_MATRIX)
        
        fenetre.blit(texte_instruction, (50, HAUTEUR//2 - 50))
        fenetre.blit(texte_mot, (50, HAUTEUR//2))
        
        # Ajout du bouton retour
        rect_retour = pygame.Rect(50, HAUTEUR - 60, 300, 40)
        pos_souris = pygame.mouse.get_pos()
        couleur_retour = ROUGE_NEON if rect_retour.collidepoint(pos_souris) else VERT_MATRIX
        texte_retour = police.render("RETOUR AU MENU", True, couleur_retour)
        fenetre.blit(texte_retour, (50, HAUTEUR - 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nouveau_mot:
                    return nouveau_mot
                elif event.key == pygame.K_BACKSPACE:
                    nouveau_mot = nouveau_mot[:-1]
                elif event.unicode.isalpha():
                    nouveau_mot += event.unicode.lower()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if rect_retour.collidepoint(event.pos):
                        return ""  # Retour sans ajouter de mot

def demander_nom():
    nom = ""
    while True:
        fenetre.fill(BLEU_FONCE)
        # Grille de fond
        for i in range(0, LARGEUR, 20):
            pygame.draw.line(fenetre, (0, 50, 50), (i, 0), (i, HAUTEUR), 1)
        for i in range(0, HAUTEUR, 20):
            pygame.draw.line(fenetre, (0, 50, 50), (0, i), (LARGEUR, i), 1)
            
        titre = police_titre.render("ENTREZ VOTRE NOM", True, CYAN)
        texte_nom = police.render(f">{nom}_", True, VERT_MATRIX)
        
        fenetre.blit(titre, (LARGEUR//2 - titre.get_width()//2, 100))
        fenetre.blit(texte_nom, (LARGEUR//2 - 100, HAUTEUR//2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nom:
                    return nom
                elif event.key == pygame.K_BACKSPACE:
                    nom = nom[:-1]
                elif event.unicode.isalnum():  # Lettres et chiffres autorisés
                    if len(nom) < 10:  # Limite à 10 caractères
                        nom += event.unicode.upper()

def sauvegarder_score(nom, score, difficulte):
    try:
        with open("scores.json", "r") as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = {"facile": [], "normal": [], "difficile": []}
    
    # Vérifier si le joueur a déjà un meilleur score
    scores_joueur = [s for s in scores[difficulte] if s["nom"] == nom]
    if scores_joueur:
        # Si le nouveau score est meilleur, on met à jour
        if score > scores_joueur[0]["score"]:
            scores[difficulte].remove(scores_joueur[0])
            scores[difficulte].append({"nom": nom, "score": score})
    else:
        # Si c'est le premier score du joueur
        scores[difficulte].append({"nom": nom, "score": score})
    
    # Trier les scores et garder les 10 meilleurs
    scores[difficulte] = sorted(scores[difficulte], key=lambda x: x["score"], reverse=True)[:10]
    
    with open("scores.json", "w") as f:
        json.dump(scores, f)

def afficher_scores():
    try:
        with open("scores.json", "r") as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = {"facile": [], "normal": [], "difficile": []}
    
    while True:
        fenetre.fill(BLEU_FONCE)
        # Grille de fond
        for i in range(0, LARGEUR, 20):
            pygame.draw.line(fenetre, (0, 50, 50), (i, 0), (i, HAUTEUR), 1)
        for i in range(0, HAUTEUR, 20):
            pygame.draw.line(fenetre, (0, 50, 50), (0, i), (LARGEUR, i), 1)
        
        titre = police_titre.render("MEILLEURS SCORES", True, CYAN)
        fenetre.blit(titre, (LARGEUR//2 - titre.get_width()//2, 50))
        
        y = 120
        for mode in ["facile", "normal", "difficile"]:
            texte_mode = police.render(f"MODE {mode.upper()}", True, VERT_MATRIX)
            fenetre.blit(texte_mode, (50, y))
            y += 40
            
            for i, score in enumerate(scores[mode][:5]):  # Afficher top 5
                texte_score = police.render(f"{i+1}. {score['nom']}: {score['score']}", True, CYAN)
                fenetre.blit(texte_score, (70, y))
                y += 30
            y += 20
        
        # Création du rectangle pour le bouton retour
        rect_retour = pygame.Rect(LARGEUR//2 - 150, HAUTEUR - 60, 300, 40)
        
        # Vérification si la souris est sur le bouton
        pos_souris = pygame.mouse.get_pos()
        couleur_retour = ROUGE_NEON if rect_retour.collidepoint(pos_souris) else VERT_MATRIX
        
        texte_retour = police.render("RETOUR AU MENU", True, couleur_retour)
        fenetre.blit(texte_retour, (LARGEUR//2 - texte_retour.get_width()//2, HAUTEUR - 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if rect_retour.collidepoint(event.pos):
                        return

def trier_mots():
    try:
        with open("mots.txt", "r", encoding="utf-8") as fichier:
            mots = fichier.read().splitlines()
            # Enlever les lignes vides
            mots = [mot for mot in mots if mot.strip()]
            # Trier par longueur
            mots_tries = sorted(mots, key=len)
            
        with open("mots.txt", "w", encoding="utf-8") as fichier:
            fichier.write("\n".join(mots_tries))
            
    except FileNotFoundError:
        print("Fichier mots.txt non trouvé")

def main():
    while True:
        choix = menu_principal()
        
        if choix == "scores":
            afficher_scores()
        elif choix == "jouer":
            nom_joueur = demander_nom()
            difficulte = menu_difficulte()
            jeu = JeuPendu(difficulte)
            jeu.charger_mot()
            
            partie_en_cours = True  # Variable pour contrôler la boucle de jeu
            while partie_en_cours:  # Utiliser cette variable au lieu de True
                fenetre.fill(BLEU_FONCE)
                # Grille de fond
                for i in range(0, LARGEUR, 20):
                    pygame.draw.line(fenetre, (0, 50, 50), (i, 0), (i, HAUTEUR), 1)
                for i in range(0, HAUTEUR, 20):
                    pygame.draw.line(fenetre, (0, 50, 50), (0, i), (LARGEUR, i), 1)
                    
                jeu.dessiner_pendu()
                
                # Message système (en bas) - seulement si le jeu est en cours
                if jeu.en_cours:
                    texte_systeme = police.render(jeu.message_systeme, True, CYAN)
                    fenetre.blit(texte_systeme, (20, HAUTEUR - 100))
                
                # Affichage du mot caché
                texte_mot = police.render(jeu.afficher_mot_cache(), True, VERT_MATRIX)
                fenetre.blit(texte_mot, (LARGEUR//2 - texte_mot.get_width()//2, 400))
                
                # Affichage des lettres ratées (remis en haut à gauche)
                if jeu.lettres_ratees:
                    texte_ratees = police.render(f"SÉQUENCES ERRONÉES: {', '.join(sorted(jeu.lettres_ratees))}", True, ROUGE_NEON)
                    fenetre.blit(texte_ratees, (20, 20))
                
                # Affichage du nombre d'erreurs
                texte_erreurs = police.render(f"CORRUPTION: {jeu.erreurs}/{jeu.max_erreurs}", True, ROUGE_NEON if jeu.erreurs > 4 else VERT_MATRIX)
                fenetre.blit(texte_erreurs, (LARGEUR - 250, 20))
                
                if not jeu.en_cours:
                    score = jeu.calculer_score()
                    if score > 0:  # Sauvegarder uniquement si victoire
                        sauvegarder_score(nom_joueur, score, difficulte)
                    if jeu.erreurs >= jeu.max_erreurs:
                        message = f"ÉCHEC - MOT CLÉ: {jeu.mot}"
                    else:
                        message = f"DÉCRYPTAGE RÉUSSI! SCORE: {score}"
                    texte_fin = police.render(message, True, ROUGE_NEON if jeu.erreurs >= jeu.max_erreurs else VERT_MATRIX)
                    fenetre.blit(texte_fin, (LARGEUR//2 - texte_fin.get_width()//2, HAUTEUR - 140))
                    
                    texte_retour = police.render("APPUYEZ SUR ESPACE POUR RETOUR MENU", True, CYAN)
                    fenetre.blit(texte_retour, (LARGEUR//2 - texte_retour.get_width()//2, HAUTEUR - 70))
                
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if jeu.en_cours and event.unicode.isalpha():
                            jeu.verifier_lettre(event.unicode.lower())
                        elif not jeu.en_cours and event.key == pygame.K_SPACE:
                            partie_en_cours = False  # Sortir de la boucle de jeu
        elif choix == "ajouter":
            nouveau_mot = ajouter_mot_interface()
            jeu = JeuPendu()
            jeu.ajouter_mot(nouveau_mot)
            
        elif choix == "quitter":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    trier_mots()
    main() 