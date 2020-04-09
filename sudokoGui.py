from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from sudoko import Sudoko
from kivy.uix.label import Label
import pickle
from kivy.uix.popup import Popup
from popup import PopGrid
from kivy.app import App

Builder.load_string("""
<MyGridLayoutBlack>:
    canvas.before:
        Color:
            rgb: 0,0,0
        Rectangle:
            size:self.size
            pos:self.pos
""")
class MyGridLayoutBlack(GridLayout):
    pass
Builder.load_string("""
<MyGridLayoutWhite>:
    canvas.before:
        Color:
            rgb: 1,1,1
        Rectangle:
            size:self.size
            pos:self.pos

<MyButton>:
    on_release:app.root.mscreen.game.update(app.root.mscreen.game.SudokoBox.Correct)
""")
class MyGridLayoutWhite(GridLayout):
    def __init__(self,**kwargs):
        super(MyGridLayoutWhite,self).__init__(**kwargs)

# MyButton
class MyButton(Button):
    def __init__(self,i,j,**kwargs):
        super(MyButton,self).__init__(**kwargs)
        self.i=i

# My ToggleButton
class MyToggleButton(ToggleButton):
    def __init__(self, i, j, **kwargs):
        super(MyToggleButton, self).__init__(**kwargs)
        self.i = i
        self.j = j
        self.temptext=' '
        self.num=self.text
        self.mutable=True
        self.Correct=False
    def yellow(self,value):
        self.font_size=30
        self.text='[color=ffff00]'+value+'[/color]'
        self.num=value
    def red(self,value):
        self.text='[color=ff0000]'+value+'[/color]'
        self.num=value
    def orginal(self,value):
        if self.mutable==False:
            self.yellow(value)
            return
        self.font_size=40
        self.text=value
        self.num=value


