########################################################################################################
### IMPORTATIONS
########################################################################################################

from os import listdir
from os.path import isfile, join, isdir
import sys, time, pygame, random, webbrowser, filetype, csv
from numpy.core.fromnumeric import sort

########################################################################################################
### FONCTIONS
########################################################################################################


def pos_curseur(x):
    """Cette fonction renvoie la position du curseur."""
    if x < 15:
        return 15
    
    elif x > 215:
        return 215
    
    else:
        return x


def save_csv():
        """Cette fonction modifie le fichier csv "tab_score".
        La colonne "Score" doit etre remplie que de valeurs convertibles en nombres entiers."""
        global text_entree_nom
        print("text :", text_entree_nom)
        file = open(chemin_programme + "file_csv.csv","r",newline='')
        myReader = csv.DictReader(file)
        tab = []
        for ligne in myReader:
            tab.append([ligne["Nom"],int(ligne["Score"])])
        tab.append([text_entree_nom + " " * (18-len(text_entree_nom)-len(str(score))),score])
        tab.sort(key = lambda x: x[1], reverse=True)
        print(tab)
        tab_2 = [["Nom","Score"]]
        for ligne in tab:
            tab_2.append(ligne)
        
        file = open(chemin_programme + "file_csv.csv","w",newline='')
        
        writer = csv.writer(file)
        for ligne in tab_2:
            writer.writerow([ligne[0],ligne[1]])
        file = open("C:/Users/kylia/OneDrive/Documents/test4.csv","r",newline='')
        myReader = csv.DictReader(file)


def quitter():
    global var_bouton_parametre,text_entree_nom, fond, var_musique, test_save_csv
    
    rang_curseur = len(text_entree_nom)
    last_move_ticks = -201
    var_parametre_clicked = False
    last_pos_ticks = -100
    ticks = pygame.time.get_ticks()
    while True:
        for evenement in pygame.event.get():
            keys = pygame.key.get_pressed()
            #parametres
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                x,y = evenement.pos
                if x >= 0 and y >= 715 and x <= 75 and y <= 780:
                    if var_parametre_clicked == False : var_parametre_clicked = True
                    elif var_parametre_clicked == True : var_parametre_clicked = False
                if x >= 0 and y >= 675 and x <= 230 and y <= 711 and var_parametre_clicked == True:
                    new_x = pos_curseur(x)
                    rect_curseur_parametre.center = new_x,693.5
                    volume = (new_x - 15) / 200
                    pygame.mixer.music.set_volume(volume)

                if x >= 0 and y >= 615 and x <= 230 and y <= 651 and var_parametre_clicked == True:
                    new_x = pos_curseur(x)
                    rect_curseur_parametre2.center = new_x,633.5
                    volume = (new_x - 15) / 200
                    swoosh.set_volume(volume)
                if x >= 40 and y >= 532 and x <= 60 and y <= 562 and var_parametre_clicked == True:
                    if fond == 0:
                        fond = len(sprites_fonds)-1
                    else:
                        fond -= 1

                if x >= 172 and y >= 532 and x <= 192 and y <= 562 and var_parametre_clicked == True:
                    if fond == len(sprites_fonds)-1:
                        fond = 0
                    else:
                        fond += 1

                if x >= 46 and y >= 475 and x <= 66 and y <= 505 and var_parametre_clicked == True:
                    if var_musique == 0:
                        var_musique = len(musique)-1
                    else:
                        var_musique -= 1

                    pygame.mixer.music.load(musique[var_musique]["musique"])
                    pygame.mixer.music.play(-1, 0.0)

                if x >= 166 and y >= 475 and x <= 186 and y <= 505 and var_parametre_clicked == True:
                    if var_musique == len(musique)-1:
                        var_musique = 0
                    else:
                        var_musique += 1 


                    pygame.mixer.music.load(musique[var_musique]["musique"])
                    pygame.mixer.music.play(-1, 0.0)

                if x >= 400 and y >= 300 and x <= 470 and y <= 345:
                    last_pos_ticks = ticks

            #test fermeture programme
            if evenement.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                sys.exit()

            #zone texte
            elif keys[pygame.K_LEFT] and rang_curseur > 0:
                rang_curseur -= 1
                last_move_ticks = pygame.time.get_ticks()

            elif keys[pygame.K_RIGHT] and rang_curseur < len(text_entree_nom):
                rang_curseur += 1
                last_move_ticks = pygame.time.get_ticks()

            elif keys[pygame.K_BACKSPACE] and rang_curseur > 0:
                text_entree_nom = text_entree_nom[0:rang_curseur-1] + text_entree_nom[rang_curseur:len(text_entree_nom)]
                rang_curseur -= 1
            elif keys[pygame.K_RETURN] or ticks - last_pos_ticks <= 100:
                save_csv()
                menu()
            elif evenement.type == pygame.KEYDOWN and keys[pygame.K_BACKSPACE] == False and keys[pygame.K_DELETE] == False and keys[pygame.K_TAB] == False and len(text_entree_nom) < 15:
                len_precedent = len(text_entree_nom)
                text_entree_nom = text_entree_nom[0:rang_curseur] + evenement.unicode + text_entree_nom[rang_curseur:len(text_entree_nom)]
                if len_precedent < len(text_entree_nom):
                    rang_curseur += 1
        
        rect_curseur_entree_nom.topleft = 408 + 22 * rang_curseur ,205

        screen.blit(sprites_fonds[fond],rect_fond)
        screen.blit(sprite_parametre[var_bouton_parametre],rect_bouton_parametre)
        text_surface_score = myfont.render(str(score), False, (230, 230, 230))
        screen.blit(text_surface_score,(1100,100))
        if var_parametre_clicked == True:
            screen.blit(sprite_barre_parametre,rect_barre_parametre)
            screen.blit(sprite_curseur_parametre,rect_curseur_parametre)
            screen.blit(sprite_texte_musique,rect_texte_musique)
            screen.blit(sprite_barre_parametre,rect_barre_parametre2)
            screen.blit(sprite_curseur_parametre,rect_curseur_parametre2)
            screen.blit(sprite_texte_sons,rect_texte_sons)
            screen.blit(sprites_fonds_mini[fond],rect_fond_mini)
            screen.blit(sprite_flèche_gauche,rect_flèche_fond_gauche)
            screen.blit(sprite_flèche_droite,rect_flèche_fond_droite)
            screen.blit(musique[var_musique]["image"],rect_musique)
            screen.blit(sprite_flèche_gauche,rect_flèche_3_gauche)
            screen.blit(sprite_flèche_droite,rect_flèche_3_droite)
        screen.blit(sprite_barre_entree_nom,rect_barre_entree_nom)
        text_surface_entree_nom = myfont3.render(text_entree_nom, False, (230, 230, 230))
        screen.blit(text_surface_entree_nom,(410,208))
        ticks=pygame.time.get_ticks()
        if ticks // 700 % 2 == 0 or ticks - last_move_ticks <= 200:
            screen.blit(sprite_curseur_entree_nom,rect_curseur_entree_nom)
        
        if ticks - last_pos_ticks <= 100:
            text_surface_bouton_valider = myfont4.render("Ok", False, (75,75,75))
        else:
            text_surface_bouton_valider = myfont4.render("Ok", False, (240,240,240))
        screen.blit(text_surface_bouton_valider,(416,316))
        
        
        pygame.display.flip()
    

