from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
import pickle


Builder.load_string("""
<LeaderBoardScreen>:
    name:'LeaderBoard'   

<BButton>:
    on_release: app.root.mscreen.game.update(app.root.back)
    on_release: app.root.current=app.root.back               
""")
class BButton(Button):
    def __init__(self,**kwargs):
        super(BButton,self).__init__(**kwargs)
        
class LeaderBoardDetails:
    def __init__(self):
        self.l=list()
        self.read()
        self.k=None
        
    def read(self):
        pickle_in=open('leaderbord.txt','rb')
        try:
            self.l=pickle.load(pickle_in)
        except:
            self.reset()
        pickle_in.close()
    
    def write(self):
        pickle_out=open('leaderbord.txt','wb')
        pickle.dump(self.l,pickle_out)
        pickle_out.close()
    
    def reset(self,Value):
        self.l=list()
        for i in range(1,11):
            self.l.append([30,0,'Sudoku'])
        self.write()
    
    def Sort(self):
        k=list(map(lambda x:x[0]*60+x[1],self.l))
        for i in range(len(k)):
            for j in range(len(k)-1-i):
                if k[j]>k[j+1]:
                    k[j],k[j+1]=k[j+1],k[j]
                    self.l[j],self.l[j+1]=self.l[j+1],self.l[j]
        self.l=self.l[:10]
    def add_record(self,text):
        pickle_in=open('time.txt','rb')
        t=pickle.load(pickle_in)
        pickle_in.close()
        self.l.append([t[1],t[0],text])
        self.Sort()
        self.write()
    
        
class LeaderBoard(BoxLayout):
    def __init__(self,**kwargs):
        super(LeaderBoard,self).__init__(**kwargs)
        self.Details=LeaderBoardDetails()
        self.topGrid=BoxLayout()
        self.topGrid.orientation='horizontal'
        self.topGrid.add_widget(BButton(text='Back'))
        self.topGrid.add_widget(Button(text='Reset',on_press=self.Details.reset,on_release=self.reset))
        self.add_widget(self.topGrid)
        self.orientation='vertical'
        self.list_L=list()
        self.create()
        
    def reset(self,value):
        for i in range(10):
            self.list_L[i].text=str(i+1)+' '*10+str(self.Details.l[i][0])+':'+str(self.Details.l[i][1])+' '*10+self.Details.l[i][2]
    
    def create(self):
        for i in range(10):
            self.list_L.append(Label(text=str(i+1)+' '*10+str(self.Details.l[i][0])+':'+str(self.Details.l[i][1])+' '*10+self.Details.l[i][2]))
            self.add_widget(self.list_L[-1])
    def reload(self,Value,text):
        if Value==False or text==None or text==len(text)*' ':
            return 
        self.Details.add_record(text)
        self.Details.Sort()
        for i in range(10):
            self.list_L[i].text=str(i+1)+' '*10+str(self.Details.l[i][0])+':'+str(self.Details.l[i][1])+' '*10+self.Details.l[i][2]
            
class LeaderBoardScreen(Screen):
    def __init__(self,**kwargs):
        super(LeaderBoardScreen,self).__init__(**kwargs)
        self.LB=LeaderBoard()
        self.add_widget(self.LB)
        
class MyApp(App):
    def build(self):
        return LeaderBoardScreen()
    
if __name__=='__main__':
    MyApp().run()
    