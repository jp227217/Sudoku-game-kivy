from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from game import Game
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import pickle
from sudoko import Sudoko
from sudokoGui import MyGridLayoutWhite
from leaderbord import LeaderBoardScreen

Builder.load_string("""
<ScreenManagement>:
    WelcomeScreen:

<MainScreen>:
    name:'Game'
    Game:

<WelcomeScreen>:
    name:'welcome'
    Welcome:

<Welcome>:
    canvas.before:
        Rectangle:
            pos:self.pos
            size:self.size
            source:'background.jpg'

<MButton>:
    on_release: app.root.press()

<ExitButton>:
    on_release: app.stop()

<BackButton>:
    on_release: app.root.current='welcome'
    text:'Back'

<LButton>:
    on_press: app.root.back=app.root.current
    on_release: app.root.current='LeaderBoard'

""")
class LButton(Button):
    def __init__(self,**kwargs):
        super(LButton,self).__init__(**kwargs)

class BackButton(Button):
    pass

class ExitButton(Button):
    def __init__(self,**kwargs):
        super(ExitButton,self).__init__(**kwargs)
class MButton(Button):
    def __init__(self,**kwargs):
        super(MButton,self).__init__(**kwargs)

class Welcome(FloatLayout):
    def __init__(self,**kwargs):
        super(Welcome,self).__init__(**kwargs)
        self.add_widget(MButton(text='New game',size_hint=(.2,.08),pos_hint={'x':.7,'y':.9},on_release=self.new_game))
        self.add_widget(MButton(text='Continue',size_hint=(.2,.08),pos_hint={'x':.75,'y':.8}))
        self.add_widget(ExitButton(text='Exit',size_hint=(.2,.08),pos_hint={'x':.75,'y':.6}))
        self.add_widget(LButton(text='Leader Board',size_hint=(.2,0.08),pos_hint={'x':.7,'y':.7}))

    def new_game(self,Value):
        pickle_out = open('time.txt', 'wb')
        pickle.dump([0,0], pickle_out)
        pickle_out.close()

        pickle_out=open('sudoko.txt','wb')
        pickle.dump(Sudoko(),pickle_out)
        pickle_out.close()


class WelcomeScreen(Screen):
    pass

class MainScreen(Screen):
    def __init__(self,**kwargs):
        super(MainScreen,self).__init__(**kwargs)
        self.MainGrid=MyGridLayoutWhite(cols=1,rows=2)
        self.game=Game(size_hint_y=self.MainGrid.size[1]*(9/10))
        self.screenGrid=GridLayout(cols=3,rows=1,size_hint_y=self.MainGrid.size[1]/10)
        self.screenGrid.add_widget(BackButton(on_press=self.Back))
        self.screenGrid.add_widget(LButton(text='Leader Board',on_press=self.Back))
        self.screenGrid.add_widget(ExitButton(text='Exit'))
        self.MainGrid.add_widget(self.game)
        self.MainGrid.add_widget(self.screenGrid)
        self.add_widget(self.MainGrid)

    def Back(self,Value):
        if self.game.SudokoBox.pause==False and self.game.pauseButton.text=='Pause':
            self.game.update(Value)
        self.game.Save(1)

class ScreenManagement(ScreenManager):
    def __init__(self,**kwargs):
        super(ScreenManagement,self).__init__(**kwargs)
        self.mscreen=MainScreen()
        self.LBScreen=LeaderBoardScreen()
        self.add_widget(self.mscreen)
        self.add_widget(self.LBScreen)
        self.back='welcome'

    def press(self):
        self.mscreen.game.reload()
        self.current='Game'

class MainApp(App):
    def build(self):
        sc=ScreenManagement()
        sc.current='welcome'
        return sc

if __name__=='__main__':
    MainApp().run()
