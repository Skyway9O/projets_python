
import random
from tkinter import *


#variables globales
cases = [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]

line_0 = ["-", "-", "-"]
line_1 = ["-", "-", "-"]
line_2 = ["-", "-", "-"]
signe_tour = random.choice([True, False])
tour_de_jeu = 1
point_croix = 0
point_rond = 0


#correspondance = {0 : line_0, 1 : line_1, 2 : line_2}

def afficher_element_clavier(event):
    global cases, tour_de_jeu, signe_tour, champ_saisi
    texte_champ = str(champ_saisi.get())
    texte_champ_saisi = texte_champ.split(",")
    l = int(texte_champ_saisi[0])
    c = int(texte_champ_saisi[1])
    champ_saisi.delete(0,END)
    afficher_element(l, c)


def coord_souris(event):
    l = (event.y)//100                    # Ligne du clic
    c = (event.x)//100                    # Colonne du clic
    afficher_element(l, c)


def afficher_element(l, c):
    global cases, tour_de_jeu, signe_tour
    if (tour_de_jeu < 10) and (cases[l][c] == 0):
        if signe_tour:
            canvas.create_line(100*c+8, 100*l+8, 100*c+96, 100*l+96, width = 5, fill = "blue")
            canvas.create_line(100*c+8, 100*l+96, 100*c+96, 100*l+8, width = 5, fill = "blue")
            cases[l][c] = 1
            message.configure(text=" de jouer", image= image_rond, compound=LEFT)
            
        else:
            canvas.create_oval(100*c+8, 100*l+8, 100*c+96, 100*l+96, width = 5, outline = "red")
            cases[l][c] = -1
            message.configure(text=" de jouer", image = image_croix, compound=LEFT)

        signe_tour = not(signe_tour)
        if (tour_de_jeu >= 5) and (tour_de_jeu <= 9):
            somme = verif(cases)
            if somme == 1 or somme == -1:
                tour_de_jeu = gagner(somme)
            elif tour_de_jeu == 9:
                tour_de_jeu = gagner(0)
        tour_de_jeu += 1


def renit():
    global cases, tour_de_jeu, signe_tour
    cases = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]
    signe_tour = random.choice([True, False])
    tour_de_jeu = 1

    message.configure(text=" de jouer" if signe_tour == True else " de jouer", image=(image_croix if signe_tour == True else image_rond), compound=LEFT)
    canvas.delete(ALL)      # Efface toutes les figures

    lignes = []
    for i in range(4):
        lignes.append(canvas.create_line(0, 100*i+2, 303, 100*i+2, width=3))
        lignes.append(canvas.create_line(100*i+2, 0, 100*i+2, 303, width=3))
    
    lignes.append(sous_canvas.create_line(20, 18, 40, 38, width=3, fill = "blue"))
    lignes.append(sous_canvas.create_line(20, 38, 40, 18, width=3, fill = "blue"))
    lignes.append(sous_canvas.create_oval(243, 18, 263, 38, width = 3, outline = "red"))

def verif(cases):
    """ Entrées : toutes las cases
        Sorties : Calcule les sommes de chaque ligne/colonne/diagonale
            et vérifie l'alignement."""
    sommes = [0,0,0,0,0,0,0,0]             # Il y a 8 sommes à vérifier
    # Les lignes :
    sommes[0] = sum(cases[0])
    sommes[1] = sum(cases[1])
    sommes[2] = sum(cases[2])
    # Les colonnes
    sommes[3] = cases[0][0]+cases[1][0]+cases[2][0]
    sommes[4] = cases[0][1]+cases[1][1]+cases[2][1]
    sommes[5] = cases[0][2]+cases[1][2]+cases[2][2]
    # Les diagonales
    sommes[6] = cases[0][0]+cases[1][1]+cases[2][2]
    sommes[7] = cases[0][2]+cases[1][1]+cases[2][0]

    for i in range(8):                     # Parcours des sommes
        if sommes[i] == 3:
            return 1
        elif sommes[i] == -3:
            return -1
    return 0
   
def gagner(a):
    global point_croix, point_rond
    if a == 1:
        message.configure(text = " ont gagné !", image = image_croix, compound=LEFT)
        point_croix += 1
        point_croix_message.configure(text = point_croix)
    elif a == -1:
        message.configure(text = " ont gagné !", image = image_rond, compound=LEFT)
        point_rond += 1
        point_rond_message.configure(text = point_rond)
    elif a == 0:
        message.configure(text = "Match nul !", image=image_rien )
    return 9
    

#création de la fenêtre
fenetre = Tk()
fenetre.title("Morpion")
fenetre.geometry("500x500")
fenetre.minsize(500, 450)


image_croix = PhotoImage(file="NSI\morpion\croix_morpion.png")
image_rond = PhotoImage(file="NSI/morpion/rond_morpion.png")
image_rien = PhotoImage(file="NSI/morpion/image_vide.png")

#crée une frame
frame = Frame(fenetre)

#afficher le tour de jeu
message = Label(frame, text="Aux croix de jouer" if signe_tour == True else "Aux ronds de jouer", font=("Helvetica, 15"))
message.grid(row = 1, column = 0, columnspan=2, padx=3, pady=3, sticky = W+E)

#crée le canvas
canvas=Canvas(frame, width=301, height=301)
canvas.grid(row = 2, column = 0, columnspan=2)

#crée un autre canvas
sous_canvas = Canvas(frame, width=300, height=50)
sous_canvas.grid(row = 0, column = 0, columnspan=2)

#afficher les scores
point_croix_message = Label(frame, text=": {}".format(point_croix), font=("Helvetica, 17"))
point_rond_message = Label(frame, text=": {}".format(point_rond), font=("Helvetica, 17"))
point_croix_message.grid(row=0, column=0)
point_rond_message.grid(row= 0, column = 1)

#crée des bouton
bouton_reload = Button(frame, text="Recommencer", font=("Helvetica, 13"), command=renit)
bouton_reload.grid(row=4, column=0, sticky = W+E, padx=10, pady=5)

bouton_quitter = Button(frame, text="Quitter", font=("Helvetica, 13"), command=fenetre.destroy)
bouton_quitter.grid(row=4, column=1, sticky = W+E, padx=10, pady=5)

#pack la frame
frame.pack(expand=YES )

#texte et champ de saisi pour palcer le pion
texte_saisi = Label(frame, text="Entrez le coup ou cliquez sur \nla case que vous voulez jouer: ", font=("Helvetica, 14"))
texte_saisi.grid(row=3, column=0)

champ_saisi = Entry(frame, bd = 1, font=("Helvetica, 12"), justify=CENTER)
champ_saisi.grid(row=3, column=1)

#récupère les événement de la souris
canvas.bind("<Button-1>", coord_souris)
champ_saisi.bind("<Return>", afficher_element_clavier)

#programme principale
renit()
fenetre.mainloop()


