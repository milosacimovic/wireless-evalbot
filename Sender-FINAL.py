# -*- coding: utf-8 -*-
import tkinter
from tkinter import *
import socket
from time import sleep

class App():
    def __init__(self,master):

        self.connected = 0
        self.senderSocket = None
        self.successfull = 0
        self.targetIP=""
        self.heldDown=[0,0,0,0,0,0]
        self.master=master
        master.protocol("WM_DELETE_WINDOW", self.end)
        master.wm_title("Controller")
        master.resizable(0,0)
        
        masterFrame= Frame(master,bg="white")
        masterFrame.pack()
        
        frameTraka= Frame(masterFrame)
        frameTraka.grid(row=1, column=1,columnspan=3)
        
        frame = Frame(masterFrame,bg="white")
        frame.grid(row=2, column=2)  
       
        frameSpeed1 = Frame(frame,bg="white")
        frameSpeed1.grid(row=2, column=1)
          
        frameSpeed2 = Frame(frame,bg="white")
        frameSpeed2.grid(row=2, column=2)  
        
        frameButtons= Frame(masterFrame,bg="white")
        frameButtons.grid(row=2, column=1,padx=50,pady=15) 
        
        frameRotate= Frame(frameButtons,bg="white")
        frameRotate.grid(row=5, column=3) 
        
        
        self.speed=0
        self.main = Text(frameTraka,width=15,height=1,bd=6,bg="firebrick")
        self.main.grid(row=1,column=1)
        
        self.con= Button(frameTraka,text="Connect",width=15,height=1,command=self.connect_press,state="normal",bg="white",bd=4)
        self.con.grid(row=1,column=2)
        self.disc=Button(frameTraka,text="Disconnect",width=15,height=1,command=self.disconnect_press,state="disabled",bg="white",bd=4)
        self.disc.grid(row=1,column=3)

        
        self.speed_inc_button=Button(frameSpeed1, text="Increase",width=7,height=1,command=self.speed_inc,bd=1,bg="white")
        self.speed_inc_button.grid(row=2, column=1,pady=4)
        self.speed_lab=Label(frameSpeed1, text="  0  ",relief=GROOVE,bg="white",height=1,fg="black",width=7,bd=3)
        self.speed_lab.grid(row=3, column=1,pady=4)
        self.speed_dec_button=Button(frameSpeed1, text="Decrease",width=7,height=1,command=self.speed_dec,bd=1,bg="white")
        self.speed_dec_button.grid(row=4, column=1,pady=4)

        
        self.w= Button(frameButtons, text="↑",width=4,height=2,bd=3,bg="white")
        self.w.grid(row=4, column=3)
        self.a= Button(frameButtons, text="←",width=4,height=2,bd=3,bg="white")
        self.a.grid(row=5, column=2)
        self.s= Button(frameButtons, text="↓",width=4,height=2,bd=3,bg="white")
        self.s.grid(row=6, column=3)
        self.d= Button(frameButtons, text="→",width=4,height=2,bd=3,bg="white")
        self.d.grid(row=5, column=4)
        self.rr= Button(frameRotate, text="↻",width=1,height=2,bd=3,bg="white")
        self.rr.grid(row=1,column=2)
        self.rl= Button(frameRotate, text="↺",width=1,height=2,bd=3,bg="white")
        self.rl.grid(row=1,column=1)
       
       
        Label(frameSpeed1, text="Speed:",relief=GROOVE,bg="white",height=1,fg="black",width=7,bd=3).grid(row=1, column=1,pady=4)
        
        self.bSpeed1=Label(frameSpeed2, text="",width=2,height=1,bg="silver")
        self.bSpeed1.grid(row=1,column=2,padx=10,pady=2)
        self.bSpeed2=Label(frameSpeed2, text="",width=2,height=1,bg="silver")
        self.bSpeed2.grid(row=2,column=2,pady=2)
        self.bSpeed3=Label(frameSpeed2, text="",width=2,height=1,bg="silver")
        self.bSpeed3.grid(row=3,column=2,pady=2)
        self.bSpeed4=Label(frameSpeed2, text="",width=2,height=1,bg="silver")
        self.bSpeed4.grid(row=4,column=2,pady=2)
        self.bSpeed5=Label(frameSpeed2, text="",width=2,height=1,bg="silver")
        self.bSpeed5.grid(row=5,column=2,pady=2)
        self.bSpeed6=Label(frameSpeed2, text="",width=2,height=1,bg="silver")
        self.bSpeed6.grid(row=6,column=2,pady=2)
        self.bSpeed7=Label(frameSpeed2, text="",width=2,height=1,bg="silver")
        self.bSpeed7.grid(row=7,column=2,pady=2)
        self.bSpeed8=Label(frameSpeed2, text="",width=2,height=1,bg="silver")
        self.bSpeed8.grid(row=8,column=2,pady=2)
        self.bSpeed9=Label(frameSpeed2, text="",width=2,height=1,bg="silver")
        self.bSpeed9.grid(row=9,column=2,pady=2)
        self.bSpeed10=Label(frameSpeed2, text="",width=2,height=1,bg="silver")
        self.bSpeed10.grid(row=10,column=2,pady=2)
        
        master.bind('e',self.speed_inc)
        master.bind('q',self.speed_dec)
        master.bind("<KeyRelease>", self.keyup)
        master.bind("<KeyPress>", self.keydown)
        
        self.w.bind("<ButtonPress>", self.up_press)
        self.w.bind("<ButtonRelease>", self.up_release)
        self.a.bind("<ButtonPress>", self.left_press)
        self.a.bind("<ButtonRelease>", self.left_release)
        self.s.bind("<ButtonPress>", self.down_press)
        self.s.bind("<ButtonRelease>", self.down_release)
        self.d.bind("<ButtonPress>", self.right_press)
        self.d.bind("<ButtonRelease>", self.right_release)
        self.rr.bind("<ButtonPress>", self.rr_press)
        self.rr.bind("<ButtonRelease>", self.rr_release)
        self.rl.bind("<ButtonPress>", self.rl_press)
        self.rl.bind("<ButtonRelease>", self.rl_release)

    
    def keydown(self,event=None):
        inst=event.keysym
        if inst == "a" :
            if(self.heldDown[4]==0):
                self.heldDown[4]=1
                self.rl_press()
        if inst == "d" :
            if(self.heldDown[5]==0):
                self.heldDown[5]=1
                self.rr_press()
        if inst == "Up" :
            if(self.heldDown[0]==0):
                self.heldDown[0]=1
                self.up_press()
        if inst == "Left" :
            if(self.heldDown[1]==0):
                self.heldDown[1]=1
                self.left_press()   
        if inst == "Down" :
            if(self.heldDown[2]==0):
                self.heldDown[2]=1
                self.down_press() 
        if inst == "Right" :
            if(self.heldDown[3]==0):
                self.heldDown[3]=1
                self.right_press()          
                                


    def keyup(self,event=None):
        inst= event.keysym
        if inst== "a":
            self.heldDown[4]=0
            self.rl_release()
        if inst== "d":
            self.heldDown[5]=0
            self.rr_release()
        if inst== "Up":
            self.heldDown[0]=0
            self.up_release()
        if inst== "Left":
            self.heldDown[1]=0
            self.left_release()
        if inst== "Down":
            self.heldDown[2]=0
            self.down_release()
        if inst== "Right":
            self.heldDown[3]=0
            self.right_release()
    
    def connect_press(self,event=None):
        self.senderSocket = socket.socket()
        self.targetIP=self.main.get(0.1,END)
        self.successfull = self.senderSocket.connect_ex((self.targetIP, 4001))
        if self.successfull == 0:
            self.connected = 1
            self.main.config(state="disabled")
            self.main.config(bg='lightgreen')
            self.disc.config(state="normal")
            self.con.config(state="disabled")
            self.speed=5;
            self.speed_lab.config(text=(" " + str(self.speed) + " "))
            self.bSpeed10.config(bg="darkgreen")
            self.bSpeed9.config(bg="forestgreen")
            self.bSpeed8.config(bg="yellowgreen")
            self.bSpeed7.config(bg="lawngreen")
            self.bSpeed6.config(bg="greenyellow")
        else:
           self.senderSocket.close()

    def disconnect_press(self,event=None):
        self.main.config(bg='firebrick')
        self.main.config(state="normal")
        self.con.config(state="normal")
        self.disc.config(state="disabled")
        try:
            self.senderSocket.send("_end_".encode())
        except BaseException:
            self.master.destroy()
        self.senderSocket.close()
        self.senderSocket = None
        self.connected = 0
        self.speed=0
        self.speed_lab.config(text=(" " + str(self.speed) + " "))
        self.bSpeed1.config(bg="silver")
        self.bSpeed2.config(bg="silver")
        self.bSpeed3.config(bg="silver")
        self.bSpeed4.config(bg="silver")
        self.bSpeed5.config(bg="silver")
        self.bSpeed6.config(bg="silver")
        self.bSpeed7.config(bg="silver")
        self.bSpeed8.config(bg="silver")
        self.bSpeed9.config(bg="silver")
        self.bSpeed10.config(bg="silver")
        
        
    def speed_inc(self,event=None):
        if (self.speed < 10):
           if self.connected == 1:
                self.senderSocket.send("_increase_speed_".encode())
                self.speed=self.speed+1
                self.speed_lab.config(text=(" " + str(self.speed) + " "))
                if self.speed==1 :
                    self.bSpeed10.config(bg="darkgreen")
                if self.speed==2 :
                    self.bSpeed9.config(bg="forestgreen")
                if self.speed==3 :
                    self.bSpeed8.config(bg="yellowgreen")
                if self.speed==4 :
                    self.bSpeed7.config(bg="lawngreen")
                if self.speed==5 :
                    self.bSpeed6.config(bg="greenyellow")
                if self.speed==6 :
                    self.bSpeed5.config(bg="yellow")
                if self.speed==7 :
                    self.bSpeed4.config(bg="gold")
                if self.speed==8 :
                    self.bSpeed3.config(bg="orange")
                if self.speed==9 :
                    self.bSpeed2.config(bg="darkorange")
                if self.speed==10 :
                    self.bSpeed1.config(bg="chocolate")
        sleep(0.2)

    def speed_dec(self,event=None):
        if (self.speed > 0):
            if self.connected == 1:
                self.senderSocket.send("_decrease_speed_".encode())
                self.speed=self.speed-1
                self.speed_lab.config(text=(" " + str(self.speed) + " "))
                if self.speed==0 :
                    self.bSpeed10.config(bg="silver")
                if self.speed==1 :
                    self.bSpeed9.config(bg="silver")
                if self.speed==2 :
                    self.bSpeed8.config(bg="silver")
                if self.speed==3 :
                    self.bSpeed7.config(bg="silver")
                if self.speed==4 :
                    self.bSpeed6.config(bg="silver")
                if self.speed==5 :
                    self.bSpeed5.config(bg="silver")
                if self.speed==6 :
                    self.bSpeed4.config(bg="silver")
                if self.speed==7 :
                    self.bSpeed3.config(bg="silver")
                if self.speed==8 :
                    self.bSpeed2.config(bg="silver")
                if self.speed==9 :
                    self.bSpeed1.config(bg="silver")
        sleep(0.2)

    def up_press(self,event=None):
        if self.connected == 1:
            self.senderSocket.send("_forward_".encode())
            sleep(0.2)
    def up_release(self,event=None):
        self.senderSocket.send("_stop_".encode())
        
    def down_press(self,event=None):
        if self.connected == 1:
            self.senderSocket.send("_backward_".encode())
            sleep(0.2)
    def down_release(self,event=None):
        self.senderSocket.send("_stop_".encode())
        
    def left_press(self,event=None):
        if self.connected == 1:
            self.senderSocket.send("_turn_left_".encode())
            sleep(0.2)
    def left_release(self,event=None):
        self.senderSocket.send("_stop_".encode())
    def right_press(self,event=None):
        if self.connected == 1:
            self.senderSocket.send("_turn_right_".encode())
            sleep(0.2)
    def right_release(self,event=None):
        self.senderSocket.send("_stop_".encode())
    def rr_press(self,event=None):
        if self.connected == 1:
            self.senderSocket.send("_rotate_right_".encode())
            sleep(0.2)
    def rr_release(self,event=None):
        self.senderSocket.send("_stop_".encode())
    def rl_press(self,event=None):
        if self.connected == 1:
            self.senderSocket.send("_rotate_left_".encode())
            sleep(0.2)
    def rl_release(self,event=None):
        self.senderSocket.send("_stop_".encode())
    def end(self,event=None):
        if self.senderSocket != None:
            self.disconnect_press()
        self.master.destroy()

        

root = Tk()
app= App(root)
root.mainloop()