def game():
    

    def victoire():
        """Affiche l'écran de victoire"""
        screen.blit(sprite_victoire,rect_victoire)
        


    def defaite():
        """Affiche l'écran de défaite"""
        screen.blit(sprite_defaite,rect_defaite)
    
    
        

    def None_list_generator():
        """
        Cette fonction créer une liste contenant toutes les cases ayant pour valeur None.

        """

        for i in range(4):
            for j in range(4):
                if tab_sprite[i][j][0] == None:
                    None_list.append([i,j])


    def random_spawn():
        """Cette fonction change la valeur d'une case None au hasard en 2 (90% des cas) ou 4 (10% des cas)"""
        new = random.choice(None_list)
        if random.randint(1,100) < 11 :
            tab_sprite[new[0]][new[1]] = ordre_sprite[2]
        else:
            tab_sprite[new[0]][new[1]] = ordre_sprite[1]
    

    def up_move():
        global score, test_save_csv
        """Cette fonction effectue les modifications d'un mouvement vers le haut."""
        nonlocal test_changement,test_victoire
        for j in range(4):
            for i in range(3):
                test_fusion = 0
                for k in range(i+1,4):
                    if tab_sprite[i][j][0] == None:
                        if tab_sprite[k][j][0] != None:
                            tab_sprite[i][j] = tab_sprite[k][j]
                            tab_sprite[k][j] = ordre_sprite[0]
                            test_changement = 1   
                    elif test_fusion == 0:
                        if tab_sprite[k][j][0] != None:
                            if tab_sprite[k][j][0] == tab_sprite[i][j][0]:
                                score += 2 ** (ordre_sprite[tab_sprite[i][j][1]][1] + 1)
                                
                                tab_sprite[i][j] = ordre_sprite[tab_sprite[i][j][1]+1]
                                tab_sprite[k][j] = ordre_sprite[0]
                                test_changement = 1
                                if tab_sprite[i][j][0] == valeur_max[mode] and test_victoire == 0:
                                    print(test_victoire)
                                    test_victoire = 1
                                    if test_save_csv == False:
                                        test_save_csv = True
                                test_fusion = 1
                                continue
                            
                            elif i < k-1:
                                tab_sprite[i+1][j] = tab_sprite[k][j]
                                tab_sprite[k][j] = ordre_sprite[0]
                                test_changement = 1
                                break  
                            else:
                                break
                            

    def down_move():
        global score, test_save_csv
        """Cette fonction effectue les modifications d'un mouvement vers le bas."""
        nonlocal test_changement, test_victoire
        for j in range(4):
            for i in range(3,0,-1):
                test_fusion = 0
                for k in range(i-1,-1,-1):
                    if tab_sprite[i][j][0] == None:
                        if tab_sprite[k][j][0] != None:
                            tab_sprite[i][j] = tab_sprite[k][j]
                            tab_sprite[k][j] = ordre_sprite[0]
                            test_changement = 1   
                    elif test_fusion == 0:
                        if tab_sprite[k][j][0] != None:
                            if tab_sprite[k][j][0] == tab_sprite[i][j][0]:
                                score += 2 ** (ordre_sprite[tab_sprite[i][j][1]][1] + 1)
                                
                                tab_sprite[i][j] = ordre_sprite[tab_sprite[i][j][1]+1]
                                tab_sprite[k][j] = ordre_sprite[0]
                                test_changement = 1
                                test_fusion = 1
                                if tab_sprite[i][j][0] == valeur_max[mode] and test_victoire == 0:
                                    print(test_victoire)
                                    test_victoire = 1
                                    if test_save_csv == False:
                                        test_save_csv = True
                                test_fusion = 1
                                continue

                            elif i > k+1:
                                tab_sprite[i-1][j] = tab_sprite[k][j]
                                tab_sprite[k][j] = ordre_sprite[0]
                                test_changement = 1
                                break  
                            else:
                                break
    def left_move():
        global score, test_save_csv
        """Cette fonction effectue les modifications d'un mouvement vers la gauche."""
        nonlocal test_changement, test_victoire
        for i in range(4):
            for j in range(3):
                test_fusion = 0
                for k in range(j+1,4):
                    if tab_sprite[i][j][0] == None:
                        if tab_sprite[i][k][0] != None:
                            tab_sprite[i][j] = tab_sprite[i][k]
                            tab_sprite[i][k] = ordre_sprite[0]
                            test_changement = 1        
                    elif test_fusion == 0:
                        if tab_sprite[i][k][0] != None:
                            if tab_sprite[i][k][0] == tab_sprite[i][j][0]:
                                score += 2 ** (ordre_sprite[tab_sprite[i][j][1]][1] + 1)
                                
                                tab_sprite[i][j] = ordre_sprite[tab_sprite[i][j][1]+1]
                                tab_sprite[i][k] = ordre_sprite[0]
                                test_changement = 1
                                if tab_sprite[i][j][0] == valeur_max[mode] and test_victoire == 0:
                                    print(test_victoire)
                                    test_victoire = 1
                                    if test_save_csv == False:
                                        test_save_csv = True
                                test_fusion = 1
                                continue

                            elif j < k-1:
                                tab_sprite[i][j+1] = tab_sprite[i][k]
                                tab_sprite[i][k] = ordre_sprite[0]
                                test_changement = 1
                                break  
                            else:
                                break
    def right_move():
        global score, test_save_csv
        """Cette fonction effectue les modifications d'un mouvement vers la droite."""
        nonlocal test_changement, test_victoire
        for i in range(4):
            for j in range(3,0,-1):
                test_fusion = 0
                for k in range(j-1,-1,-1):
                    if tab_sprite[i][j][0] == None:
                        if tab_sprite[i][k][0] != None:
                            tab_sprite[i][j] = tab_sprite[i][k]
                            tab_sprite[i][k] = ordre_sprite[0]
                            test_changement = 1        
                    elif test_fusion == 0:
                        if tab_sprite[i][k][0] != None:
                            if tab_sprite[i][k][0] == tab_sprite[i][j][0]:
                                score += 2 ** (ordre_sprite[tab_sprite[i][j][1]][1] + 1)
                                
                                tab_sprite[i][j] = ordre_sprite[tab_sprite[i][j][1]+1]
                                tab_sprite[i][k] = ordre_sprite[0]
                                test_changement = 1
                                if tab_sprite[i][j][0] == valeur_max[mode] and test_victoire == 0:
                                    print(test_victoire)
                                    test_victoire = 1
                                    if test_save_csv == False:
                                        test_save_csv = True
                                test_fusion = 1
                                continue

                            elif j > k+1:
                                tab_sprite[i][j-1] = tab_sprite[i][k]
                                tab_sprite[i][k] = ordre_sprite[0]
                                test_changement = 1
                                break  
                            else:
                                break



                            
    def up_move_test():
        """Cette fonction renvoie True si un mouvement vers le haut est possible et False dans le cas contraire."""
        nonlocal test_changement,test_victoire
        for j in range(4):
            for i in range(3):
                for k in range(i+1,4):
                    if tab_sprite[i][j][0] == None:
                        if tab_sprite[k][j][0] != None:
                            return True
                    else:
                        if tab_sprite[k][j][0] != None:
                            if tab_sprite[k][j][0] == tab_sprite[i][j][0]:    
                                return True

                            elif i < k-1:
                                return True
                            else:
                                break
        return False


    def down_move_test():
        """Cette fonction renvoie True si un mouvement vers le bas est possible et False dans le cas contraire."""
        nonlocal test_changement, test_victoire
        for j in range(4):
            for i in range(3,0,-1):
                for k in range(i-1,-1,-1):
                    if tab_sprite[i][j][0] == None:
                        if tab_sprite[k][j][0] != None:
                            return True 
                    else:
                        if tab_sprite[k][j][0] != None:
                            if tab_sprite[k][j][0] == tab_sprite[i][j][0]:
                                return True

                            elif i > k+1:
                                return True
                            else:
                                break
        return False


    def left_move_test():
        """Cette fonction renvoie True si un mouvement vers la gauche est possible et False dans le cas contraire."""
        nonlocal test_changement, test_victoire
        for i in range(4):
            for j in range(3):
                for k in range(j+1,4):
                    if tab_sprite[i][j][0] == None:
                        if tab_sprite[i][k][0] != None:
                            return True
                    else:
                        if tab_sprite[i][k][0] != None:
                            if tab_sprite[i][k][0] == tab_sprite[i][j][0]:
                                return True

                            elif j < k-1:
                                return True
                            else:
                                break
        return False


    def right_move_test():
        """Cette fonction renvoie True si un mouvement vers la droite est possible et False dans le cas contraire."""
        nonlocal test_changement, test_victoire
        for i in range(4):
            for j in range(3,0,-1):
                for k in range(j-1,-1,-1):
                    if tab_sprite[i][j][0] == None:
                        if tab_sprite[i][k][0] != None:
                            return True   
                    else:
                        if tab_sprite[i][k][0] != None:
                            if tab_sprite[i][k][0] == tab_sprite[i][j][0]:
                                return True

                            elif j > k+1:
                                return True
                            else:
                                break
        return False

    

    global mode, ordre_sprite, fond, var_musique, score, test_save_csv, var_bouton_parametre,var_parametre_clicked

    score = 0
    var_quitter = False
    valeur_max = sprite_512

    #création du tableau des valeurs des sprites et du tableau sauvegarde(pour le bouton retour)
    tab_sprite = [  [ ordre_sprite[0], ordre_sprite[0], ordre_sprite[0], ordre_sprite[0] ],
                    [ ordre_sprite[0], ordre_sprite[0], ordre_sprite[0], ordre_sprite[0] ],
                    [ ordre_sprite[0], ordre_sprite[0], ordre_sprite[0], ordre_sprite[0] ],
                    [ ordre_sprite[0], ordre_sprite[0], ordre_sprite[0], ordre_sprite[0] ]  ]

    tab_sprite_retour = [   [ ordre_sprite[0], ordre_sprite[0], ordre_sprite[0], ordre_sprite[0] ],
                            [ ordre_sprite[0], ordre_sprite[0], ordre_sprite[0], ordre_sprite[0] ],
                            [ ordre_sprite[0], ordre_sprite[0], ordre_sprite[0], ordre_sprite[0] ],
                            [ ordre_sprite[0], ordre_sprite[0], ordre_sprite[0], ordre_sprite[0] ]   ]
             
    score_retour = 0
    None_list = [ [0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[2,0],[2,1],[2,2],[2,3],[3,0],[3,1],[3,2],[3,3] ] #tableau contenant les coordonnées des cases vides
    test_changement = 0        #variable = 1 si un mouvement a modifié tab_sprite
    test_victoire = 0        #variable = 1 si une des cases = 2048
    pause_clic = 0        #variable permettant d'effectuer une seule action quand une fleche du clavier est touchée
    nb_mouv = 0        #variable indiquant le nombre de mouvement depuis le debut de la partie

    #création des variables d'état des boutons
    returned = True        #variable = True si le bouton retour ne doit pas etre activé
    var_bouton_retour = 0        #variable d'état du bouton retour
    var_bouton_retour_menu = 0        #variable d'état du bouton menu
    var_bouton_parametre = 0        #variable d'état du bouton paramètre
    var_parametre_clicked = False        #variable = True si le bouton parametre est activé
    None_list_generator()
    random_spawn()

    ########################################################################################################
    ### BOUCLE INFINIE
    ########################################################################################################
    
    while 1:
        for evenement in pygame.event.get():
            keys = pygame.key.get_pressed()
            if evenement.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                sys.exit()
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                x,y = evenement.pos
                if x <= 75 and y <= 75 and nb_mouv > 0 and returned == False:
                    returned = True
                    var_bouton_retour = 1
                    screen.blit(sprite_bouton_retour[2],rect_bouton_retour)
                    pygame.display.flip()
                    print("retour1",score,score_retour)
                    score = score_retour
                    print("retour2",score,score_retour)
                    for i in range(4):
                        for j in range(4):
                            tab_sprite[i][j] = tab_sprite_retour[i][j]


                if x >= 1380 and y >= 10 and x <= 1530 and y <= 50:
                    screen.blit(sprite_retour_menu[2],rect_bouton_retour_menu)
                    pygame.display.flip()
                    if test_victoire == "False" or test_victoire == 1:
                        var_quitter = True
                        test_victoire = 0
                    else:
                        menu()
                
                if x >= 0 and y >= 715 and x <= 75 and y <= 780:
                    if var_parametre_clicked == False : var_parametre_clicked = True
                    elif var_parametre_clicked == True : var_parametre_clicked = False

                if x >= 0 and y >= 675 and x <= 230 and y <= 711 and var_parametre_clicked == True:
                    new_x = pos_curseur(x)
                    rect_curseur_parametre.center = new_x,693.5
                    volume = (new_x - 15) / 200
                    pygame.mixer.music.set_volume(volume)

                
                if x >= 0 and y >= 615 and x <= 230 and y <= 651 and var_parametre_clicked == True:
                    new_x = pos_curseur(x)
                    rect_curseur_parametre2.center = new_x,633.5
                    volume = (new_x - 15) / 200
                    swoosh.set_volume(volume)
                
                if x >= 40 and y >= 532 and x <= 60 and y <= 562 and var_parametre_clicked == True:
                    if fond == 0:
                        fond = len(sprites_fonds)-1
                    else:
                        fond -= 1
                
                if x >= 172 and y >= 532 and x <= 192 and y <= 562 and var_parametre_clicked == True:
                    if fond == len(sprites_fonds)-1:
                        fond = 0
                    else:
                        fond += 1
                

                if x >= 46 and y >= 410 and x <= 66 and y <= 440 and var_parametre_clicked == True:
                    if mode == 0:
                        mode = len(sprite_2)-1
                    else:
                        mode -= 1
                    
                    ordre_sprite =  ( (None,0), (sprite_2[mode],1), (sprite_4[mode],2), (sprite_8[mode],3), (sprite_16[mode],4), (sprite_32[mode],5), (sprite_64[mode],6), (sprite_128[mode],7), 
                                      (sprite_256[mode],8), (sprite_512[mode],9), (sprite_1024[mode],10), (sprite_2048[mode],11), (sprite_N,12) )

                    for i in range(4):
                        for j in range(4):
                            if tab_sprite[i][j][0] != None:
                                tab_sprite[i][j] = ordre_sprite[tab_sprite[i][j][1]]
                            if tab_sprite_retour[i][j][0] != None:
                                tab_sprite_retour[i][j] = ordre_sprite[tab_sprite_retour[i][j][1]]
                
                if x >= 166 and y >= 410 and x <= 186 and y <= 440 and var_parametre_clicked == True:
                    if mode == len(sprite_2)-1:
                        mode = 0
                    else:
                        mode += 1 
                    
                    ordre_sprite =  ( (None,0), (sprite_2[mode],1), (sprite_4[mode],2), (sprite_8[mode],3), (sprite_16[mode],4), (sprite_32[mode],5), (sprite_64[mode],6), (sprite_128[mode],7), 
                                      (sprite_256[mode],8), (sprite_512[mode],9), (sprite_1024[mode],10), (sprite_2048[mode],11), (sprite_N,12) )

                    for i in range(4):
                        for j in range(4):
                            if tab_sprite[i][j][0] != None:
                                tab_sprite[i][j] = ordre_sprite[tab_sprite[i][j][1]]
                            if tab_sprite_retour[i][j][0] != None:
                                tab_sprite_retour[i][j] = ordre_sprite[tab_sprite_retour[i][j][1]]
                
                if x >= 46 and y >= 475 and x <= 66 and y <= 505 and var_parametre_clicked == True:
                    if var_musique == 0:
                        var_musique = len(musique)-1
                    else:
                        var_musique -= 1
                    
                    pygame.mixer.music.load(musique[var_musique]["musique"])
                    pygame.mixer.music.play(-1, 0.0)
                
                if x >= 166 and y >= 475 and x <= 186 and y <= 505 and var_parametre_clicked == True:
                    if var_musique == len(musique)-1:
                        var_musique = 0
                    else:
                        var_musique += 1 
                    
                    
                    pygame.mixer.music.load(musique[var_musique]["musique"])
                    pygame.mixer.music.play(-1, 0.0)

            mouse_x,mouse_y = pygame.mouse.get_pos()
            if mouse_x <= 75 and mouse_y <= 75:
                var_bouton_retour = 1
            else:            
                var_bouton_retour = 0
            
            if mouse_x >= 1380 and mouse_y >= 10 and mouse_x <= 1530 and mouse_y <= 50:
                var_bouton_retour_menu = 1
            else:            
                var_bouton_retour_menu = 0

            if mouse_x >= 0 and mouse_y >= 715 and mouse_x <= 75 and mouse_y <= 780:
                var_bouton_parametre = 1
            else:            
                var_bouton_parametre = 0

            if keys[pygame.K_UP] == True and pause_clic == 0:
                for i in range(4):
                    for j in range(4):
                        tab_sprite_retour[i][j] = tab_sprite[i][j]
                score_retour = score
                if test_victoire == 1:
                    test_victoire = "False"
                nb_mouv += 1
                pause_clic = 1
                None_list = []
                up_move()
                if test_changement == 0:
                    continue
                
                swoosh.play()
                test_changement = 0
                None_list_generator()
                random_spawn()
                pause_clic = 0
                returned = False

            if keys[pygame.K_DOWN] == True and pause_clic == 0:
                for i in range(4):
                    for j in range(4):
                        tab_sprite_retour[i][j] = tab_sprite[i][j]
                score_retour = score
                if test_victoire == 1:
                    test_victoire = "False"
                nb_mouv += 1
                pause_clic = 1
                None_list = []
                down_move()
                if test_changement == 0:
                    continue
                swoosh.play()
                test_changement = 0
                None_list_generator()
                random_spawn()
                pause_clic = 0
                returned = False

            if keys[pygame.K_LEFT] == True and pause_clic == 0:
                for i in range(4):
                    for j in range(4):
                        tab_sprite_retour[i][j] = tab_sprite[i][j]
                score_retour = score
                if test_victoire == 1:
                    test_victoire = "False"
                nb_mouv += 1
                pause_clic = 1
                None_list = []
                left_move()
                if test_changement == 0:
                    continue
                swoosh.play()
                test_changement = 0
                None_list_generator()
                random_spawn()
                pause_clic = 0
                returned = False

            if keys[pygame.K_RIGHT] == True and pause_clic == 0:
                for i in range(4):
                    for j in range(4):
                        tab_sprite_retour[i][j] = tab_sprite[i][j]
                score_retour = score
                if test_victoire == 1:
                    test_victoire = "False"
                nb_mouv += 1
                pause_clic = 1
                None_list = []
                right_move()
                if test_changement == 0:
                    continue
                swoosh.play()
                test_changement = 0
                None_list_generator()
                random_spawn()
                pause_clic = 0
                returned = False


        pause_clic = 0

        
        text_surface_score = myfont.render(str(score), False, (230, 230, 230))
        #affiche les sprites

        screen.blit(sprites_fonds[fond],rect_fond)
        screen.blit(sprite_cadre,rect_cadre)
        screen.blit(sprite_bouton_retour[var_bouton_retour],rect_bouton_retour)
        screen.blit(sprite_retour_menu[var_bouton_retour_menu],rect_bouton_retour_menu)
        screen.blit(sprite_parametre[var_bouton_parametre],rect_bouton_parametre)
        screen.blit(text_surface_score,(1100,100))
        if var_parametre_clicked == True:
            screen.blit(sprite_barre_parametre,rect_barre_parametre)
            screen.blit(sprite_curseur_parametre,rect_curseur_parametre)
            screen.blit(sprite_texte_musique,rect_texte_musique)
            screen.blit(sprite_barre_parametre,rect_barre_parametre2)
            screen.blit(sprite_curseur_parametre,rect_curseur_parametre2)
            screen.blit(sprite_texte_sons,rect_texte_sons)
            screen.blit(sprites_fonds_mini[fond],rect_fond_mini)
            screen.blit(sprite_flèche_gauche,rect_flèche_fond_gauche)
            screen.blit(sprite_flèche_droite,rect_flèche_fond_droite)
            screen.blit(sprites_2_mini[mode],rect_2_mini)
            screen.blit(sprite_flèche_gauche,rect_flèche_2_gauche)
            screen.blit(sprite_flèche_droite,rect_flèche_2_droite)
            screen.blit(musique[var_musique]["image"],rect_musique)
            screen.blit(sprite_flèche_gauche,rect_flèche_3_gauche)
            screen.blit(sprite_flèche_droite,rect_flèche_3_droite)

        for i in range(4):
            for j in range(4):
                if tab_sprite[i][j][0] != None:
                    screen.blit(tab_sprite[i][j][0],rect[i][j])

        if [up_move_test(),down_move_test(),left_move_test(),right_move_test()] == [False,False,False,False]:
            returned = True
            pygame.mixer.music.pause()
            defaite()
        if test_victoire == 1:
            victoire()
        if var_quitter == True:
            if not [up_move_test(),down_move_test(),left_move_test(),right_move_test()] == [False,False,False,False]:
                quitter()
            else: 
                menu()
        pygame.display.flip()
        time.sleep(0.1)


def menu():
    pygame.mixer.music.unpause() #reprend la musique si elle est en pause
    

    #charge les autres variables dans la fonction
    global fond, var_musique

    #création des variables d'état des boutons
    var_bouton_menu_jouer = 0
    var_bouton_twitter = 0
    var_bouton_insta = 0
    var_bouton_discord = 0
    var_bouton_parametre = 0
    var_parametre_clicked = False

    
    file = open(chemin_programme +"file_csv.csv","r",newline='')
    
    myReader = csv.DictReader(file)
    tab_score = []
    for ligne in myReader:
        tab_score.append([ligne["Nom"],int(ligne["Score"])])
        print(ligne)

    
    text_surface_score_1,text_surface_score_2,text_surface_score_3,text_surface_score_4,text_surface_score_5 = 0,0,0,0,0
    tab_text_surface = [text_surface_score_1,text_surface_score_2,text_surface_score_3,text_surface_score_4,text_surface_score_5]
    for i in range(5):
        if len(tab_score) > i:
            print(i,tab_score[i],len(tab_score))
            tab_text_surface[i] = myfont2.render(str(tab_score[i][0]) + " " + str(tab_score[i][1]), False, (230, 230, 230))
        if len(tab_score) <= i:
            tab_text_surface[i] = myfont2.render(None, False, (230, 230, 230))
    
    print(tab_text_surface)
    text_surface_meilleur_score = myfont.render("Meilleurs scores", False, (230, 230, 230))
    tab_pos_text = ( (900,150), (900,250), (900,350), (900,450), (900,550) )
    #boucle infinie
    while 1:
        for evenement in pygame.event.get():
            keys = pygame.key.get_pressed()
            if evenement.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                sys.exit()
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                x,y = evenement.pos
                if x <= 370 and y <= 350 and x >= 250 and y >= 300:
                    game()
                if x <= 1530 and y <= 85 and x >= 1450 and y >= 5:
                    webbrowser.open('https://twitter.com/Keima04332639')
                if x <= 1530 and y <= 170 and x >= 1450 and y >= 90:
                    webbrowser.open('https://instagram.com/keima_nara')
                if x <= 1530 and y <= 255 and x >= 1450 and y >= 175:
                    webbrowser.open('https://discord.com/channels/@me/824348392938930188')
                
                if x >= 0 and y >= 715 and x <= 75 and y <= 780:
                    if var_parametre_clicked == False : var_parametre_clicked = True
                    elif var_parametre_clicked == True : var_parametre_clicked = False

                if x >= 0 and y >= 675 and x <= 230 and y <= 711 and var_parametre_clicked == True:
                    new_x = pos_curseur(x)
                    rect_curseur_parametre.center = new_x,693.5
                    volume = (new_x - 15) / 200
                    pygame.mixer.music.set_volume(volume)

                if x >= 40 and y >= 532 and x <= 60 and y <= 562 and var_parametre_clicked == True:
                    if fond == 0:
                        fond = len(sprites_fonds)-1
                    else:
                        fond -= 1
                
                if x >= 172 and y >= 532 and x <= 192 and y <= 562 and var_parametre_clicked == True:
                    if fond == len(sprites_fonds)-1:
                        fond = 0
                    else:
                        fond += 1
                
                if x >= 46 and y >= 475 and x <= 66 and y <= 505 and var_parametre_clicked == True:
                    if var_musique == 0:
                        var_musique = len(musique)-1
                    else:
                        var_musique -= 1
                    
                    pygame.mixer.music.load(musique[var_musique]["musique"])
                    pygame.mixer.music.play(-1, 0.0)
                
                if x >= 166 and y >= 475 and x <= 186 and y <= 505 and var_parametre_clicked == True:
                    if var_musique == len(musique)-1:
                        var_musique = 0
                    else:
                        var_musique += 1 
                    
                    
                    pygame.mixer.music.load(musique[var_musique]["musique"])
                    pygame.mixer.music.play(-1, 0.0)
                    
                    


            x,y = pygame.mouse.get_pos()
            
            if x <= 370 and y <= 350 and x >= 250 and y >= 300:
                var_bouton_menu_jouer = 1
            else:            
                var_bouton_menu_jouer = 0

            if x <= 1530 and y <= 85 and x >= 1450 and y >= 5:
                var_bouton_twitter = 1
            else:            
                var_bouton_twitter = 0

            if x <= 1530 and y <= 170 and x >= 1450 and y >= 90:
                var_bouton_insta = 1
            else:            
                var_bouton_insta = 0

            if x <= 1530 and y <= 255 and x >= 1450 and y >= 175:
                var_bouton_discord = 1
            else:            
                var_bouton_discord = 0

            if x >= 0 and y >= 715 and x <= 75 and y <= 780:
                var_bouton_parametre = 1
            else:            
                var_bouton_parametre = 0
        #affiche les sprites

        screen.blit(sprites_fonds[fond],rect_fond)
        screen.blit(sprite_titre,rect_titre)
        screen.blit(sprite_twitter[var_bouton_twitter],rect_twitter)
        screen.blit(sprite_insta[var_bouton_insta],rect_insta)
        screen.blit(sprite_discord[var_bouton_discord],rect_discord)
        screen.blit(sprite_menu_bouton_jouer[var_bouton_menu_jouer],rect_sprite_menu_bouton_jouer)
        screen.blit(sprite_parametre[var_bouton_parametre],rect_bouton_parametre)
        for i in range(5):
            screen.blit(tab_text_surface[i],tab_pos_text[i])
        screen.blit(text_surface_meilleur_score,(850,50))
        if var_parametre_clicked == True:
            screen.blit(sprite_barre_parametre,rect_barre_parametre)
            screen.blit(sprite_curseur_parametre,rect_curseur_parametre)
            screen.blit(sprite_texte_musique,rect_texte_musique)
            screen.blit(sprites_fonds_mini[fond],rect_fond_mini)
            screen.blit(sprite_flèche_gauche,rect_flèche_fond_gauche)
            screen.blit(sprite_flèche_droite,rect_flèche_fond_droite)
            screen.blit(musique[var_musique]["image"],rect_musique)
            screen.blit(sprite_flèche_gauche,rect_flèche_3_gauche)
            screen.blit(sprite_flèche_droite,rect_flèche_3_droite)

        pygame.display.flip()

                






########################################################################################################
### PROGRAMME PRINCIPAL
########################################################################################################
pygame.init() #initialisation de pygame
pygame.mixer.init() #initialisation du module de son

size = 1535,800 
screen = pygame.display.set_mode(size) #initialisation de la fenetre

test_save_csv = False
fond = 0
mode = 0

myfont = pygame.font.SysFont('Consolas', 60)
myfont2 = pygame.font.SysFont('Consolas', 45)
myfont3 = pygame.font.SysFont('Consolas', 40)
myfont4 = pygame.font.SysFont('Consolas', 30)

score = 0
text_surface_score = myfont.render(str(score), False, (230,230,230))
text_entree_nom = "Anonyme"
text_surface_entree_nom = myfont3.render(text_entree_nom, False, (230,230,230))
text_surface_bouton_valider = myfont4.render("Ok", False, (230,230,230))

#Définition de la position des sprites

tab_pos = ( ( (450,100), (605,100),(760,100),(915,100) ),
            ( (450,255), (605,255),(760,255),(915,255) ),
            ( (450,410), (605,410),(760,410),(915,410) ),
            ( (450,565), (605,565),(760,565),(915,565) ) )

#chargement des musiques 
musique = []
indice_musique = -1


chemin_programme = ""
for i in range(len(sys.argv[0].split("/"))):
    if i < len(sys.argv[0].split("/")) - 1:
        chemin_programme += sys.argv[0].split("/")[i] + "/"

for d in listdir(chemin_programme + "sons et musiques 2048/Musique"):
    if isdir(join(chemin_programme + "sons et musiques 2048/Musique", d)):
        musique.append({"musique" : None,"image" : None})
        indice_musique += 1
        for f in listdir(join(chemin_programme + "sons et musiques 2048/Musique", d)):
            if isfile(join(chemin_programme + "sons et musiques 2048/Musique", d, f)):
                kind = filetype.guess(join(chemin_programme + "sons et musiques 2048/Musique", d, f))
                
                if kind.extension == "ogg":
                    musique[indice_musique]["musique"] = join(chemin_programme + "sons et musiques 2048/Musique", d, f)
                
                if kind.extension == "png":
                    musique[indice_musique]["image"] = pygame.image.load(join(chemin_programme + "sons et musiques 2048/Musique", d, f))
        
        if musique[indice_musique]["musique"] == None:
            del musique[indice_musique]
            indice_musique -= 1
        if musique[indice_musique]["image"] == None:
            musique[indice_musique]["image"] = pygame.image.load(chemin_programme + "sons et musiques 2048/Musique/image_par_defaut.png")

del indice_musique
var_musique = 0
pygame.mixer.music.load(musique[var_musique]["musique"])


#chargement des sons
swoosh = pygame.mixer.Sound(chemin_programme + "sons et musiques 2048/Swoosh.ogg")
swoosh.set_volume(0.5)

#chargement des sprites
sprites_fonds = []
for f in listdir(chemin_programme + "2048_sprites/fond"):
    if isfile(join(chemin_programme + "2048_sprites/fond", f)):
        sprites_fonds.append(pygame.image.load(join(chemin_programme + "2048_sprites/fond", f)))

sprites_fonds_mini = []
for i in sprites_fonds:
    sprites_fonds_mini.append(pygame.transform.scale(i, (72, 38)))



sprite_parametre = (pygame.image.load(chemin_programme + "2048_sprites/parametre/parametre.png"),pygame.image.load(chemin_programme + "2048_sprites/parametre/parametre2.png"))
sprite_barre_parametre = pygame.image.load(chemin_programme + "2048_sprites/parametre/barre_parametre.png")
sprite_curseur_parametre = pygame.image.load(chemin_programme + "2048_sprites/parametre/curseur_parametre.png")
sprite_texte_musique = pygame.image.load(chemin_programme + "2048_sprites/parametre/texte_musique.png")
sprite_texte_sons = pygame.image.load(chemin_programme + "2048_sprites/parametre/texte_sons.png")
sprite_flèche_gauche = pygame.image.load(chemin_programme + "2048_sprites/parametre/flèche_fond_gauche.png")
sprite_flèche_droite = pygame.image.load(chemin_programme + "2048_sprites/parametre/flèche_fond_droite.png")
sprite_menu_bouton_jouer = (pygame.image.load(chemin_programme + "2048_sprites/menu/bouton_menu_jouer1.png"),pygame.image.load(chemin_programme + "2048_sprites/menu/bouton_menu_jouer2.png"))
sprite_titre = pygame.image.load(chemin_programme + "2048_sprites/menu/titre.png")
sprite_twitter = (pygame.image.load(chemin_programme + "2048_sprites/menu/twitter.png"),pygame.image.load(chemin_programme + "2048_sprites/menu/twitter2.png"))
sprite_insta = (pygame.image.load(chemin_programme + "2048_sprites/menu/insta.png"),pygame.image.load(chemin_programme + "2048_sprites/menu/insta2.png"))
sprite_discord = (pygame.image.load(chemin_programme + "2048_sprites/menu/discord.png"),pygame.image.load(chemin_programme + "2048_sprites/menu/discord2.png"))


sprite_2 = []
sprite_4 = []
sprite_8 = []
sprite_16 = []
sprite_32 = []
sprite_64 = []
sprite_128 = []
sprite_256 = []
sprite_512 = []
sprite_1024 = []
sprite_2048 = []
list_sprites_tuiles = [sprite_2, sprite_4, sprite_8, sprite_16, sprite_32, sprite_64, sprite_128, sprite_256, sprite_512, sprite_1024, sprite_2048]


for d in listdir(chemin_programme + "2048_sprites/sprites_tuiles"):
    if isdir(join(chemin_programme + "2048_sprites/sprites_tuiles", d)):
        for i in range(11):
            list_sprites_tuiles[i].append(pygame.image.load(chemin_programme + "2048_sprites/sprites_tuiles" + "//" + d + "//" + str(2**(i+1)) + ".png"))


sprites_2_mini = []
for i in sprite_2:
    sprites_2_mini.append(pygame.transform.scale(i, (60, 60)))


sprite_N = pygame.image.load(chemin_programme + "2048_sprites/sprites_tuiles/N.png")
sprite_cadre = pygame.image.load(chemin_programme + "2048_sprites/jeu/cadre.png")
sprite_victoire = pygame.image.load(chemin_programme + "2048_sprites/jeu/victoire.png")
sprite_defaite = pygame.image.load(chemin_programme + "2048_sprites/jeu/defaite.png")
sprite_bouton_retour = (pygame.image.load(chemin_programme + "2048_sprites/jeu/bouton_retour.png"),pygame.image.load(chemin_programme + "2048_sprites/jeu/bouton_retour_2.png"),pygame.image.load(chemin_programme + "2048_sprites/jeu/bouton_retour_clické.png"))
sprite_retour_menu = (pygame.image.load(chemin_programme + "2048_sprites/jeu/retour_menu.png"),pygame.image.load(chemin_programme + "2048_sprites/jeu/retour_menu2.png"),pygame.image.load(chemin_programme + "2048_sprites/jeu/retour_menu3.png"))
sprite_barre_entree_nom = pygame.image.load(chemin_programme + "2048_sprites/jeu/barre_entree_nom.png")
sprite_curseur_entree_nom = pygame.image.load(chemin_programme + "2048_sprites/jeu/curseur_entree_nom.png")


#active la musique et précise le volume

pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.5)


