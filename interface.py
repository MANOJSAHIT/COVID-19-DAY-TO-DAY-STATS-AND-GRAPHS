import tkinter as tk
from tkinter import *
import collect_data
import pandas as pd
from matplotlib import pyplot as plt
from threading import Thread
import time
class user_interface:
    def __init__(self):
        self.collect_obj=collect_data.parse_hub()
        self.root=Tk()
        self.root.geometry('400x400')
        self.root.configure(bg='#00ffd7')
        self.warning_text=Text(self.root,height=10,width=50,bg='#f4c2c2')
        self.warning_text.pack(side=BOTTOM)
        india_button=Button(self.root,text='View India Statistics',bg='#00ff0b',command=self.view_india).place(x=100,y=50)
        world_button=Button(self.root,text='View World Wide Statistics',bg='#00ff0b',command=self.view_world).place(x=100,y=90)
        fetch_india_button=Button(self.root,text='Update Data Of India To Date',bg='#00ff0b',command=self.thread_state).place(x=100,y=130)
        fetch_world_button=Button(self.root,text='Update World Wide Data To Date',bg='#00ff0b',command=self.thread_world).place(x=100,y=170)
        self.root.mainloop()
    def thread_state(self):
        self.warning_text.insert(tk.END,'\nCollecting Data For India..........\nPlease Do Not Close Window')
        self.state_t=Thread(target=self.collect_obj.collect_state,daemon=True)
        self.state_t.start()
        Thread(target=self.check_thread).start()
    def check_thread(self):
        temp=self.state_t.is_alive()
        while temp==True:
            temp=self.state_t.is_alive()
        self.warning_text.insert(tk.END,'\nData Collected And Updated For India')
        time.sleep(3)
    def check_thread1(self):
        temp=self.world_t.is_alive()
        while temp==True:
            temp=self.world_t.is_alive()
        self.warning_text.insert(tk.END,'\nData Collected And Updated For World')
    def thread_world(self):
        self.warning_text.insert(tk.END,'\nCollecting Data For World..........\nPlease Do Not Close Window')
        self.world_t=Thread(target=self.collect_obj.collect_world,daemon=True)
        self.world_t.start()
        Thread(target=self.check_thread1).start()
    def view_india(self):
        self.cur=0
        self.cases_data=pd.read_csv('confirmed_state.csv')
        self.recovered_data=pd.read_csv('recovered_state.csv')
        self.deaths_data=pd.read_csv('deaths_state.csv')
        self.states=list(self.cases_data.columns)[1:]
        self.dates=list(self.cases_data['state'])[len(list(self.cases_data['state']))-10:]
        self.set_params()
        self.base_interface(0)
    def view_world(self):
        self.cur=0
        self.cases_data=pd.read_csv('confirmed_world.csv')
        self.recovered_data=pd.read_csv('recovered_world.csv')
        self.deaths_data=pd.read_csv('deaths_world.csv')
        self.states=list(self.cases_data.columns)[1:]
        self.dates=list(self.cases_data['Dates'])[len(list(self.cases_data['Dates']))-10:]
        self.set_params()
        self.base_interface(1)
    def base_interface(self,sep):
        self.base=Toplevel()
        self.base.geometry('400x400')
        self.base.configure(bg='#00ff58')
        if sep==1:
            self.warning=Label(self.base,text='If Search Did Not Give Desired Result Use Drop Down Menu And Click Select',bg='#c1ff00')
            self.warning.place(x=0,y=10)
            self.special=StringVar(self.base)
            self.special.set('USA')
            self.special_case=OptionMenu(self.base,self.special,'USA','UK','UAE','S. Korea')
            self.special_case.place(x=350,y=50)
            self.view_graphs=Button(self.base,text='View Graphs Date Wise For Above Country',bg='#ffe766',command=lambda:self.date_wise_graphs(sep))
            self.view_graphs.place(x=100,y=300)
        if sep==0:
            self.warning=Label(self.base,text='Please Type Full Name Of State',bg='#c1ff00')
            self.warning.place(x=80,y=10)
            self.view_graphs=Button(self.base,text='View Graphs Date Wise For Above State',bg='#ffe766',command=lambda:self.date_wise_graphs(sep))
            self.view_graphs.place(x=100,y=300)
        self.see_recovered=Label(self.base,text='Total Number Of Recovered:- '+str(self.num_recovered),bg='#c1ff00')
        self.see_recovered.place(x=100,y=200)
        self.search_base_name=Entry(self.base,font='bold',bg='#c1ff00')
        self.search_base_name.place(x=50,y=50)
        self.search_button=Button(self.base,text='Search',bg='#ffe766',command=self.search_command).place(x=300,y=50)
        self.see_base_name2=Label(self.base,text=self.base_name2,bg='#c1ff00')
        self.see_base_name2.place(x=150,y=100)
        self.back_ward_button=Button(self.base,text='<<',bg='#ffe766',command=self.backward)
        self.back_ward_button.place(x=100,y=100)
        self.forward_button=Button(self.base,text='>>',bg='#ffe766',command=self.forward).place(x=250,y=100)
        self.see_deaths=Label(self.base,text='Total Number Of Deaths:- '+str(self.num_deaths),bg='#c1ff00')
        self.see_deaths.place(x=100,y=250)
        self.see_cases=Label(self.base,text='Total Number Of Cases:- '+str(self.num_cases),bg='#c1ff00')
        self.see_cases.place(x=100,y=150)
    def forward(self):
        if self.cur>=len(self.states)-1:
            return
        self.cur+=1
        self.base_name2=self.states[self.cur]
        self.num_cases=str(list(self.cases_data[self.states[self.cur]])[len(self.cases_data)-1])
        self.num_recovered=str(list(self.recovered_data[self.states[self.cur]])[len(self.recovered_data)-1])
        self.num_deaths=str(list(self.deaths_data[self.states[self.cur]])[len(self.deaths_data)-1])
        self.see_base_name2.config(text=self.base_name2)
        self.see_cases.config(text='Total Number Of Cases:-'+str(self.num_cases))
        self.see_recovered.config(text='Total Number Of Recovered:-'+str(self.num_recovered))
        self.see_deaths.config(text='Total Number Of Deaths:-'+str(self.num_deaths))
    def backward(self):
        self.cur-=1
        self.base_name2=self.states[self.cur]
        self.num_cases=str(list(self.cases_data[self.states[self.cur]])[len(self.cases_data)-1])
        self.num_recovered=str(list(self.recovered_data[self.states[self.cur]])[len(self.recovered_data)-1])
        self.num_deaths=str(list(self.deaths_data[self.states[self.cur]])[len(self.deaths_data)-1])
        self.see_base_name2.config(text=self.base_name2)
        self.see_cases.config(text='Total Number Of Cases:- '+str(self.num_cases))
        self.see_recovered.config(text='Total Number Of Recovered:-'+str(self.num_recovered))
        self.see_deaths.config(text='Total Number Of Deaths:-'+str(self.num_deaths))
    def search_command(self):
        self.base_name=self.search_base_name.get()
        self.search_base_name.delete(0,'end')
        self.base_name2=''
        i=0
        while(i<len(self.base_name)):
            if i==0:
                self.base_name2+=self.base_name[0].upper()
                i+=1
            elif self.base_name[i]==' ':
                self.base_name2+=self.base_name[i]
                i+=1
                self.base_name2+=self.base_name[i].upper()
                i+=1
            else:
                self.base_name2+=self.base_name[i]
                i+=1
        if self.base_name2 in self.states:
            pass
        else:
            self.base_name2=str(self.special.get())
        self.num_cases=str(list(self.cases_data[self.base_name2])[len(self.cases_data)-1])
        self.num_recovered=str(list(self.recovered_data[self.base_name2])[len(self.recovered_data)-1])
        self.num_deaths=str(list(self.deaths_data[self.base_name2])[len(self.deaths_data)-1])
        self.see_base_name2.config(text=self.base_name2)
        self.see_cases.config(text='Total Number Of Cases:- '+str(self.num_cases))
        self.see_recovered.config(text='Total Number Of Recovered:- '+str(self.num_recovered))
        self.see_deaths.config(text='Total Number Of Deaths:-'+str(self.num_deaths))
    def set_params(self):
        self.base_name2=self.states[0]
        self.num_cases=str(list(self.cases_data[self.states[0]])[len(self.cases_data)-1])
        self.num_recovered=str(list(self.recovered_data[self.states[0]])[len(self.recovered_data)-1])
        self.num_deaths=str(list(self.deaths_data[self.states[0]])[len(self.deaths_data)-1])
    def date_wise_graphs(self,sep):
        self.graph_base=Toplevel()
        self.graph_base.geometry('400x400')
        self.graph_base.configure(bg='#009980')
        self.death_graph=Button(self.graph_base,text='View Deaths Graph',bg='#ff00c4',command=lambda:self.plot_death(sep)).place(x=150,y=150)
        self.cases_graph=Button(self.graph_base,text='View Cases Graph',bg='#ff00c4',command=lambda:self.plot_cases(sep)).place(x=150,y=100)
    def plot_death(self,sep):
        temp=list(self.deaths_data[self.base_name2])[len(list(self.deaths_data[self.base_name2]))-10:]
        if sep==0:
            i=0
            final_plot_data=[]
            while(i<len(temp)):
                final_plot_data.append(temp[i])
                i+=1
        if sep==1:
            temp=list(self.deaths_data[self.base_name2])[len(list(self.deaths_data[self.base_name2]))-10:]
            i=0
            final_plot_data=[]
            while(i<len(temp)):
                if isinstance(temp[i],str):
                    final_plot_data.append(abs(int(temp[i].replace(',',''))))
                else:
                    final_plot_data.append(abs(temp[i]))
                i+=1
        plt.style.use('dark_background')
        plt.xlabel('Dates')
        plt.ylabel('Deaths')
        plt.xticks(rotation=315)
        plt.title(self.base_name2+'\nDate-Deaths Plot',loc='center')
        plt.bar(self.dates,final_plot_data,color='maroon')
        for i,j in zip(self.dates,final_plot_data):
            plt.annotate(j,(i,j),textcoords="offset points",xytext=(0,10),ha='center')
        plt.show()
    def plot_cases(self,sep):
        temp=list(self.cases_data[self.base_name2])[len(list(self.cases_data[self.base_name2]))-10:]
        if sep==0:
            i=0
            final_plot_data=[]
            while(i<len(temp)):
                final_plot_data.append(temp[i])
                i+=1
        if sep==1:
            temp=list(self.cases_data[self.base_name2])[len(list(self.cases_data[self.base_name2]))-10:]
            i=0
            final_plot_data=[]
            while(i<len(temp)):
                if isinstance(temp[i],str):
                    final_plot_data.append(abs(int(temp[i].replace(',',''))))
                else:
                    final_plot_data.append(abs(temp[i]))
                i+=1
        plt.style.use('dark_background')
        plt.title(self.base_name2+'\nDate-Cases Plot',loc='center')
        plt.xlabel('Dates')
        plt.ylabel('Cases')
        plt.xticks(rotation=315)
        plt.bar(self.dates,final_plot_data,color='maroon')
        for i,j in zip(self.dates,final_plot_data):
            plt.annotate(j,(i,j),textcoords="offset points",xytext=(0,10),ha='center')
        plt.yscale('log')
        plt.show()
us=user_interface()
