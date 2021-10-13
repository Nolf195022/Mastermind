import json
import copy
import os
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition, RiseInTransition
from random import randrange
#Chemin vers fichier de savegarde
savepath = 'save.json'
scorepath = 'scores.json'
colormatch = {i:[
    {"color" : "rouge", "code" : [1,0,0,1]},
    {"color" : "jaune", "code" : [255/255, 255/255, 0, 1]},
    {"color" : "bleu", "code" : [0, 0, 255/255, 1]},
    {"color" : "vert", "code" : [0, 255/255, 0, 1]},
    {"color" : "gris", "code" : [130/255, 130/255, 130/255, 1]},
    {"color" : "blanc", "code" : [255/255, 255/255, 255/255, 1]},
    {"color" : "mauve", "code" : [106/255, 90/255, 205/255, 1]},
    {"color" : "orange", "code" : [255/255, 165/255, 0, 1]}
    ][i] for i in range(8)}
# sans back to mainmenu
def detele(a):
    os.remove(a)
class Mastermindgame(App):
    #screenmanager
    def build(self):
        self.__manager = ScreenManager()
        self.__manager.add_widget(self.mainmenu())
        self.__manager.add_widget(self.helppage())
        return self.__manager
    def helppage(self):
        screen = Screen(name = 'Help')
        box = BoxLayout(orientation='vertical')
        titre = Label(text='How does mastermind works ?', font_size = 40, bold = True, size_hint=(1,0.1))
        box.add_widget(titre)
        cadre = BoxLayout(orientation='vertical', size_hint=(1,0.7))
        titlefontsize = 25
        textfontsize = 17
        margin = 0.044
        #------cadre------
            #Score 10%
        cadre.add_widget(Label(text = 'Score', font_size = titlefontsize, bold = True, size_hint=(1,0.05)))
        scorehelp = "The number of attempts you have left at victory equals your finalscore. \n In SUPER mode you have a maximum of 12 attempts \n In NORMAL mode you have a maximum of 10 attempts"
        cadre.add_widget(Label(size_hint=(1,margin)))
        cadre.add_widget(Label(text = scorehelp, font_size = textfontsize, size_hint=(1,0.1), halign = "center"))
        cadre.add_widget(Label(size_hint=(1,margin)))
            #Coulours text 10%
        cadre.add_widget(Label(text = 'Colors', font_size = titlefontsize, bold = True, size_hint=(1,0.05)))
        colorhelp = 'To create a color combination, just click on the color up to the one of your choice. Below you will find the list of colors in order. \nIn the answer there can be several times the same color.\n In NORMAL mode only the first 6 colors are used.'
        cadre.add_widget(Label(size_hint=(1,margin)))
        cadre.add_widget(Label(text = colorhelp, font_size = textfontsize, size_hint=(1,0.1), halign = "center"))
            #Coulours cadre 27%
        ordrecoloursbox = BoxLayout(orientation= 'horizontal',size_hint=(1,0.11))
        ordrecoloursbox.add_widget(Label(size_hint=(0.2,1)))
        for i in colormatch: 
            ordrecoloursbox.add_widget(Button(text = str(i+1),color =[0,0,0,1], bold= True , background_normal = '', background_color=colormatch[i]["code"], background_down = '', size_hint=(0.6/len(colormatch),1)))
        ordrecoloursbox.add_widget(Label(size_hint=(0.2,1)))
        cadre.add_widget(ordrecoloursbox)
        cadre.add_widget(Label(size_hint=(1,margin)))
            #Indices text = 5% * 4 cadres 11% * 3
        cadre.add_widget(Label(text = 'Hints', font_size = titlefontsize, bold = True, size_hint=(1,0.05)))
        cadre.add_widget(Label(size_hint=(1,margin)))
        ligneincide1 = BoxLayout(orientation= 'horizontal',size_hint=(1,0.11))
        espace1 = 0.46
        ligneincide1.add_widget(Label(size_hint=(espace1,1)))
        ligneincide1.add_widget(Button(size_hint=(1 - (2*espace1),1), background_normal = '', background_color=[39/255, 167/255, 255/255, 1], background_down = ''))
        ligneincide1.add_widget(Label(size_hint=(espace1,1)))
        cadre.add_widget(ligneincide1)
        cadre.add_widget(Label(text = "One color is in the right place", font_size = textfontsize, size_hint=(1,0.05), halign = "center"))
        ligneincide2 = BoxLayout(orientation= 'horizontal',size_hint=(1,0.11))
        ligneincide2.add_widget(Label(size_hint=(espace1,1)))
        ligneincide2.add_widget(Button(size_hint=(1 - (2*espace1),1), background_normal = '', background_color=[1, 1, 1, 1], background_down = ''))
        ligneincide2.add_widget(Label(size_hint=(espace1,1))) 
        cadre.add_widget(ligneincide2)
        cadre.add_widget(Label(text = "One color is right but not in the right place", font_size = textfontsize, size_hint=(1,0.05), halign = "center"))
        ligneincide3 = Label(size_hint=(1,0.11))
        cadre.add_widget(ligneincide3)
        cadre.add_widget(Label(text = "One color is not right", font_size = textfontsize, size_hint=(1,0.05), halign = "center"))
        #-----------------------
        box.add_widget(cadre)
        #-----------------------
        cadre2 = BoxLayout(orientation='horizontal', size_hint=(1,0.2),padding=[50,50,50,50])
        cadre2.add_widget(Label(size_hint=(0.35,1)))
        retour = Button(text='Back to game...', size_hint=(0.3,1))
        def switch1(source):
            self.__manager.transition = FallOutTransition()
            self.__manager.current = 'Mastermind'
        retour.bind(on_press=switch1)
        cadre2.add_widget(retour)
        cadre2.add_widget(Label(size_hint=(0.35,1)))
        box.add_widget(cadre2)
        screen.add_widget(box)
        return screen
    def mainmenu(self):
        screen = Screen(name = 'Mastermind - Mainmenu')
        main = BoxLayout(orientation='vertical')
        titleline = BoxLayout(orientation='horizontal')
        resumebuttonline = BoxLayout(orientation='horizontal', padding=[600,80,600,80]) 
        playbuttonline = BoxLayout(orientation='horizontal', padding=[600,80,600,80])
        levelbuttonline = BoxLayout(orientation='horizontal', padding=[600,80,600,80])
        self.__resumebutton = Button(text='RESUME')
        self.__resumebutton.bind(on_press=self._resumegame)
        self.__playbutton = Button(text='PLAY')
        self.__playbutton.bind(on_press=self._saveverif)
        self.__level = ['NORMAL','SUPER']
        self.__currentlevel = 0
        self.levelbutton = Button(text='DIFFICULTY : ' + self.__level[self.__currentlevel])
        self.levelbutton.bind(on_press=self._switchlevel)
        titleline.add_widget(Label(text='MASTERMIND'))
        resumebuttonline.add_widget(self.__resumebutton)
        playbuttonline.add_widget(self.__playbutton)
        levelbuttonline.add_widget(self.levelbutton)
        main.add_widget(titleline)
        #afficher le bouton RESUME uniquement si une sauvegarde existe
        try:
            with open(savepath, 'r'):
                main.add_widget(resumebuttonline)
        except:
            main.add_widget(Label(text = ' NO PREVIOUS GAME WAS SAVED '))
        main.add_widget(playbuttonline)
        main.add_widget(levelbuttonline)
        screen.add_widget(main)
        return screen
    def game(self):
        screen = Screen(name ='Mastermind')
        self.writevalidate = True 
        try:
            with open(savepath, 'r') as file:
                self.__session = json.loads(file.read())
        except:
            pass
        main = BoxLayout(orientation = "vertical")
        #création des variables de session de jeu
        if self.__session["level"] == "SUPER":
            self.__nombretentative = 12
            self.__nombrecouleurs = 8
            self.__nombrepions = 5
        else:
            self.__nombretentative = 10
            self.__nombrecouleurs = 6
            self.__nombrepions = 4
        self.__score = self.__nombretentative
        #modification de la sauvegarde, création de la combinaison si elle n'éxiste pas
        if self.__session["answer"] == []:
            self.__session["answer"] = self._goalgenerator(self.__nombrepions, self.__nombrecouleurs)
        try:
            with open(savepath, 'w') as file:
                file.write(json.dumps(self.__session, indent = 4))
        except:
            pass
        #titre | highscore
        bare1 = BoxLayout(orientation = "horizontal", size_hint=(1,0.08))
        title = Label(text="MASTERMIND \n\n" + 'PLAYER : ' + self.__session["pseudo"])
        highscore = Label(text="High Score :\n" + self.gethighscore())
        bare1.add_widget(title)
        bare1.add_widget(highscore)
        main.add_widget(bare1)
        self.presscolortext = (Label(text = 'Press one color to change the color',size_hint=(1,0.02)))
        main.add_widget(self.presscolortext)
        #etrée
        self.__combinaison = BoxLayout(orientation = "horizontal", size_hint=(1,0.15), padding=[200,20,200,20], spacing= 5)
        self.__combinaisonmaker = BoxLayout(orientation = "horizontal", size_hint=(0.5,1), spacing= 5)
        self.__combinaisonvalidate = BoxLayout(orientation = "horizontal", size_hint=(0.3,1))
        self.testbouton = Button(text = 'TRY')
        self.testbouton.bind(on_press=self.tryinput)
        for i in range(self.__nombrepions):
            self.iconbutton = Button(background_normal = '', background_color=[1, 0, 0, 1], background_down = '')
            self.iconbutton.bind(on_release= self._switchcolor)
            self.__combinaisonmaker.add_widget(self.iconbutton)
        self.__combinaisonvalidate.add_widget(self.testbouton)
        self.__combinaison.add_widget(self.__combinaisonmaker)
        self.__combinaison.add_widget(self.__combinaisonvalidate)
        main.add_widget(self.__combinaison)
        #tentative | indices
        self.__jeu = BoxLayout(orientation = "vertical", size_hint=(1,0.7))
        main.add_widget(self.__jeu)
        #Score + Level | infopopupbutton
        self.bare2 =BoxLayout(orientation = "horizontal", size_hint=(1,0.05))
        self.__currentprogress = Label(text = "Level : " + self.__session["level"] +"          "+ "Score : " + str(self.__score))
        self._input_tentatives()
        helppopupbutton = Button(text = 'HELP')
        def switch2(source):
            self.__manager.transition = RiseInTransition()
            self.__manager.current = 'Help'
        helppopupbutton.bind(on_press=switch2)
        self.bare2.add_widget(self.__currentprogress)
        self.bare2.add_widget(helppopupbutton)
        main.add_widget(self.bare2)
        screen.add_widget(main)
        return screen

    #fonction qui sert a faire changer les niveaux de difficulté
    def _switchlevel(self,source):
        if self.__currentlevel < len(self.__level)-1:
            self.__currentlevel += 1
            self.levelbutton.text = 'DIFFICULTY : ' + self.__level[self.__currentlevel]
        else : 
            self.__currentlevel = 0
            self.levelbutton.text = 'DIFFICULTY : ' + self.__level[self.__currentlevel]

    #fonction qui change l'ecran vers le jeu en fonction de sa difficultée
    def _saveverif(self, source):
        try:
            with open(savepath, 'r'):
                content = BoxLayout(orientation = 'horizontal')
                deletesavepopup = Popup(
                    title = 'Delete last save ?',
                    content = content,
                    size_hint=(None,None), size=(300,300))
                yesbutton = Button(text = 'YES')
                yesbutton.bind(on_press=self.pseudoenter)
                yesbutton.bind(on_press=deletesavepopup.dismiss)
                content.add_widget(yesbutton)
                nobutton = Button(text = 'NO')
                nobutton.bind(on_press=deletesavepopup.dismiss)
                content.add_widget(nobutton)
                deletesavepopup.open()
        except FileNotFoundError:
            self.pseudoenter(self)
    def _gamelaunch(self,source):
        with open(savepath, 'w') as file:
            file.write(json.dumps({"level":self.__level[self.__currentlevel],"answer" : [],"trials" : [],"pseudo" : self.currentpseudo}, indent = 4))
        with open(savepath, 'r') as file:
            self.__session = json.loads(file.read())
        self.__manager.add_widget(self.game())
        self.__manager.transition = RiseInTransition()
        self.__manager.current = 'Mastermind'
    def _resumegame(self,source):
        self.__manager.add_widget(self.game())
        self.__manager.transition = RiseInTransition()
        self.__manager.current = 'Mastermind'
    #generateur aléatoir de combinaisons en fonction du nombre de pions et de couleurs
    def _goalgenerator(self,a,b):
        # a = nombre de pions, b = nombre de couleurs 
        result = []
        for i in range(a):
            result.append(randrange(b))
        return result
    def gethighscore(self):
        try:
            with open(scorepath, 'r') as file:
                scoreboard = json.loads(file.read())
            minus = -1
            indice = 0
            indicetopplayer = 0
            for i in scoreboard[self.__session["level"]]:
                if i['score'] > minus:
                    minus = i['score']
                    indicetopplayer = indice
                indice +=1
            result = scoreboard[self.__session["level"]][indicetopplayer]['pseudo'] + '\n' + 'Score : ' + str(scoreboard[self.__session["level"]][indicetopplayer]['score'])
            return result
        except:
            return 'First game.. no highscore available'
    def tryinput(self,source):
        result = []
        indice = 0
        for i in self.__combinaisonmaker.children:
            indice -= 1
            result.append(self.__combinaisonmaker.children[indice].background_color)
        indice = 0
        tentative = self.colorcodeintoint(result)
        self.__session['trials'].append(tentative)
        self._input_tentatives()
        if self.writevalidate == True :
            try:
                with open(savepath, 'w') as file:
                    file.write(json.dumps(self.__session, indent = 4))
            except:
                pass

    def _input_tentatives(self):
        try:
            self.__jeu.clear_widgets()
            #parcourir la liste de tentatives a l'envers
            n = 0
            self.__score = self.__nombretentative - len(self.__session['trials'])
            self.__currentprogress.text = "Level : " + self.__session["level"] +"          "+ "Score : " + str(self.__score)
            for trial in self.__session['trials']:
                n -= 1
                self.__jeu.add_widget(self.__proces(self.__session['trials'][n]))
            i = len(self.__session['trials'])
            while i < self.__nombretentative:
                self.__jeu.add_widget(Label(size_hint=(1,1/self.__nombretentative)))
                i += 1
            if self.__score == 0:
                self.testbouton.unbind(on_press=self.tryinput)
                self.endgame(self.__session['trials'][-1])
        except:
            pass
    def __proces(self,trial):
        box = BoxLayout(orientation='horizontal', size_hint=(1,1/self.__nombretentative), padding=[400,2,400,2])
        #creation des indices
        leftresult = copy.deepcopy(self.__session['answer'])
        lefttrial = copy.deepcopy(trial)
        indice = 0
        perfectmatch = 0
        rightcolormatch = 0
        for i in lefttrial:
            if i == leftresult[indice]:
                leftresult[indice] = None
                lefttrial[indice] = None
                perfectmatch += 1
            indice += 1
        for i in lefttrial:
            indiceprime = 0    
            if (i in leftresult) and (i != None) :
                for x in leftresult:
                    if i == leftresult[indiceprime]:
                        leftresult[indiceprime] = None
                        break
                    indiceprime += 1
                rightcolormatch += 1
        #affichage des indices
        result = BoxLayout(orientation = 'horizontal', spacing = 5)
        for color in trial:
            for i in colormatch:
                if color == i:
                    result.add_widget(Button(size_hint=(0.45/self.__nombrepions,1) ,background_normal = '', background_color=colormatch[i]["code"], background_down = ''))
        result.add_widget(Label(size_hint=(0.20,1),text = 'Hint : '))
        for i in range(perfectmatch):
            result.add_widget(Button(size_hint=(0.35/self.__nombrepions,1) ,background_normal = '', background_color=[39/255, 167/255, 255/255, 1], background_down = ''))
        for i in range(rightcolormatch):
            result.add_widget(Button(size_hint=(0.35/self.__nombrepions,1) ,background_normal = '', background_color=[1, 1, 1, 1], background_down = ''))
        rien = self.__nombrepions - perfectmatch - rightcolormatch
        if rien > 0:
            for i in range(rien):
                result.add_widget(Label(size_hint=(0.35/self.__nombrepions,1)))
        box.add_widget(result)
        if self.__nombrepions == perfectmatch:
            self.win()
        return box
    def endgame(self,entry):
        #popup en fonction du status de jeu
        if self.__session['answer'] != entry:
            self.testbouton.disabled = True
            detele(savepath)
            self.presscolortext.text = ''
            self.writevalidate = False
            self.unableinput()
            self.bare2.clear_widgets()
            self.bare2.add_widget(Label(size_hint =(0.3,1), text = 'The answer was : '))
            answerbox = BoxLayout(orientation = 'horizontal', spacing = 5, size_hint = (0.4,1))
            for i in self.__session['answer']:
                answerbox.add_widget(Button(background_normal = '', background_color=colormatch[i]["code"], background_down = ''))
            self.bare2.add_widget(answerbox)
            lostquitbutton = Button(text ='QUIT',size_hint =(0.1,1))
            lostquitbutton.bind(on_press=self.stope)
            self.bare2.add_widget(Label(size_hint=(0.1,1)))
            self.bare2.add_widget(lostquitbutton)
            self.bare2.add_widget(Label(size_hint=(0.1,1)))
            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text=str(self.__session['pseudo'])))
            content.add_widget(Label(text='YOU LOST'))
            content.add_widget(Label(text='Press RESUME to check the answer'))
            buttonsbox = BoxLayout(orientation = 'horizontal', spacing = 5)
            resumebutton = Button(text='RESUME')
            quitbutton = Button(text='QUIT')
            quitbutton.bind(on_press=self.stope)
            buttonsbox.add_widget(resumebutton)
            buttonsbox.add_widget(quitbutton)
            content.add_widget(buttonsbox)
            lostpopup = Popup(title = 'GAME OVER', content = content,size_hint=(None,None), size=(300,300))
            lostpopup.open()
            resumebutton.bind(on_press=lostpopup.dismiss)
    def win(self): 
        try:
            with open(scorepath, 'r') as file:
                scoreboard = json.loads(file.read())
            scoreboard[self.__session["level"]].append({"pseudo": self.__session['pseudo'],'score':self.__score})
        except:
            scoreboard = {"NORMAL":[], "SUPER":[]}
            scoreboard[self.__session["level"]].append({"pseudo": self.__session['pseudo'],'score':self.__score})
        with open(scorepath, 'w') as file:
            file.write(json.dumps(scoreboard,indent = 4))
        self.testbouton.unbind(on_press=self.tryinput)
        self.testbouton.disabled = True
        self.unableinput()
        self.presscolortext.text = ''
        detele(savepath)
        self.writevalidate = False
        self.bare2.clear_widgets()
        winquitbutton = Button(text = 'QUIT')
        winquitbutton.bind(on_press= self.stope)
        self.bare2.add_widget(winquitbutton)
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='CONGRATULATIONS'))
        content.add_widget(Label(text=str(self.__session['pseudo'])))
        content.add_widget(Label(text='YOU WON'))
        content.add_widget(Label(text='Your score has been saved'))
        quitbutton = Button(text='QUIT')
        quitbutton.bind(on_press= self.stope)
        content.add_widget(quitbutton)
        winpopup = Popup(title = 'VICTORY', content = content,size_hint=(None,None), size=(300,300))
        winpopup.open()
    def _switchcolor(self,source):
        for i in colormatch:
            if source.background_color == colormatch[i]['code']:
                if i == (self.__nombrecouleurs-1):
                    source.background_color = colormatch[0]['code']
                    break
                else:
                    source.background_color = colormatch[i+1]['code']
                    break
    def colorcodeintoint(self, entry):
        result = []
        for i in entry:
            for x in colormatch:
                if colormatch[x]['code'] == i:
                    result.append(x)
                    break
        return result
    def stope(self,source):
        print('BIZARRE')
        try:
            detele(savepath)
        except:
            pass
        self.stop()
    def pseudoenter(self,source):
        self.errorstatus = False
        def test(source):
            if len(name.text) > 20 or len(name.text) < 5:
                if self.errorstatus == False:
                    content.add_widget(Label(text='Invalid input',size_hint=(1,0.1)))
                self.errorstatus = True
            else:
                self.currentpseudo = name.text
                self._gamelaunch(self)
                entry.dismiss()
        content = BoxLayout(orientation = 'vertical')
        entry = Popup(title = 'Enter pseudo', content = content, size_hint=(None,None), size=(500,500))
        pseudo = Label(text = 'PSEUDO :', font_size = 40, size_hint=(1,0.3))
        condition = Label(size_hint=(1,0.1), text= 'Between 5 and 20 chars', bold = True, font_size = 15)
        name = TextInput(size_hint=(1,0.4),multiline= False, on_text_validate=test, font_size = 60)
        validatebutton = Button(size_hint=(1,0.1), text ='GO')
        validatebutton.bind(on_press=test)
        content.add_widget(pseudo)
        content.add_widget(condition)
        content.add_widget(name)
        content.add_widget(validatebutton)
        entry.open()
    def unableinput(self):
        indice = 0
        for i in self.__combinaisonmaker.children:
            indice -= 1
            self.__combinaisonmaker.children[indice].disabled = True
Config.set('graphics', 'fullscreen', 'auto')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Mastermindgame().run()