#création des rects

rect_fond = sprites_fonds[fond].get_rect()
rect_fond.topleft = 0,0
rect_fond_mini = sprites_fonds_mini[fond].get_rect()
rect_fond_mini.topleft = 80,530

rect_bouton_parametre = sprite_parametre[0].get_rect()
rect_bouton_parametre.topleft = 0,715
rect_barre_parametre = sprite_barre_parametre.get_rect()
rect_barre_parametre.topleft = 15,690
rect_barre_parametre2 = sprite_barre_parametre.get_rect()
rect_barre_parametre2.topleft = 15,630
rect_curseur_parametre = sprite_curseur_parametre.get_rect()
rect_curseur_parametre.center = 115,693.5
rect_curseur_parametre2 = sprite_curseur_parametre.get_rect()
rect_curseur_parametre2.center = 115,633.5
rect_texte_musique = sprite_texte_musique.get_rect()
rect_texte_musique.topleft = 15,660
rect_texte_sons = sprite_texte_sons.get_rect()
rect_texte_sons.topleft = 15,600
rect_flèche_fond_gauche = sprite_flèche_gauche.get_rect()
rect_flèche_fond_gauche.topleft = 40,534
rect_flèche_fond_droite = sprite_flèche_droite.get_rect()
rect_flèche_fond_droite.topleft = 172,534
rect_2_mini = sprites_2_mini[mode].get_rect()
rect_2_mini.topleft = 86,395
rect_flèche_2_gauche = sprite_flèche_gauche.get_rect()
rect_flèche_2_gauche.topleft = 46,410
rect_flèche_2_droite = sprite_flèche_droite.get_rect()
rect_flèche_2_droite.topleft = 166,410
rect_musique = musique[var_musique]["image"].get_rect()
rect_musique.topleft = 86,460
rect_flèche_3_gauche = sprite_flèche_gauche.get_rect()
rect_flèche_3_gauche.topleft = 46,475
rect_flèche_3_droite = sprite_flèche_droite.get_rect()
rect_flèche_3_droite.topleft = 166,475

