import pandas as pd 
import csv
import math
import os
import datetime
import plotly.plotly as py 
import plotly.graph_objs as go 
import plotly.figure_factory as FF
from datetime import datetime, timedelta, date

def hs_x_y_z(file_name,new_name):
    #convert csv file to new csv file with only #HeaderTS,X,Y,Z to use on visualizer 
    csv_input = pd.read_csv(file_name, usecols = ['HEADER_TIME_STAMP','X','Y','Z'])
    csv_input['HEADER_TIME_STAMP'] = csv_input['HEADER_TIME_STAMP'].astype('str').str[:-3]
    csv_input.to_csv(new_name, index = False)
#hs_x_y_z()

#takes in the file from the folder and obtains the name of the file set to file_name
#converts HEADERTS file to new csv file with sample rate/data_loss columns
def read_file(name):
    csv_input = pd.read_csv(name, usecols = ['HEADER_TIME_STAMP'])
    #append a substitute value at the end of header_time_stamp to fulfill algorithm
    csv_input['HEADER_TIME_STAMP'] = pd.to_datetime(csv_input['HEADER_TIME_STAMP'])
    csv_input = csv_input.sort_values(by =['HEADER_TIME_STAMP'])
    df1 = pd.DataFrame({'HEADER_TIME_STAMP':['2000-01-01 00:00:00.000000']})
    df1 = csv_input.append(df1)

    #df1['HEADER_TIME_STAMP'] = df1['HEADER_TIME_STAMP'].astype('str').str[:-3]
    df1['START_TIME'] = ''
    df1['STOP_TIME'] = ''
    df1['SAMPLING_RATE'] =''
    df1['DATA_LOSS_PERCENTAGE']= ''
    df1.to_csv('temp.csv', index = False)

#calculate sampling rate per second along with data loss, writes new file
#parameter for function is the name of the file being written
def complete_format(new_name):
    #convert dataset to datetime, time stamp format
    csv_input = pd.read_csv('temp.csv', usecols = [
        'HEADER_TIME_STAMP','START_TIME','STOP_TIME','SAMPLING_RATE',
        'DATA_LOSS_PERCENTAGE'])
    csv_input['HEADER_TIME_STAMP'] = pd.to_datetime(csv_input['HEADER_TIME_STAMP'])
    #isolate seconds within the timestamp column of csv file
    csv_input['SECONDS'] = csv_input['HEADER_TIME_STAMP'].dt.second

    #print(csv_input['SECONDS'])
    cnt = 0
    index = 0
    per = 0
    j = csv_input['SECONDS'].iloc[0]
    csv_input['NO_MILLI'] = csv_input['HEADER_TIME_STAMP'].astype('datetime64[s]')
    time = 0
    time_1_sec = 0
    #print(csv_input['NO_MILLI'])
    start_time = []
    stop_time = []
    smpl_rate = []
    data_loss = []
    
    n = datetime(2000,1,1,0,0,0)
    
    for seconds in csv_input['SECONDS']:
        if(j == csv_input['SECONDS'].iloc[index]):
            cnt += 1
            if(cnt == 1 and index == 0):
                #start_time.append(csv_input['HEADER_TIME_STAMP'].iloc[index])
                start_time.append(csv_input['NO_MILLI'].iloc[index])
            elif(cnt == 1 and index != 0):
                #start_time.append(csv_input['HEADER_TIME_STAMP'].iloc[index-1])
                start_time.append(csv_input['NO_MILLI'].iloc[index])
        elif(j != csv_input['SECONDS'].iloc[index]):
            if(cnt != 0):
                smpl_rate.append(cnt)
                #absolute value for numbers greater than 0 
                per = abs((50-cnt)/50*100)
                data_loss.append(float(per))
                #stop_time.append(csv_input['HEADER_TIME_STAMP'].iloc[index-1])
                if(csv_input['NO_MILLI'].iloc[index] == n):
                    time = csv_input['NO_MILLI'].iloc[index-1]
                    time_1_sec = time + timedelta(seconds = 1)
                    stop_time.append(time_1_sec)
                else:    
                    stop_time.append(csv_input['NO_MILLI'].iloc[index])
                    
                cnt = 0
            if(j == 59):
                j = 0
                cnt = 1
                #start_time.append(csv_input['HEADER_TIME_STAMP'].iloc[index-1])
                start_time.append(csv_input['NO_MILLI'].iloc[index])
            else:
                j += 1
        index += 1
    
        
    csv_input['START_TIME'] = pd.DataFrame(start_time)
    csv_input['STOP_TIME'] = pd.DataFrame(stop_time)
    csv_input['SAMPLING_RATE'] = pd.DataFrame(smpl_rate).astype(int)
    csv_input['DATA_LOSS_PERCENTAGE'] = pd.DataFrame(data_loss)

    csv_input = csv_input.drop(columns = 'SECONDS')
    csv_input = csv_input.drop(columns = 'HEADER_TIME_STAMP')
    csv_input = csv_input.drop(columns = 'NO_MILLI')

    csv_input = csv_input.dropna()
    csv_input.to_csv(new_name, index = False)

    os.remove('temp.csv')
                
