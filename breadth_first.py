import pygame
from collections import deque



taille =500
fenetre= pygame.display.set_mode((taille,taille))
pygame.display.set_caption("Largeur d'abord")

vide=(254, 254, 223)
mur=(47, 72, 88)
c_debut=(0,0,0)
c_fin=(0, 107, 96)
chemin=(217, 162, 58)
c_voisins=(76, 252, 225)

class Noeud:
    def __init__(self, ligne, colonne, taille, lignes):
        self.ligne=ligne
        self.colonne=colonne
        self.i=ligne*taille
        self.j=colonne*taille
        self.couleur=vide
        self.voisins=[]
        self.taille=taille
        self.lignes=lignes
    
    def get_position(self):
        return self.ligne,self.colonne
    
    def get_couleur(self):
        return self.couleur
    
    def set_couleur(self, couleur):
        self.couleur=couleur

    def draw(self,fenetre):
        pygame.draw.rect(fenetre,self.couleur,(self.i,self.j,self.taille,self.taille))

    def maj_voisins(self,grille):
        if self.ligne < self.lignes-1 and grille[self.ligne+1][self.colonne].get_couleur()!=mur:
            self.voisins.append(grille[self.ligne+1][self.colonne])
        if self.ligne>0 and grille[self.ligne-1][self.colonne].get_couleur()!=mur:
            self.voisins.append(grille[self.ligne-1][self.colonne])
        if self.colonne<self.lignes-1 and grille[self.ligne][self.colonne+1].get_couleur()!=mur:
            self.voisins.append(grille[self.ligne][self.colonne+1])
        if self.colonne>0 and grille[self.ligne][self.colonne-1].get_couleur()!=mur:
            self.voisins.append(grille[self.ligne][self.colonne-1])
        

def _grille(lignes, taille):
    grille=[]
    taille_noeud=taille//lignes
    for i in range(lignes):
        grille.append([])
        for j in range(lignes):
            noeud= Noeud(i,j,taille_noeud,lignes)
            grille[i].append(noeud)
    return grille

def draw_grille(fenetre,lignes,taille):
    taille_noeud=taille//lignes
    for i in range(lignes):
        pygame.draw.line(fenetre,(0,0,0),(0,i*taille_noeud), (taille, i*taille_noeud))
        for j in range(lignes):
            pygame.draw.line(fenetre,(0,0,0),(j*taille_noeud,0), (j*taille_noeud,taille))

def draw(fenetre,grille,lignes,taille):
    fenetre.fill(vide)
    for ligne in grille:
        for noeud in ligne:
            noeud.draw(fenetre)
    draw_grille(fenetre,lignes,taille)
    pygame.display.update()

def position_souris(pos, lignes, taille):
    taille_noeud=taille//lignes
    i,j=pos
    ligne=i//taille_noeud
    colonne=j//taille_noeud

    return ligne,colonne

def reconstruire_chemin(CLOSED,courrant,draw):
    while courrant in CLOSED:
        
        courrant=CLOSED[courrant]
        courrant.set_couleur(chemin)
        
        draw()



def breadth_first(draw,grille,debut,fin):
    OPEN=deque([])
    trouve = False
    CLOSED={}
    if debut == fin :
        trouve=True
    else:
        for noeud in debut.voisins:
            if noeud.get_couleur()!=c_voisins:
                OPEN.appendleft(noeud)
                noeud.set_couleur(c_voisins)
    while OPEN and not trouve:
        courrant=OPEN.pop()
        if courrant==fin:
            trouve=True
            
        else:
            for noeud in courrant.voisins:
                if noeud.get_couleur()!=c_voisins :
                    OPEN.appendleft(noeud)
                    noeud.set_couleur(c_voisins)
                    CLOSED[noeud]=courrant
        
        draw()

    if courrant==fin:
        reconstruire_chemin(CLOSED,fin,draw)
    debut.set_couleur(c_debut)
    fin.set_couleur(c_fin)
        
    
 



def main():
    lignes=20
    grille=_grille(lignes,taille)
    run=True
    debut=None
    fin=None
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            
            if pygame.mouse.get_pressed()[0]: 
                pos=pygame.mouse.get_pos()
                ligne, colonne=position_souris(pos,lignes,taille)
                noeud=grille[ligne][colonne]
                if not debut and noeud != fin:
                    debut=noeud
                    debut.set_couleur(c_debut)
                
                elif not fin and noeud!=debut:
                    fin=noeud
                    fin.set_couleur(c_fin)
                elif noeud!=debut and noeud!=fin:
                    noeud.set_couleur(mur)
            if pygame.mouse.get_pressed()[2]: 
                pos=pygame.mouse.get_pos()
                ligne, colonne=position_souris(pos,lignes,taille)
                noeud=grille[ligne][colonne]
                noeud.set_couleur(vide)
                if noeud==debut:
                    debut=None
                if noeud == fin:
                    fin= None
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and debut and fin:
                    for ligne in grille:
                        for noeud in ligne:
                            noeud.maj_voisins(grille)
                    breadth_first(lambda: draw(fenetre,grille,lignes,taille),grille,debut,fin)


        draw(fenetre,grille,lignes,taille)
    pygame.quit()

if __name__ == "__main__":
    main()