rect_sprite_menu_bouton_jouer = sprite_menu_bouton_jouer[0].get_rect()
rect_sprite_menu_bouton_jouer.topleft = (250,300)
rect_titre = sprite_titre.get_rect()
rect_titre.topleft = (120, 20)
rect_twitter = sprite_twitter[0].get_rect()
rect_twitter.topleft = 1450,5
rect_insta = sprite_insta[0].get_rect()
rect_insta.topleft = 1460,100
rect_discord = sprite_discord[0].get_rect()
rect_discord.topleft = 1460,195
rect_cadre = sprite_cadre.get_rect()
rect_victoire = sprite_victoire.get_rect()
rect_victoire.topleft = 0,0
rect_barre_entree_nom = sprite_barre_entree_nom.get_rect()
rect_barre_entree_nom.topleft = 400,200
rect_curseur_entree_nom = sprite_curseur_entree_nom.get_rect()
rect_curseur_entree_nom.topleft = 408,205
rect_defaite = sprite_defaite.get_rect()
rect_defaite.topleft = 0,0
rect_bouton_retour = sprite_bouton_retour[0].get_rect()
rect_bouton_retour.topleft = 0,0
rect_bouton_retour_menu = sprite_retour_menu[0].get_rect()
rect_bouton_retour_menu.topleft = 1380,10