# Box to create Sudoko Box
class Box(GridLayout):
    def __init__(self,**kwargs):
        super(Box,self).__init__(**kwargs)
        self.cols=1
        self.rows=3
        self.SudokoBox=None
        self.button=None
        self.list_buttons=[]
        self.list_number=[]
        self.resume_pause=Button()
        self.pause=True
        self.create()
        self.Correct=False
        self.Show=None
        self.popup_window=None
        self.text=None

    # chossing a button
    def press(self,Value):
        if self.pause==True:
            self.button=Value
            return
        if self.button==Value:
            self.button=None
        else:
            self.button=Value

    # number to insert a value in the box
    def NumPressed(self,Value,reload=False):
        if self.pause==True or self.button==None:
            return
        if self.button.mutable==False:
            return
        elif self.button.num==' ':
            self.SudokoBox.values[self.button.i,self.button.j]=str(Value.i)
            self.highlight(self.button.i,self.button.j,str(Value.i),reload)

        elif self.button.num==str(Value.i):
            self.SudokoBox.values[self.button.i,self.button.j]=' '
            self.button.orginal(' ')
            l=self.SudokoBox.check(self.button.i,self.button.j,str(Value.i))
            for i in l:
                self.highlight(i[0],i[1],str(Value.i),reload)
        elif self.button.num!=str(Value.i):
            n=self.SudokoBox.values[self.button.i, self.button.j]
            self.SudokoBox.values[self.button.i, self.button.j] = ' '
            self.button.orginal(' ')
            l =self.SudokoBox.check(self.button.i, self.button.j,n)
            for i in l:
                self.highlight(i[0], i[1], n,reload)
            self.SudokoBox.values[self.button.i, self.button.j] = str(Value.i)
            self.highlight(self.button.i, self.button.j, str(Value.i),reload)

    def Save(self):
        pickle_out = open('sudoko.txt', 'wb')
        pickle.dump(self.SudokoBox, pickle_out)
        pickle_out.close()

    def highlight(self,i,j,n,reload):
        l=self.SudokoBox.check(i,j,n)
        if len(l)==1:
            self.list_buttons[l[0][0]][l[0][1]].orginal(n)
            self.list_buttons[l[0][0]][l[0][1]].Correct=True
            self.check(reload)
        else :
            for k in l:
                self.list_buttons[k[0]][k[1]].red(n)
                self.list_buttons[k[0]][k[1]].Correct=False

    # to create the sudoko box
    def create(self):
        Grid=[]
        for i in range(3):
            Grid.append([])
            for j in range(3):
                Grid[-1].append(GridLayout(cols=3,rows=3))
        for i in range(9):
            self.list_buttons.append([])
            for j in range(9):
                self.list_buttons[-1].append(MyToggleButton(i=i,j=j,group='ans',on_press=self.press,markup=True))
                Grid[i // 3][j // 3].add_widget(self.list_buttons[i][j])
        G =MyGridLayoutBlack(cols=3, rows=3, spacing=3)
        for i in Grid:
            for j in i:
                G.add_widget(j)
        size_G=MyGridLayoutWhite(cols=3,rows=3,size_hint_y=self.size[1]*(8/10))
        G.size_hint_x=size_G.size[0]*(8/10)
        G.size_hint_y=size_G.size[1]*(12/14)
        size_G.add_widget(Label(size_hint_y=size_G.size[1]/14,size_hint_x=self.size[0]/16))
        size_G.add_widget(Label(size_hint_y=size_G.size[1]/14))
        size_G.add_widget(Label(size_hint_y=size_G.size[1]/14,size_hint_x=self.size[0]/16))
        size_G.add_widget(Label(size_hint_x=size_G.size[0]/16))
        size_G.add_widget(G)
        size_G.add_widget(Label(size_hint_x=size_G.size[0]/16))
        size_G.add_widget(Label(size_hint_y=size_G.size[1]/14,size_hint_x=self.size[0]/16))
        size_G.add_widget(Label(size_hint_y=size_G.size[1]/14))
        size_G.add_widget(Label(size_hint_y=size_G.size[1]/14,size_hint_x=self.size[0]/16))
        self.add_widget(size_G)
        G=MyGridLayoutWhite(cols=9,rows=1,padding=2)
        for i in range(1,10):
            self.list_number.append(MyButton(i=i,j=-1,text='[color=000000]'+str(i)+'[/color]',markup=True,on_press=self.NumPressed,background_color=[255,255,255,255]))
            G.add_widget(self.list_number[-1])
        G.size_hint_y=self.size[1]/10
        self.add_widget(G)

    def swap(self):
        for i in self.list_buttons:
            for j in i:
                t=j.text
                j.text=j.temptext
                j.temptext=t

    def reset(self,reload):
        if reload==False:
            self.SudokoBox.values[:,:]=' '
        for i in range(9):
            for j in range(9):
                if self.SudokoBox.que[i,j]==' ':
                    self.list_buttons[i][j].mutable=True
                else:
                    self.list_buttons[i][j].mutable=False
                self.list_buttons[i][j].orginal(self.SudokoBox.que[i,j])
        if reload==True:
            tempButton=self.button
            for i in range(9):
                for j in range(9):
                    if self.SudokoBox.values[i,j]!=' ':
                        self.button=self.list_buttons[i][j]
                        self.NumPressed(self.list_number[int(self.SudokoBox.values[i,j])-1],reload)
            k=self.check(reload)
            self.button=tempButton
            return k
        return True

    def NewGame(self):
        self.SudokoBox=Sudoko()
        self.Save()
        self.reset(False)

    def reload(self):
        pickle_in= open('sudoko.txt', 'rb')
        try:
            self.SudokoBox=pickle.load(pickle_in)
        except:
            self.SudokoBox=Sudoko()
            self.Save()
        pickle_in.close()
        return self.reset(True)

    def check(self,reload):
        self.Correct=False
        flag=True
        for i in range(9):
            for j in range(9):
                if self.list_buttons[i][j].mutable:
                    if self.list_buttons[i][j].Correct==False:
                        flag=False
                        break
        if flag==False:
            return
        elif flag==True and reload==True:
            return False
        elif flag==True and reload==False:
            self.Correct=flag
            self.Save()
            print(flag,reload)
            self.show_popup(reload)
            return
        return True

    def show_popup(self,reload,*args):
        if reload==True:
            return
        self.Show = PopGrid()
        self.Show.btn.on_press=self.close_popup
        self.popup_window=Popup(title='You Won',content=self.Show,size_hint=(None,None),size=(200,200))
        self.popup_window.open()

    def close_popup(self,*args):
        self.text=self.Show.Ip.text
        k=len(self.text)
        if self.text==None or self.text==' '*k:
            return
        self.popup_window.dismiss()

class MyApp(App):
    def build(self):
        return Box()

if __name__=='__main__':
    MyApp().run()
