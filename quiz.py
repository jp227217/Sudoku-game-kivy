import random as rnd
import pickle
import os

clear=lambda: os.system('cls')
class Question:
    def __init__(self):
        self.question=None
        self.options=None
        self.Ans=None
        self.choose=None

    def WriteQuestion(self):
        print("Enter Question:")
        self.question=input()
        self.options=input().split(' ')
        self.Ans=self.options[0]

    def ShuffleOptions(self):
        rnd.shuffle(self.options)

    def DisplayQuestion(self,i):
        print(i,'. ',self.question)
        print(*self.options,sep='\n')
        print('Ans  :',self.Ans,'\n')

    def QuestionOut(self):
        print(self.question)
        for i in range(len(self.options)):
            print(i+1,'. ',self.options[i])
        if self.choose != None:
            print('Choosed before :',self.choose)
        flag=True
        while flag:
            i=input()
            if i=='b' or i=='B':
                return 'B'
            elif i=='f' or i=='F':
                return 'F'
            elif i=='s' or i=='S':
                return 'S'
            try:
                i=int(i)
            except:
                continue
            if i>0 and i<=len(self.options):
                self.choose=i
                flag=False
        return 'N'
    def check(self):
        if self.choose==None:
            return None
        else:
            return self.options[self.choose-1]==self.Ans

class Quiz:
    def __init__(self):
        self.question_list=[]

    def Create(self):
        k=input('y\\n to add a question')
        while k=='y' or k=='Y':
            Q=Question()
            Q.WriteQuestion()
            self.question_list.append(Q)
            k=input('y\\n to add a question')

    def DisplayQuestions(self):
        for i in range(len(self.question_list)):
            self.question_list[i].DisplayQuestion(i+1)

    def PlayQuiz(self):
        n=len(self.question_list)
        rnd.shuffle(self.question_list)
        for i in self.question_list:
            i.choose=None
            rnd.shuffle(i.options)
        i=0
        while i>=0 and i<n:
            k=self.question_list[i].QuestionOut()
            if k=='B' and i>0:
                i-=1
            elif k=='F' and i<n-1:
                i+=1
            elif k=='S':
                break
            elif i<n-1:
                i+=1
    def Score(self):
        score=0
        notattempted=0
        k=None
        for i in self.question_list:
            k=i.check()
            if k==True:
                score+=1
            elif k==None:
                notattempted+=1
        return score,len(self.question_list),notattempted

    def DeleteQuestion(self):
        self.DisplayQuestions()
        print('Enter list of question numbers to remove seperated by only"," ')
        i=input()
        try:
            i=map(int,i.split(','))
        except:
            print('Try gain exit !!!!!')
        k=[]
        for j in range(len(self.question_list)):
            if j+1 not in i:
                k.append(self.question_list[j])
        self.questions_list=k
        print('Updated !!!')

    def ModifyQuiz(self):
        k=0
        while(True):
            print('1. Add new Questions\n2. Delete Questions\n3.Exit')
            k=input()
            try:
                k=int(input())
            except:
                continue
            if k==1:
                self.Create()
            elif k==2:
                self.DeleteQuestion()
            elif k==3:
                return
class Main:
    def __init__(self):
        self.Quiz_list=[]

    def Add_New(self):
        name=input('Enter name of the quiz')
        newQuiz=Quiz()
        newQuiz.Create()
        self.Quiz_list.append([name,newQuiz])

    def Delete(self):
        self.DisplayQuizList()
        k=input('Enter index of the quiz')
        try:
            k=int(k)
        except:
            print('Try again !!!!')
            return
        if k>0 and k<=len(self.Quiz_list):
            print('1. to delete whole quize \n2. questions from the quiz')
            a=input('Enter your choice')
            try:
                a=int(a)
            except:
                print('Try again !!!')
                return
            if a==2:
                self.Quiz_list[k-1][1].DeleteQuestion()
                print('Updated')
            if a==1:
                if k==1:
                    self.Quiz_list=self.Quiz_list[1:]
                elif k==len(self.Quiz_list):
                    self.Quiz_list=self.Quiz_list[:k-1]
                else:
                    self.Quiz_list=self.Quiz_list[:k-1]+self.Quiz_list[k:]
                print('Updated !!!')

    def DisplayQuizList(self):
        for i in range(len(self.Quiz_list)):
            print(i+1,'  .',self.Quiz_list[i][0])

    def DisplayQuiz(self):
        k=input('Enter no of the list')
        try :
            k=int(k)
        except:
            if k!='E' or k!='e':
                print('try again !!!')
            return
        if k>0 and k<=len(self.Quiz_list):
            self.Quiz_list[k-1][1].DisplayQuestions()

    def ModifyQuiz(self):
        self.DisplayQuizList()
        i=input('Enter no of the given list')
        try:
            i=int(i)
        except:
            input('Try agin !!!')
            return
        if i>0 and i<=len(self.Quiz_list):
            self.Quiz_list[i-1][1].ModifyQuiz()

    def Play(self):
        self.DisplayQuizList()
        i=input('Enter no of the given list')
        try:
            i=int(i)
        except:
            input('Try again !!!')
            return
        if i>0 and i<=len(self.Quiz_list):
            self.Quiz_list[i-1][1].PlayQuiz()
        Result=self.Quiz_list[i-1][1].Score()
        print('Quiz Name:'+self.Quiz_list[i-1][0])
        print('Score :'+str(Result[0])+'/'+str(Result[1]))
        print('NotAttempted :'+str(Result[2]),sep='\n')

    def Menu(self):
        i=0
        while(True):
            print('1. Add New Quiz','2. modify existing quiz','3. Delete Quiz','4. Display Quiz','5. Play Quiz','6. Exit',sep='\n')
            i=input()
            try:
                i=int(i)
                clear()
            except:
                continue
            if i not in range(1,7):
                continue
            if i==1:
                self.Add_New()
            elif i==2:
                self.ModifyQuiz()
            elif i==3:
                self.Delete()
            elif i==4:
                self.DisplayQuizList()
                self.DisplayQuiz()
                input()
            elif i==5:
                self.Play()
            elif i==6:
                break
            pickle_out = open('quiz.txt', 'wb')
            pickle.dump(self, pickle_out)
            pickle_out.close()
            clear()

if __name__=='__main__':
    M=Main()
    try:
        pickle_in=open('quiz.txt', 'rb')
        M=pickle.load(pickle_in)
    except:
        print('Error in database , Created new QuizList')
        M=Main()
    pickle_in.close()
    M.Menu()
    pickle_out = open('quiz.txt', 'wb')
    pickle.dump(M, pickle_out)
    pickle_out.close()
