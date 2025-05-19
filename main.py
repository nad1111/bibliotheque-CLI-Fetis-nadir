# auteur : fetis nadir
# projet : bibliotheque CLI

import json

# Charger la bibliothèque depuis le fichier JSON
def charger_bibliotheque():
    try:
        with open("bibliotheque.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Sauvegarder la bibliothèque dans un fichier JSON
def sauvegarder_bibliotheque(bibliotheque):
    with open("bibliotheque.json", "w") as f:
        json.dump(bibliotheque, f, indent=4)

# Générer un ID unique basé sur les IDs existants
def generer_id_unique(bibliotheque):
    if not bibliotheque:
        return 1
    return max(livre["ID"] for livre in bibliotheque) + 1

# Afficher tous les livres
def afficher_livres(bibliotheque):
    if not bibliotheque:
        print("📚 La bibliothèque est vide.")
    else:
        for livre in bibliotheque:
            etat = "✅ Lu" if livre["Lu"] else "❌ Non lu"
            note = livre["Note"] if livre["Note"] is not None else "Pas noté"
            print(f'ID: {livre["ID"]} | {livre["Titre"]} - {livre["Auteur"]} ({livre["Année"]}) | {etat} | Note: {note}')

# Ajouter un livre
def ajouter_livre(bibliotheque):
    titre = input("Titre du livre : ").strip()
    auteur = input("Auteur : ").strip()
    try:
        annee = int(input("Année de publication : "))
    except ValueError:
        print("❗ Année invalide. Le livre n'a pas été ajouté.")
        return
    nouveau = {
        "ID": generer_id_unique(bibliotheque),
        "Titre": titre,
        "Auteur": auteur,
        "Année": annee,
        "Lu": False,
        "Note": None
    }
    bibliotheque.append(nouveau)
    print("✅ Livre ajouté avec succès !")

# Supprimer un livre
def supprimer_livre(bibliotheque):
    try:
        id_supp = int(input("ID du livre à supprimer : "))
        for livre in bibliotheque:
            if livre["ID"] == id_supp:
                bibliotheque.remove(livre)
                print("🗑️ Livre supprimé.")
                return
        print("❗ Livre introuvable.")
    except ValueError:
        print("❗ Entrée invalide.")

# Rechercher un livre par mot-clé
def rechercher_livre(bibliotheque):
    mot_cle = input("Mot-clé dans le titre ou l’auteur : ").lower()
    resultats = [l for l in bibliotheque if mot_cle in l["Titre"].lower() or mot_cle in l["Auteur"].lower()]
    if resultats:
        afficher_livres(resultats)
    else:
        print("🔍 Aucun livre trouvé.")

# Marquer un livre comme lu et ajouter une note
def marquer_comme_lu(bibliotheque):
    try:
        id_lu = int(input("ID du livre à marquer comme lu : "))
        for livre in bibliotheque:
            if livre["ID"] == id_lu:
                livre["Lu"] = True
                try:
                    note = float(input("Note sur 10 : "))
                    if 0 <= note <= 10:
                        livre["Note"] = note
                    else:
                        print("❗ La note doit être entre 0 et 10. Note non enregistrée.")
                        livre["Note"] = None
                except ValueError:
                    print("❗ Note invalide. Note non enregistrée.")
                    livre["Note"] = None
                print("📘 Livre marqué comme lu.")
                return
        print("❗ Livre introuvable.")
    except ValueError:
        print("❗ Entrée invalide.")

# Afficher les livres selon leur état lu/non lu
def afficher_filtre(bibliotheque):
    choix = input("Voulez-vous voir les livres 'lus' ou 'non lus' ? ").lower()
    if choix == "lus":
        livres = [l for l in bibliotheque if l["Lu"]]
    elif choix == "non lus":
        livres = [l for l in bibliotheque if not l["Lu"]]
    else:
        print("❗ Choix invalide.")
        return
    afficher_livres(livres)

# Trier les livres selon l'année, l'auteur ou la note
def trier_livres(bibliotheque):
    print("Trier par :")
    print("1. Année")
    print("2. Auteur")
    print("3. Note")
    choix = input("Votre choix : ")
    if choix == "1":
        livres_tries = sorted(bibliotheque, key=lambda x: x["Année"])
    elif choix == "2":
        livres_tries = sorted(bibliotheque, key=lambda x: x["Auteur"].lower())
    elif choix == "3":
        livres_tries = sorted(bibliotheque, key=lambda x: (x["Note"] if x["Note"] is not None else -1), reverse=True)
    else:
        print("❗ Choix invalide.")
        return
    afficher_livres(livres_tries)

# Menu principal de l'application
def menu():
    print("📖 Bienvenue dans la bibliothèque de Nadir !")
    bibliotheque = charger_bibliotheque()
    while True:
        print("\n--- MENU ---")
        print("1. Afficher tous les livres")
        print("2. Ajouter un livre")
        print("3. Supprimer un livre")
        print("4. Rechercher un livre")
        print("5. Marquer un livre comme lu")
        print("6. Afficher les livres lus ou non lus")
        print("7. Trier les livres")
        print("8. Quitter")
        choix = input("Choisissez une option : ")

        if choix == "1":
            afficher_livres(bibliotheque)
        elif choix == "2":
            ajouter_livre(bibliotheque)
        elif choix == "3":
            supprimer_livre(bibliotheque)
        elif choix == "4":
            rechercher_livre(bibliotheque)
        elif choix == "5":
            marquer_comme_lu(bibliotheque)
        elif choix == "6":
            afficher_filtre(bibliotheque)
        elif choix == "7":
            trier_livres(bibliotheque)
        elif choix == "8":
            sauvegarder_bibliotheque(bibliotheque)
            print("💾 Bibliothèque sauvegardée. À bientôt !")
            break
        else:
            print("❗ Choix invalide.")

# Démarrer le programme
if __name__ == "__main__":
    menu()