#takes in the previously written csv file to find any outliers in terms
#of sampling rates less than 30 or greater than 70
def weird_data(new_name):
    #standard frequency of sampling rate 50 hz
    #if sampling rate is equal to 1, output time stamp and sum number of occurances
    csv_input = pd.read_csv(new_name, usecols = ['START_TIME','STOP_TIME','SAMPLING_RATE'])
    
    csv_input['START_TIME_ERROR'] = ''
    csv_input['STOP_TIME_ERROR'] = ''
    csv_input['SAMPLING_RATE_ERROR'] = ''
    start = []
    stop = []
    rps = []
    count = 0
    index = 0

    for row in csv_input['SAMPLING_RATE']:
        if((csv_input['SAMPLING_RATE'].iloc[index] <= 30) or (csv_input['SAMPLING_RATE'].iloc[index] >= 70)):
            start.append(csv_input['START_TIME'].iloc[index])
            stop.append(csv_input['STOP_TIME'].iloc[index])
            rps.append(csv_input['SAMPLING_RATE'].iloc[index])
            count += 1
        index += 1
    #for the last index
   
    csv_input['START_TIME_ERROR'] = pd.DataFrame(start)
    csv_input['STOP_TIME_ERROR'] = pd.DataFrame(stop)
    csv_input['SAMPLING_RATE_ERROR'] = pd.DataFrame(rps)

    csv_input = csv_input.drop(columns = 'SAMPLING_RATE')
    csv_input = csv_input.drop(columns = 'START_TIME')
    csv_input = csv_input.drop(columns = 'STOP_TIME')
    csv_input = csv_input.dropna()
    file = new_name.str[:-3]
    file = file + 'error.csv'
    csv_input.to_csv(file,index = False)

#weird_data()
#graph sampling rate vs start time
def plot_time_vs_sample(file, graph_name):
    #x-axis for time, y-axis for sample rate
    #time in hour,min,second
    file1 = pd.read_csv(file, usecols = ['START_TIME','SAMPLING_RATE'])
    #file2 = pd.read_csv(file_2, usecols = ['START_TIME_ERROR','SAMPLING_RATE_ERROR'])

    trace1 = go.Scatter(
        x = file1['START_TIME'], y = file1['SAMPLING_RATE'],
        mode = 'lines', name = 'Sampling_rate'
    )
    data = [trace1]
    layout = go.Layout(
        title = go.layout.Title(
            text = 'Sample Rate vs Time'
        ),
        xaxis = go.layout.XAxis(
            title = go.layout.xaxis.Title(
                text = 'Recorded Time', font = dict(family = 'Times New Roman, monospace', size = 18, color = 'black')
            )
        ),
        yaxis = go.layout.YAxis(
            title = go.layout.yaxis.Title( 
                text = 'Sampling Rate (hertz)', font = dict(family = 'Times New Roman, monospace', size = 18, color = 'black')
            )
        )
    )
    fig = go.Figure(data = data, layout = layout)
    py.plot(fig, filename = graph_name)
    
def main():
    new_name = ''
    visual = ''
    #iterate through a folder that contains sensor.csv files with header timestamps
    for filename in os.listdir(r'C:\Users\gilbe\Documents\data_science'):
        if(filename.endswith("sensor.csv")):
            #specifically used to differentiate files based on start time 
            new_name = filename[-20:-17]
            #if the sensor file is already created then skip the file
            if(new_name == new_name + 'samplerate.sensor.csv'):
                pass
            #read given csv file and produce a template file with specific formatting
            read_file(filename)
            #how you want to name your newly created files
            graph = new_name + '.graph'
            visual = new_name + '.xyz.sensor.csv'
            new_name = new_name + 'samplerate.sensor.csv'
            
            hs_x_y_z(filename,visual)
            #write new csv file containing HTS,SR
            complete_format(new_name)
            #create a plotly graph that graphs Sampling Rate vs Time
            plot_time_vs_sample(new_name,graph) 
        else:
            continue
#main()
