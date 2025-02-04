from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from kivy.app import App
import matplotlib.pyplot as plt
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder

def detect(string):
    p=pd.read_csv("spam_ham_dataset.csv")
    label=p['label']
    text=p['text']
    x_train,x_test,y_train,y_test=train_test_split(text,label,test_size=0.25)
    sc = CountVectorizer()
    p1=sc.fit_transform(x_train)
    p2=sc.transform(x_test)
    m=SVC()
    q=m.fit(p1,y_train)
    i=q.predict(p2)
    o=[string]
    o1=sc.transform(o)
    i1=q.predict(o1)
    #print(accuracy_score(i,y_test))
    return i1
import imaplib
import email
def extract(mail,password,source):
    l2=[]
    username=mail
    app_password=password
    gmail_host='imap.gmail.com'
    mail=imaplib.IMAP4_SSL(gmail_host)
    mail.login(username,app_password)
    mail.select("INBOX")
    source1='(FROM '+'"'+source+'"'+')'
    _,selected_mails = mail.search(None,source1)
    l=selected_mails[0].split()
    l1=[]
    l2=[]
    for x in l:
        _,data=mail.fetch(x,'(RFC822)')
        _,bdata=data[0]
        e = email.message_from_bytes(bdata)
        for p in e.walk():
            if p.get_content_type()=="text/plain" or p.get_content_type()=="text/html":
                message = p.get_payload(decode=True)
                l1.append(message.decode())
                break
    for x in l1:
        i=detect(x)
        l2.append(i[0])
    l3=list(dict(Counter(l2)).values())
    print("Spam mails:",l3[0])
    print("Ham mails:",l3[1])
    label=["Spam","Ham"]
    y=np.array(l3)
    plt.pie(y,labels=label)
    plt.show()

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name',size=(10,10)))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='Password',size=(10,10)))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        self.add_widget(Label(text='Source Mail ID',size=(10,10)))
        self.source = TextInput(multiline=False)
        self.add_widget(self.source)
        self.print_info=Button(text="Click Here")
        self.print_info.bind(on_press=self.click_button)
        self.add_widget(self.print_info)
    def click_button(self,instance):
        extract(self.username.text,self.password.text,self.source.text)
        print(self.username.text)
        
        

class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
