from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder

Builder.load_string("""
<EButton>:
    on_release:app.root.LBScreen.LB.reload(app.root.mscreen.game.SudokoBox.Correct,app.root.mscreen.game.SudokoBox.text)                    
""")

class EButton(Button):
    def __init__(self,**kwargs):
        super(EButton,self).__init__(**kwargs)
        
class PopGrid(GridLayout):
    def __init__(self,**kwargs):
        super(PopGrid,self).__init__(**kwargs)
        self.cols=1
        self.rows=3
        self.add_widget(Label(text='Enter your Name'))
        self.Ip=TextInput(multiline=False,hint_text='name')
        self.add_widget(self.Ip)
        self.btn=EButton(text="Enter")
        self.add_widget(self.btn)
        
class Main(GridLayout):
    def __init__(self,**kwargs):
        super(Main,self).__init__(**kwargs)
        self.Show=None
        self.popup_window=None
        self.text=None
        self.show_popup()
        
    def show_popup(self,*args):
        self.Show = PopGrid()
        self.Show.btn.on_press=self.close_popup
        self.popup_window=Popup(title='You Won',content=self.Show,size_hint=(None,None),size=(200,200))
        self.popup_window.open()
        
    def close_popup(self,*args):
        self.text=self.Show.Ip.text
        print(self.text)
        k=len(self.text)
        if self.text==None or self.text==' '*k:
            return 
        self.popup_window.dismiss()
        
class MyApp(App):
    def build(self):
        return Main()

if __name__=='__main__':
    MyApp().run()