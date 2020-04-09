from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from sudoko import Sudoko
import pickle

Builder.load_string("""

<WelcomeScreen>:
    name:'welcome'

<Welcome>:
    canvas.before:
        Rectangle:
            pos:self.pos
            size:self.size
            source:'background.jpg'
<MyButton>:
    on_release: app.root.current='Game'
""")

class MyButton(Button):
    def __init__(self,**kwargs):
        super(MyButton,self).__init__(**kwargs)


class Welcome(FloatLayout):
    def __init__(self,**kwargs):
        super(Welcome,self).__init__(**kwargs)
        self.add_widget(MyButton(text='New game',size_hint=(.2,.08),pos_hint={'x':.7,'y':.8},markup=True,on_press=self.new_game))
        self.add_widget(MyButton(text='Continue',size_hint=(.2,.08),pos_hint={'x':.75,'y':.7},markup=True,on_press=self.Continue))

    def Continue(self,Value):
        pass

    def new_game(self,Value):
        s= Sudoko()
        pickle_out = open('sudoko.txt', 'wb')
        pickle.dump(s, pickle_out)
        pickle_out.close()

class WelcomeScreen(Screen):
    def __init__(self,**kwargs):
        super(WelcomeScreen,self).__init__(**kwargs)
        self.add_widget(Welcome())

class MyApp(App):
    def build(self):
        return WelcomeScreen()

if __name__=='__main__':
    MyApp().run()
