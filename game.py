from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from sudokoGui import Box
from kivy.clock import Clock
from kivy.app import App
import pickle
Builder.load_string("""
<MyGridLayout>:
    canvas.before:
        Color:
            rgb: 1,1,1
        Rectangle:
            size:self.size
            pos:self.pos
""")

class MyGridLayout(GridLayout):
    pass

# Time label
class MyTimeLabel(Label):
    def __init__(self,**kwargs):
        super(MyTimeLabel,self).__init__(**kwargs)
        self.text=''
        self.markup=True
        self.sec=0
        self.min=0
        self.unit=0
        self.Load()
        Clock.schedule_interval(self.updateTime, 1)

    def updateTime(self,*args):
        self.sec+=self.unit
        if self.sec==60:
            self.sec=0
            self.min+=1
        self.text ='[color=000000]'+str(self.min)+' : '+str(self.sec)+'[/color]'
        self.Save()
    
    def Save(self):
        pickle_out = open('time.txt', 'wb')
        pickle.dump([self.sec,self.min], pickle_out)
        pickle_out.close()
    
    def Load(self):
        pickle_in= open('time.txt', 'rb')
        try:
            k=pickle.load(pickle_in)
            self.sec=k[0]
            self.min=k[1]
        except:
            self.sec=0
            self.min=0
        pickle_in.close()

class Game(GridLayout):
    def __init__(self,**kwargs):
        super(Game,self).__init__(**kwargs)
        self.cols=1
        self.rows=2
        self.SudokoBox = Box(size_hint_y=self.size[1] * (9 / 10))
        self.time=MyTimeLabel()
        G=MyGridLayout(cols=5,rows=1,size_hint_y=self.size[1]/10)
        G.add_widget(Button(text='NewGame',on_release=self.NewGame))
        G.add_widget(Button(text='Save',on_release=self.Save))
        G.add_widget(self.time)
        self.pauseButton=Button(text='Resume',on_release=self.update)
        G.add_widget(self.pauseButton)
        G.add_widget(Button(text='Reset',on_release=self.reset))
        self.add_widget(G)
        self.add_widget(self.SudokoBox)

    def reset(self,Value):
        if self.SudokoBox.pause==True:
            self.update(self.pauseButton)
        self.SudokoBox.reset(False)

    def update(self,Value):
        if self.pauseButton.text=='Won':
            return
        if Value=='welcome':
            return
        if Value==True:
            self.pauseButton.text='Won'
            self.time.unit = 0
            return
        elif Value==False:
            return
        if self.pauseButton.text == 'Pause':
            self.time.unit = 0
            self.pauseButton.text = 'Resume'
            self.SudokoBox.pause = True
            self.SudokoBox.swap()
        elif self.pauseButton.text == 'Resume':
            self.time.unit = 1
            self.pauseButton.text = 'Pause'
            self.SudokoBox.pause = False
            self.SudokoBox.swap()
        
    def reload(self):
        if self.pauseButton.text=='Won':
            self.NewGame(1)
            return
        if self.SudokoBox.pause==True:
            self.update(self.pauseButton)
        k=self.SudokoBox.reload()
        if k==False:
            self.NewGame(True)
        else :
            self.time.Load()

    def Save(self,Value):
        self.SudokoBox.Save()
    
    def NewGame(self,Value):
        if self.pauseButton.text=='Won':
            self.pauseButton.text='Pause'
            self.SudokoBox.pause=False
            
        if self.SudokoBox.pause==True:
            self.update(self.pauseButton)
        self.SudokoBox.NewGame()
        self.time.sec=0
        self.time.min=0
        self.time.unit=1
        
class MyApp(App):
    def __init__(self,**kwargs):
        super(MyApp,self).__init__(**kwargs)
        self.game=Game()
    def build(self):
        return self.game

if __name__=='__main__':
    app=MyApp()
    app.game.reload()
    app.run()