rect = ( (  (sprite_2[mode].get_rect()), (sprite_2[mode].get_rect()),(sprite_2[mode].get_rect()),(sprite_2[mode].get_rect()) ),
            ( (sprite_2[mode].get_rect()), (sprite_2[mode].get_rect()),(sprite_2[mode].get_rect()),(sprite_2[mode].get_rect()) ),
            ( (sprite_2[mode].get_rect()), (sprite_2[mode].get_rect()),(sprite_2[mode].get_rect()),(sprite_2[mode].get_rect()) ),
            ( (sprite_2[mode].get_rect()), (sprite_2[mode].get_rect()),(sprite_2[mode].get_rect()),(sprite_2[mode].get_rect()) ) )

pos_cadre_ext = 445,95
rect_cadre.topleft = pos_cadre_ext

for i in range(4):
        for j in range(4):
            rect[i][j].topleft = tab_pos[i][j]


ordre_sprite =  ( (None,0), (sprite_2[mode],1), (sprite_4[mode],2), (sprite_8[mode],3), (sprite_16[mode],4), (sprite_32[mode],5), (sprite_64[mode],6), (sprite_128[mode],7), 
                    (sprite_256[mode],8), (sprite_512[mode],9), (sprite_1024[mode],10), (sprite_2048[mode],11), (sprite_N,12) )



#lance le menu
menu()