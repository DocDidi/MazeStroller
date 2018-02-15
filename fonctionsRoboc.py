#! /usr/bin/env python3
# coding: utf-8

import os, glob, pickle, sys, time
from var import *
from Joueur import *
from Mur import *
from Porte import *
from Couloir import *

def effaceEtAffiche(*valeur):
    """Efface l'écran et positionne le curseur en haut a gauche."""
    if SYSTEME_D_EXPLOITATION == 'nt':
        os.system('cls')
        if valeur:
            print(valeur[0])
    else:
        print(EFFACE_ECRAN)
        if valeur == ():
            print(RESET_CURSEUR, end = "")
        else:
            print(RESET_CURSEUR + WHITE_TEXT + valeur[0])

def verifTailleConsole(Hauteur):
    HAUTEURECRANCORRECT = True
    rows, columns = os.popen('stty size', 'r').read().split()
    while int(rows) < Hauteur + 3:
        HAUTEURECRANCORRECT = False
        rows, columns = os.popen('stty size', 'r').read().split()
        effaceEtAffiche(MESSAGEHAUTEURECRANINCORRECT)
    if HAUTEURECRANCORRECT == False:
        effaceEtAffiche(MESSAGEHAUTEURECRANCORRECT)
        input()

def afficheLaby(Joueur, Props, Hauteur):
    """Affiche le labyrinthe"""
    for item in Props:
        print(item)
    print(Joueur)

def repriseSauvegarde():
    """Propose de reprendre la partie précedente"""
    if os.path.exists(FICHIERDESAUVEGARDE):
        print(WHITE_TEXT + MESSAGEREPRISESAUVEGARDE)
        choix = capturesaisie()
        if choix.lower() == "o":
            with open(FICHIERDESAUVEGARDE, "rb") as Sauvegarde:
                PartieEnCours = pickle.loads(Sauvegarde.read())
        else:
            os.remove(FICHIERDESAUVEGARDE)
            PartieEnCours = False
    else:
        PartieEnCours = False
    return (PartieEnCours)

def sauvegarde(Joueur, Props, Hauteur):
    """Sauvegarde la partie"""
    with open(FICHIERDESAUVEGARDE, "wb") as Sauvegarde:
        Sauvegarde.write(pickle.dumps((Joueur, Props, Hauteur)))

def choixlaby():
    """Menu de selection des cartes"""
    contenu = glob.glob(EMPLACEMENTCARTES)
    if not contenu:
        print(WHITE_TEXT = MESSAGEERREURDOSSIER.format(EMPLACEMENTCARTES))
        exit()
    chemin = EMPLACEMENTCARTES.find("*")
    chosen = False
    selected = 0
    while not chosen:
        effaceEtAffiche(MESSAGECHOIXCARTE)
        for i, carte in enumerate(contenu):
            if i == selected:
                print(BLACK_ON_WHITE + "{0} - {1}"\
                .format(i+1, carte[chemin:-4].capitalize()))
            else:
                print(WHITE_TEXT + "{0} - {1}"\
                .format(i+1, carte[chemin:-4].capitalize()))
        print(WHITE_TEXT + "\nQ - Quitter")
        noinput = True
        while noinput:
            x=capturesaisie()
            if x == CTRL_C:
                exit()
            if ord(x) == 13:
                chosen = contenu[selected]
                noinput = False
            if x == ECHAP_CARAC:
                import termios, tty
                orig_settings = termios.tcgetattr(sys.stdin)
                tty.setraw(sys.stdin)
                y=sys.stdin.read(2)
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
                x = x+y
            if x==FLECHE_BAS:
                if selected < (len(contenu)-1):
                    selected += 1
                noinput = False
            elif x==FLECHE_HAUT:
                if selected > 0:
                    selected -= 1
                noinput = False
            elif x.lower()=='q':
                exit()
    if os.path.exists(chosen):
        return chosen
    else:
        print(WHITE_TEXT + MESSAGEERREURCHOIXCARTE)
        exit()

def labyload(fichier):
    """Charge la carte selectionnée"""
    if os.path.exists(fichier):
        with open(fichier, "r") as carte:
            return carte.read()

def labymap(carte):
    """Converti la carte (str) en données du jeu"""
    lines = carte.split("\n")
    Props = []
    Murs = []
    Portes = []
    Couloirs = []
    for i, line in enumerate(lines):
        for j, letter in enumerate(line):
            if letter is LETTREJOUEUR:
                Joueur = Personnage(i,j)
                Props.append(Couloir(i,j))
            elif letter is LETTREFIN:
                Props.append(Porte(i,j,fin = True))
            elif letter is LETTREPORTE:
                Props.append(Porte(i,j))
            elif letter is LETTREMURS:
                Props.append(Mur(i,j))
            else:
                Props.append(Couloir(i,j))

    try:
        return(Joueur, Props, i)
    except:
        return labymap(CARTEDEFAUT)

def playermove(Joueur, Props, LabyOn, Hauteur):
    """Fait bouger le joueur"""
    noinput = True
    print(WHITE_TEXT + MESSAGEDEMANDEMOUVEMENT.format(Hauteur + 2))
    TestPosJoueur = [Joueur.y, Joueur.x]
    while noinput:
        x=capturesaisie()
        if x == CTRL_C:
            exit()
        if x == ECHAP_CARAC:
            import termios, tty
            orig_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin)
            y=sys.stdin.read(2)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
            x = x+y
        if x==FLECHE_HAUT:
            TestPosJoueur = [Joueur.y-1,Joueur.x]
            noinput = False
        elif x==FLECHE_BAS:
            TestPosJoueur = [Joueur.y+1,Joueur.x]
            noinput = False
        elif x==FLECHE_DROITE:
            TestPosJoueur = [Joueur.y,Joueur.x+1]
            noinput = False
        elif x==FLECHE_GAUCHE:
            TestPosJoueur = [Joueur.y,Joueur.x-1]
            noinput = False
        elif x.lower()=='q':
            noinput =  LabyOn = False

    bloc = False

    for item in Props:
        if (TestPosJoueur[1], TestPosJoueur[0]) == (item.x, item.y)\
        and item.bloc == True:
            bloc = True

    if bloc == False:
        Joueur.x = TestPosJoueur[1]
        Joueur.y = TestPosJoueur[0]

    return (LabyOn)

def capturesaisie():
    """Renvoie la touche de clavier pressée"""
    if SYSTEME_D_EXPLOITATION == 'nt':
        import keyboard
        saisie = keyboard.read_hotkey()
        if saisie == "up":
            saisie = FLECHE_HAUT
        elif saisie == "down":
            saisie = FLECHE_BAS
        elif saisie == "right":
            saisie = FLECHE_DROITE
        elif saisie == "left":
            saisie = FLECHE_GAUCHE
        keyboard.clear_all_hotkeys()
        return saisie

    else:
        import termios, tty
        orig_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        saisie=sys.stdin.read(1)[0]
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    return saisie

def islit(sujet, Joueur):
    """Calcule si l'objet est éclairé"""
    if ((-1 <= Joueur.x - sujet.x <= 1) and (-2 <= Joueur.y - sujet.y <= 2)) or\
    ((-2 <= Joueur.x - sujet.x <= 2) and (-1 <= Joueur.y - sujet.y <= 1)):
        sujet.revealed = True
        sujet.lit = True
    else:
        sujet.lit = False

def brouillard(Joueur, Props):
    """Liste les choses à reveler"""
    for item in Props:
        islit(item, Joueur)
