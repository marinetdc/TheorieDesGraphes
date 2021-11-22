# ==============================================================================
"""DM GNO : demo program for the 'Frame' widget"""
# ==============================================================================
# __author__  = "Marine Troadec et Marie-Ange Bayeux"
# __version__ = "1.0"
# __date__    = "2019-12-02"
# ------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lecture
import os
class Reseau(object):
    # ----------------------------------------------------------------------------
    def __init__(self, r=[]):
        self.reset()
        if type(r) == list :
            for i in r:       
                if len(i) == 3:       #verifie que la liste est de taille 3 : sommet1, sommet2, poids
                    self.add_node(i[0]) #ajoute le sommet à la liste de sommet
                    self.add_node(i[1]) 
                    self.add_edge(i[0], i[1], i[2])  #Ajoute l'arete       



    def add_edge(self, x: int, y: int, w=1):       
        if (-10 <= w <= 10) and type(x) == int and type(y) == int:       
            a = min(x, y)                   #on fait en sorte que le couple de sommets soit trié dans l'odre croissant
            b = max(x, y)
            p = len(self.__reseau)
            if (a, b) in self.__reseau.keys():       
                if w not in self.__reseau[a, b]:   #si l'arete de poids w n'existe pas il l'ajoute    
                    self.__reseau[a, b].append(w)
                    return True
            else: 
                self.add_node(a)
                self.add_node(b)            
                self.__reseau[a, b] = []      #ajout de a et b dans la liste de sommet puis dans le graphe
                self.__reseau[a, b].append(w)       
                return True
        if p == len(self.__reseau) : return False
        else : return False

    def add_node(self, x: int):       
        if type(x) == int and x >= 0:       
            for i in self.__nodes:       #ajout du sommet dans nodes si il existe pas 
                if i== x:       
                    return False                        
            self.__nodes.append(x)
            self.__nodes.sort()
            return True

    def reset(self):
        self.__reseau = {}    #créé un graphe vide
        self.__nodes = []

    def del_nodes(self):
        self.reset()        #efface tout le graphe

    def del_node(self, x):
        lst = []
        for i in self.__reseau.keys():
            if i[0] == x or i[1] == x :
                lst.append(i)
        for i in lst :
            del self.__reseau[i]          #supprime l'arete
        for i,j in enumerate(self.__nodes) : 
            if j == x :
                del self.__nodes[i]       #supprime le sommet
                break
            
    def del_edges(self):
        self.__reseau = {}      #supprime toutes les aretes

    def del_edge(self,x,y,w=1):
        lst = []
        lst_2 = []
        for i,j in self.__reseau.items():           #parcours le graphe
            if i[0] == x and i[1] == y or i[0] == y and i[1] == x :         #si l'arete est trouvée
                p = 0
                while p < len(j) :
                    if j[p] == w :      #cherche le poids correspondant, sachant qu'il ne peut pas avoir deux fois le meme couple noeud-poids 
                        lst.append(i)   #ajoute toutes les arrete entre ces sommets dans une liste
                        v = 0
                        while v < len(j) :
                            if j[v] != w :
                                lst_2.append((x,y,j[v])) #créé une liste avec les poids à ne pas enlever si aretes multiples
                            v = v+1
                    p = p+1
        if not(lst) : return False
        for i in lst :
            del self.__reseau[i]            #supprime  l'arete entiere
        for i in lst_2 :
            self.add_edge(i[0],i[1],i[2])   #ajoute l'arete sans le poids à enlever 
        return True

    def erase_edge(self,x,y) :
        lst = []            
        for i in self.__reseau.keys() :
            if i[0]==x and i[1] == y or i[0] == y and i[1] == x : #cherche l'arete x,y
                lst.append(i)
        for i in lst :
            del self.__reseau[i]        #supprime toutes les aretes existantes entre les deux sommets
        if not(lst) : return False
        return True 

    @property
    def nbVertices(self):
        return len(self.__nodes)        #retourne le nombre de noeuds

    @property
    def nbEdges(self) :
        nb = 0
        for j in self.__reseau.values() :  
            p = 0
            while p < len(j) :
                nb = nb+1
                p=p+1           #retourne le nombre d'arete
        return nb  

    @property
    def dmin(self):
        lst = self.lst_deg()
        a = lst[self.__nodes[0]]
        for i in lst.keys() :
            if lst[i] < a :
                a = lst[i]
        return a
                                #les fontions retournent respectivement les degres min et max
    @property
    def dmax(self):
        lst = self.lst_deg()
        a = 0
        for i in lst.keys() :
            if lst[i] > a :
                a = lst[i]
        return a

    def lst_deg(self):      #créé un dictionnaire de la forme {sommet : degre}
        self.lst = {}
        for i in self.__nodes : #initialise le dictionnaire {sommet : 0}  chaque sommet est de poids 0
            self.lst[i] = 0
        for i,j in self.__reseau.items():
            if i[0] == i[1] :
                self.lst[i[0]] = self.lst[i[0]]+len(j)*2 #si c'est une boucle ajoute deux fois la longeur de la liste de poids au degré du sommet 
            else :
                self.lst[i[0]]= self.lst[i[0]]+len(j)  #ajoute la longeur de la liste de poids au degré du sommet
                self.lst[i[1]]= self.lst[i[1]]+len(j)
        return self.lst
        
    @property
    def edges(self):
        lst= []
        for i,j in self.__reseau.items() :              #renvoie une liste de toutes les aretes 
            p = 0
            while p<len(j):
                lst.append((i[0],i[1],j[p]))
                p=p+1
        return lst

    @property
    def weight(self):
        p = 0
        for i in self.__reseau.values():  #retourne le poid total du graphe
            for j in i: 
                p = p + j  
        return p 

    def adj(self,x):
        lst = []
        for i in self.__reseau.keys() :
            if i[0] == x :              #retourne la liste d'adjacence de x
                lst.append(i[1])
            if i[1]==x :
                lst.append(i[0])
        lst.sort()                  #tri dans l'ordre croissant
        return lst

    def degre(self,x) :
        lst = {}
        if x not in self.__nodes :      
            return -1
        else :
            lst = self.lst_deg()    #revoie le degre du sommet x
            return lst[x]

    def estSimple(self) :
        for i,j in self.__reseau.items() :      #renvoie true si le graphe n'a pas  :  
            if i[0] == i[1] : return False                                          #d'aretes multiples
            if len(j)>1 : return False                                              #ou de boucles
        return True


    def estComplet(self):
        if not self.estSimple() : return False                  #renvoie true si le graphe et simple et que toutes les aretes sont reliées entre elles
        for i,j in self.__reseau.items():           
            if len(j) != len(self.__nodes)-1 : return False
        return True

    def matrice_adjacence(self):
        mat = [[0 for i in range(len(self.__nodes))] for j in range(len(self.__nodes))]
        if not self.estSimple() :
            for i,j in self.__reseau.items():
                if i[0]==i[1] :                     #si l'arrete est multiple
                    mat[self.__nodes.index(i[0])][self.__nodes.index(i[1])] = len(j)*2      #prend comme valeur 2 * le nombre de poids
                else :
                    mat[self.__nodes.index(i[0])][self.__nodes.index(i[1])] = len(j)        #mat[sommet1][sommet2] = nombre d'arete
                    mat[self.__nodes.index(i[1])][self.__nodes.index(i[0])] = len(j)        #mat[sommet2][sommet1] = nombre d'arete
        else :
            for i in self.__reseau.keys():
                mat[self.__nodes.index(i[0])][self.__nodes.index(i[1])] = 1                 #mat[sommet1][sommet2] = 1 car grpahe simmple
                mat[self.__nodes.index(i[1])][self.__nodes.index(i[0])] = 1                 #mat[sommet2][sommet1] = 1 car grpahe simmple
        return mat

    def matrice_incidence(self):
        nb = self.nbEdges
        mat = [[0 for i in range(nb)] for j in range(len(self.__nodes))]
        if not self.estSimple() :
            p=0
            for i,j in self.__reseau.items():
                if i[0]==i[1] :
                    mat[self.__nodes.index(i[0])][p] = len(j)*2                     #la matrice à la place [sommet][arete] prend 2 * le nombre d'arete 
                else :
                    mat[self.__nodes.index(i[0])][p] = len(j)
                    mat[self.__nodes.index(i[1])][p] = len(j)
                p=p+1
        else :
            p = 0
            for i in self.__reseau.keys():
                mat[self.__nodes.index(i[0])][p] = 1
                mat[self.__nodes.index(i[1])][p] = 1
                p=p+1
        return mat

    def write_to(self):
        fichier = open ("write_to","w")                                                 #ouvre un fichier
        fichier.write(str(self.nbVertices)+ " " + str(self.nbEdges)+ " "+               #ecrit dans le fichier 
                      str(self.dmin)+ " " + str(self.dmax) + "\n" + str(self.edges))
        fichier.close()                                                                 #ferme le fichier 

    def composante(self, x):
        composante=list()
        composante.append(x)
        test=list()
        test.append(x)                  #liste de test
        test2=list()
        adja=list()
        while test != []:
            n=len(test)
            for i in range(n):              #parcours la liste de test             
                adja=self.adj(test[i])      #créé une lsite de sommet adjacents
                m=len(adja)                 
                for j in range(m):          #parcours la liste d'adjacence
                    if composante.count(adja[j])==0: #si le sommet n'a pas encore été ajouté à la lisre composante
                        test2.append(adja[j])       #on va tester plus tard ses adjacences
                        composante.append(adja[j])       #on ajoute le sommet à la liste des composantes
            test=test2
            test2=[]
            composante.sort()
        return composante

    def estConnexe(self):
        x=self.__nodes[0]   
        if len(self.composante(x))==len(self.__nodes) :     #si le nombre de sommets reliés à x est égale au nombre de noeuds du graphe entier
            return True                                         #alors le graphe estConnexe renvoie True
        else : return False

    def cconnexe(self):
        connexe = {}
        for i in self.__nodes :     
            connexe[i]=[]
            connexe[i].append(min(self.composante(i)))  #renvoie le minimum de la liste de composante de i 
        return connexe

    def estEulerien(self):
        if not self.estConnexe() : return False #on verifie que le graphe soit connexe
        lst = []
        lst = self.lst_deg()
        for i in lst :          #on verifie que chaque degré soit pair
            if i%2 == 1 : return False
        return True

    def minimisation(self):
        lst = []
        _stockage = []
        for p in self.__nodes :      
            dico ={}
            for i in self.edges :
                if i[0] == p and i[1] != p or i[1] == p and i[0] != p :
                    c = i[2]
                    if (i[0],i[1]) in dico.keys() :  
                        d = dico[i[0],i[1]]
                        g = d
                        if c < d :
                            dico[i[0],i[1]] = c             #si l'arete existe on regarde si son poids est maximale
                    else:
                        dico[i[0],i[1]] = []
                        dico[i[0],i[1]] = c
            for i,j in dico.items():
                    _stockage.append((i[0],i[1],j))
        for i in _stockage :
            if i not in lst :
                lst.append((i[0],i[1],i[2]))
        return Reseau(lst)

    def maximisation(self):
        lst = []
        _stockage = []
        for p in self.__nodes :         #parcours des sommets
            dico ={}
            for i in self.edges :       #parcours des aretes
                if i[0] == p and i[1] != p or i[1] == p and i[0] != p :     #si le sommet appartient  à l'arete
                    c = i[2]                                                #garde le poids de cette arete
                    if (i[0],i[1]) in dico.keys() :         #regarde si l'arte a deja été ajouté au nouveau dico
                        d = dico[i[0],i[1]]                 
                        g = d
                        if c > d :                          #si l'arete existe on regarde si son poids est maximale
                            dico[i[0],i[1]] = c
                    else:                                   #si l'aretee existe pas deja on la créé
                        dico[i[0],i[1]] = []
                        dico[i[0],i[1]] = c
            for i,j in dico.items():
                    _stockage.append((i[0],i[1],j))     #on stocke les aretes
        for i in _stockage :                        
            if i not in lst :
                lst.append((i[0],i[1],i[2]))            #on créé une liste des aretes 
        return Reseau(lst)

    def estArbre(self):
        if self.estConnexe and self.nbVertices == self.nbEdges - 1 : # verifie si c'est un arbre (connexe et |V| = |E|-1)
            return True

    def minimal_subtree(self) :
        if self.estConnexe() :
            lst_edges = self.edges
            lst_sg = []
            lst_edges.sort(key=lambda colonnes: colonnes[2])        #on trie les aretes par ordre croissant de poids
            min_subtree = Reseau()
            for i in self.__nodes :                     #on créé un reseau de sommets 
                min_subtree.add_node(i)
            for i in lst_edges :
                if i[1] not in min_subtree.composante(i[0]):    #si la composante connexe n'existe pas encore dans le nouveau grpahe
                    min_subtree.add_edge(i[0],i[1],i[2])        #on l'ajoute
            return min_subtree
        else :
            return None

    def maximal_subtree(self) :
        if self.estConnexe() :
            lst_edges = self.edges
            lst_sg = []
            lst_edges.sort(reverse = True, key=lambda colonnes: colonnes[2])        #on trie les artes par ordre decroissant de poids
            min_subtree = Reseau()
            for i in self.__nodes :
                min_subtree.add_node(i)
            for i in lst_edges :
                if i[1] not in min_subtree.composante(i[0]):
                    min_subtree.add_edge(i[0],i[1],i[2])
            return min_subtree
        else :
            return None
        

    def read_from(self) :
        _d = {1: "graphe.txt", 2: "bad_file.txt", 3: "good_file.txt"}
        print("""Pour tester la lecture choisissez

    1/ fichier sans erreur
    2/ fichier plein d'erreurs
    3/ fichier avec quelques erreurs
    
                  """)
        try:
            choix = int(input("votre choix ? "))
            print("votre choix est {}".format(_d[choix]))
            print("Le résultat du traitement renvoie\n\t {}"
                  .format(lecture.read_validate(_d[choix])))
            return self.__init__(lecture.read_validate(_d[choix]))
        except Exception as _e:
            print(_e)
            
    def __str__(self) :
        r =""
        for i in self.__reseau.items():
            r+=str(i)
            r+="\n"
        r+="\n"
        return r

    def __repr__(self):
        return ("{0}({1.nbVertices}, {1.nbEdges})"
                "".format(self.__class__.__name__, self))
    
