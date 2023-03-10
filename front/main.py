from kivy.app import App
import ast
import requests
from kivy.uix.gridlayout import GridLayout
import json
from kivy.uix.textinput import TextInput
from functools import partial
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class Miney_Client(GridLayout):
    def __init__(self, **kwargs):
        super(Miney_Client, self).__init__(**kwargs)
        self.padding=0
        self.layout = BoxLayout(spacing=10, orientation = 'vertical',padding=10)
        self.rows = 2
        self.cols = 2
        self.add_widget(self.layout)
        self.i = -1
        self.tag = []
        self.btnarr = []
        self.seltagArr = []
        self.sel = 0
        self.threshold = 16
        self.deskname   = TextInput(text="Miney-Deploy",size_hint=(.7,.7))
        self.layout.add_widget( self.deskname)
        self.username   = TextInput(text="USERNAME",size_hint=(.7,.7))
        self.layout.add_widget( self.username)
        self.password   = TextInput(hint_text="Miney-Deploy",text="PASSWORD",password=True,size_hint=(.7,.7),)
        self.layout.add_widget( self.password)
        self.btn_start = Button(text="Create Container",size_hint=(.7,.7))
        self.btn_start.bind(on_press=self.onCreatePress)
        self.layout.add_widget(self.btn_start)
        self.btn_delete = Button(text="Delete Container",size_hint=(.7,.7))
        self.layout.add_widget(self.btn_delete)
        self.spinlock = False
        self.btn_sync = Button(text="Sync Data",size_hint=(.7,.7))
        self.btn_sync.bind(on_press=self.syncOnclick)
        self.layout.add_widget(self.btn_sync)
        self.r = Button(text="Register",size_hint=(.7,.7))
        self.r.bind(on_press=self.register)
        self.layout.add_widget(self.r)
    def syncOnclick(self,instance):
        try:
            response = requests.get('http://daegu.yjlee-dev.pe.kr:32000/request?'+username+'&'+password+'&', timeout = 1).text
            if len(response):
                response = json.loads(response)
            for resp in response:
                self.i+=1
                resp = str(resp)
                resp = json.loads(resp,strict=False)
                self.tag.append(resp)
                self.seltagArr.append(resp.get("tag"))
                self.tmp = globals()['self.btn{}'.format(self.i)]=Button(text="Select "+ self.tag[self.i].get("servername")+":"+"(Port:" +self.tag[self.i].get("serverport")+")"+ " Now",size_hint=(.7,.7))
                self.ids["tag"]=self.seltagArr[self.i]
                self.tmp.bind(on_press = self.onSelectPress)
                self.btnarr.append(self.tmp)
                self.layout.add_widget(self.tmp)
                self.btn_delete.bind(on_press=self.onDeletePress)
        except:
            print("no json")

    def onCreatePress(self,instance):
        try:
            if self.spinlock:
                pass
            if self.i>self.threshold:
                print('No more space available here. Contact on yoonjin67@gmail.com')
                self.spinlock = False
                pass
            self.i+=1
            self.spinlock = True
            self.name = self.deskname.text
            password = self.password.text
            username = self.username.text
            r = requests.post ('http://daegu.yjlee-dev.pe.kr:32000/create', json = { "server-name" : self.name, "gamemode" : "creative", "force-gamemode" : True, "difficulty" : "easy", "allow-cheat" : True, "max-players" : 100, "online-mode" : True, "white-list" : False, "server-port" : 19132, "server-portv6" : 19133, "view-distance" : 32, "tick-distance" : 4, "player-idle-timeout" : 30, "max-threads" : 8, "level-name" : "Bedrock level", "level-seed" : "MineCraftX", "default-player-permission-level" : "operator", "texturepack-required" : False, "content-log-file-enabled" : True, "compression-threshold" : 20, "server-authoritative-movement" : "server-auth", "player-movement-score-threshold" : 0.85, "player-movement-distance-threshold" : 0.7, "player-movement-duration-threshold-in-ms" : 500, "correct-player-movement" : True, "server-authoritative-block-breaking" : True }, auth = (password,username))
            resp = globals()['jsondata'.format(self.i)]=r.json()
            self.tag.append(resp)
            self.seltagArr.append(resp.get("tag"))
            self.tmp = globals()['self.btn{}'.format(self.i)]=Button(text="Select "+ self.tag[self.i].get("servername")+":"+"(Port:" +self.tag[self.i].get("serverport")+")"+ " Now",size_hint=(.7,.7))
            self.ids["tag"]=self.seltagArr[self.i]
            self.tmp.bind(on_press = self.onSelectPress)
            self.btnarr.append(self.tmp)
            self.layout.add_widget(self.tmp)
            self.spinlock = False
        except:
            print("not registered")
            self.i-=1
            
    def register(self,instance):
            username = self.username.text
            password = self.password.text
            r = requests.get ('http://daegu.yjlee-dev.pe.kr:32000/register', auth = (password,username))
        
    def onDeletePress(self,instance):
        if self.spinlock:
            return
        if self.i==-1:
            return
        try:
            self.spinlock = True
            r = requests.post('http://daegu.yjlee-dev.pe.kr:32000/delete', data=self.seltagArr[self.sel])
            wid = self.btnarr[self.sel]
            wid.parent.remove_widget(wid)
            self.tag.remove(self.tag[self.sel])
            self.i-=1
            self.sel-=1
            self.spinlock = False
        except:
            self.spinlock = False
    def onSelectPress(self,instance):
            i = self.seltagArr.index(self.ids["tag"])
            self.sel = i
class Miney_App(App):
    def build(self):
        return Miney_Client()

Miney_App().build()
Miney_App().run()

