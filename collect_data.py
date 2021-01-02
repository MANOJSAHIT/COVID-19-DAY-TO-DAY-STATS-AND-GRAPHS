import requests
import pandas as pd
import json
import time
from datetime import date
class parse_hub:
    def __init__(self):
        self.API_KEY='tTKF3KYdpHPM'
        self.PROJECT_WORLD='tqC2y7jarc3D'
        self.PROJECT_STATE='taqvrTmFMyrM'
    def collect_state(self):
        #print('Collecting Data..........')
        total_cases_df=pd.read_csv('confirmed_state.csv')
        date_list=list(total_cases_df['state'])
        self.today=date.today()
        self.today=self.today.strftime('%d-%m-%Y')
        try:
            response_state=requests.post(f'https://www.parsehub.com/api/v2/projects/{self.PROJECT_STATE}/run',params={'api_key':self.API_KEY})
            self.RUN_STATE=json.loads(response_state.text)['run_token']
            state_run_status=requests.get(f'https://www.parsehub.com/api/v2/runs/{self.RUN_STATE}',params={'api_key':self.API_KEY})
            state_ready=json.loads(state_run_status.text)['status']
            while(state_ready!='complete'):
                time.sleep(10)
                state_run_status=requests.get(f'https://www.parsehub.com/api/v2/runs/{self.RUN_STATE}',params={'api_key':self.API_KEY})
                state_ready=json.loads(state_run_status.text)['status']
            self.state_data=requests.get(f'https://www.parsehub.com/api/v2/runs/{self.RUN_STATE}/data',params={'api_key':self.API_KEY})
        except :
            self.state_data=requests.get(f'https://www.parsehub.com/api/v2/projects/{self.PROJECT_STATE}/last_ready_run/data',params={'api_key':self.API_KEY})
        try:
            state_data_dic=json.loads(self.state_data.text)['state']
        except :
            self.state_data=requests.get(f'https://www.parsehub.com/api/v2/projects/{self.PROJECT_STATE}/last_ready_run/data',params={'api_key':self.API_KEY})
        if str(self.today) in date_list:
            cases_drop=pd.read_csv('confirmed_state.csv')
            cases_drop=cases_drop[:-1]
            cases_drop.to_csv('confirmed_state.csv',index=False)
            recovered_drop=pd.read_csv('recovered_state.csv')
            recovered_drop=recovered_drop[:-1]
            recovered_drop.to_csv('recovered_state.csv',index=False)
            deaths_drop=pd.read_csv('deaths_state.csv')
            deaths_drop=deaths_drop[:-1]
            deaths_drop.to_csv('deaths_state.csv',index=False)
        #print('Storing Data...........')
        self.store_state()
        #print('Updated And Stored')
    def collect_world(self):
        #print('Collecting Data...........')
        temp_df=pd.read_csv('confirmed_world.csv')
        date_list=list(temp_df['Dates'])
        self.today=date.today()
        self.today=self.today.strftime('%d-%m-%Y')
        try:
            response_world=requests.post(f'https://www.parsehub.com/api/v2/projects/{self.PROJECT_WORLD}/run',params={'api_key':self.API_KEY})
            self.RUN_WORLD=json.loads(response_world.text)['run_token']
            world_run_status=requests.get(f'https://www.parsehub.com/api/v2/runs/{self.RUN_WORLD}',params={'api_key':self.API_KEY})
            world_ready=json.loads(world_run_status.text)['status']
            while(world_ready!='complete'):
                time.sleep(10)
                world_run_status=requests.get(f'https://www.parsehub.com/api/v2/runs/{self.RUN_WORLD}',params={'api_key':self.API_KEY})
                world_ready=json.loads(world_run_status.text)['status']
                self.world_data=requests.get(f'https://www.parsehub.com/api/v2/runs/{self.RUN_WORLD}/data',params={'api_key':self.API_KEY})
        except :
                self.world_data=requests.get(f'https://www.parsehub.com/api/v2/projects/{self.PROJECT_WORLD}/last_ready_run/data',params={'api_key':self.API_KEY})
        try:
            world_data_dic=json.loads(self.world_data.text)['country_name']
        except :
            self.world_data=requests.get(f'https://www.parsehub.com/api/v2/projects/{self.PROJECT_WORLD}/last_ready_run/data',params={'api_key':self.API_KEY})
        if str(self.today) in date_list:
            cases_drop=pd.read_csv('confirmed_world.csv')
            cases_drop=cases_drop[:-1]
            cases_drop.to_csv('confirmed_world.csv',index=False)
            recovered_drop=pd.read_csv('recovered_world.csv')
            recovered_drop=recovered_drop[:-1]
            recovered_drop.to_csv('recovered_world.csv',index=False)
            deaths_drop=pd.read_csv('deaths_world.csv')
            deaths_drop=deaths_drop[:-1]
            deaths_drop.to_csv('deaths_world.csv',index=False)
        #print('Storing Data........')
        self.store_world()
        #print('Updated And Stored')
    def store_state(self):
        state_data_dic=json.loads(self.state_data.text)['state']
        total_cases_df=pd.read_csv('confirmed_state.csv')
        total_recovered_df=pd.read_csv('recovered_state.csv')
        total_deaths_df=pd.read_csv('deaths_state.csv')
        #states_existing=list(total_cases_df.columns)
        cases_new={}
        recovered_new={}
        deaths_new={}
        date_list=list(total_cases_df['state'])
        date_list.append(str(self.today))
        for i in state_data_dic:
            try:
                tempc=list(total_cases_df[i['name']])
                tempc.append(int(i['total_cases']))
                cases_new[i['name']]=tempc
                tempr=list(total_recovered_df[i['name']])
                tempr.append(int(i['total_recovered']))
                recovered_new[i['name']]=tempr
                tempd=list(total_deaths_df[i['name']])
                tempd.append(int(i['total_deaths']))
                deaths_new[i['name']]=tempd
            except :
                pass
        cases_df=pd.DataFrame.from_dict(cases_new)
        cases_df.insert(0,'state',date_list)
        cases_df.to_csv('confirmed_state.csv',index=False)
        recovered_df=pd.DataFrame.from_dict(recovered_new)
        recovered_df.insert(0,'state',date_list)
        recovered_df.to_csv('recovered_state.csv',index=False)
        deaths_df=pd.DataFrame.from_dict(deaths_new)
        deaths_df.insert(0,'state',date_list)
        deaths_df.to_csv('deaths_state.csv',index=False)
    def store_world(self):
        world_data_dic=json.loads(self.world_data.text)['country_name']
        total_cases_df=pd.read_csv('confirmed_world.csv')
        total_recovered_df=pd.read_csv('recovered_world.csv')
        total_deaths_df=pd.read_csv('deaths_world.csv')
        #countries_existing=list(total_recovered_df.columns)[1:]
        cases_new={}
        recovered_new={}
        deaths_new={}
        date_list=list(total_cases_df['Dates'])
        date_list.append(str(self.today))
        ab_list=['St. Barth', 'Taiwan', 'Congo', 'Montserrat', 'Martinique', 'Myanmar','Vatican City', 'Réunion', 'Sint Maarten', 'Wallis and Futuna', 'Guadeloupe','Ivory Coast', 'Gibraltar', 'DRC', 'Anguilla', 'Greenland', 'Mayotte','Caribbean Netherlands', 'Saint Pierre Miquelon','Curaçao', 'Turks and Caicos', 'Aruba','Falkland Islands','French Polynesia', 'CAR', 'French Guiana', 'Cayman Islands','Channel Islands', 'New Caledonia', 'Bermuda', 'Macao']
        converted_dic={}
        for i in world_data_dic:
            if i['name'] in ab_list:
                pass
            else:
                try:
                    tempc=list(total_cases_df[i['name']])
                    tempc.append(i['total_cases'])
                    cases_new[i['name']]=tempc
                    tempr=list(total_recovered_df[i['name']])
                    tempr.append(i['total_recovered'])
                    recovered_new[i['name']]=tempr
                    tempd=list(total_deaths_df[i['name']])
                    tempd.append(i['total_deaths'])
                    deaths_new[i['name']]=tempd
                except :
                    pass
        cases_df=pd.DataFrame.from_dict(cases_new)
        cases_df.insert(0,'Dates',date_list)
        cases_df.to_csv('confirmed_world.csv',index=False)
        recovered_df=pd.DataFrame.from_dict(recovered_new)
        recovered_df.insert(0,'Dates',date_list)
        recovered_df.to_csv('recovered_world.csv',index=False)
        deaths_df=pd.DataFrame.from_dict(deaths_new)
        deaths_df.insert(0,'Dates',date_list)
        deaths_df.to_csv('deaths_world.csv',index=False)