if __name__ == "__main__":
    g = Reseau()
##    g.add_edge(1, 2, 3) # True
##    g.add_edge(3, 2 -1) # True
##    g.add_edge(4, 2) # True
##    g.add_edge(2, 1, 3)# False
##    h=g.minimal_subtree()
##    g.nbVertices # 4
##    g.nbEdges # 3
##    g.dmin # 1
##    g.dmax # 3
##    g.edges # [(1, 2, 3), (2, 3, -1), (2, 4, 1)]
##    g.weight # 3
##    g.del_edge(2, 4, -1) # False
##    g.nbEdges # 3
##    g.del_edge(2, 4) # True
##    g.nbEdges # 2
##    g.add_edge(2, 4) # True
##    g.add_edge(2, 5) # True
##    g.add_node(5) # False
##    g.add_node(7) # True
##    g.add_edge(2, 3, -5) # True
##    g.add_edge(2, 3, 3) # True
##    g.dmin # 0
##    g.dmax # 6
##    g.nbVertices # 6
##    g.nbEdges # 6
##    g.edges # [(1, 2, 3), (2, 3, 3), (2, 3, -5), (2, 3, -1), (2, 4, 1), (2, 5, 1)]
##    g.degre(2) # 6
##    g.add_edge(2, 2, 7) # True
##    g.degre(2) # 8 
##    g.composante(1) # [1, 2, 3, 4, 5]
##    g.adj(1) # [2]
##    g.cconnexe() # {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 7: 7} 
##    g.estConnexe() # False
##    g.degre(4) # 1
##    g.dmin # 0
##    g.degre(5) # 1
##    g.add_edge(4, 6, 10) # True
##    g.add_edge(5, 8, 3) # True
##    g.add_edge(6, 7, -7) # True
##    g.add_edge(7, 8, -2) # True
##    g.nbVertices # 8
##    g.nbEdges # 11
##    g.dmin # 1
##    g.dmax # 8
##    g.weight # 13
##    g.estSimple() # False
##    g.estEulerien() # True
##    g.estConnexe() # True
##    min_tree = g.minimal_subtree()
##    min_tree.weight # -6
##    min_tree.nbVertices # 8
##    min_tree.nbEdges # 7
##    min_tree.estSimple() # True
##    min_tree.estEulerien() # False
##    min_tree.estConnexe() # True
##    max_tree = g.maximal_subtree()
##    max_tree.weight # 19
##    max_tree.nbVertices # 8
##    max_tree.nbEdges # 7
##    max_tree.estSimple() # True
##    max_tree.estEulerien() # False
##    max_tree.estConnexe() # True
##    mini = g.minimisation()
##    mini.estSimple() # True
##    mini.nbVertices # 8
##    mini.nbEdges # 8
##    mini.weight # 4
##    mini.edges # [(1, 2, 3), (2, 3, -5), (2, 4, 1), (2, 5, 1), (4, 6, 10), (5, 8, 3), (6, 7, -7), (7, 8, -2)]
##    maxi = g.maximisation()
##    maxi.estSimple() # True
##    maxi.nbVertices # 8
##    maxi.nbEdges # 8
##    maxi.weight # 12
##    maxi.edges # [(1, 2, 3), (2, 3, 3), (2, 4, 1), (2, 5, 1),(4, 6, 10), (5, 8, 3), (6, 7, -7), (7, 8, -2)]
##    g.nbVertices # 8
##    g.nbEdges # 11
##    g.weight # 13
##    g.edges # [(1, 2, 3), (2, 2, 7), (2, 3, 3), (2, 3, -5), (2, 3, -1), (2, 4, 1), (2, 5, 1), (4, 6, 10), (5, 8, 3), (6, 7, -7), (7, 8, -2)]
##    maxi.matrice_adjacence()
##    g.matrice_adjacence()
##    maxi.matrice_incidence()
##    g.matrice_incidence()
##    g.add_edge(2,3,-1)

## ---------------------------------------------------------------------------
