## HTS_draft
Python Code (contains plotly, pandas)

Utilizes accelerometer datafiles (CSV format) that contain "HEADER_TIME_STAMPS" as well as 3D coordinates (X,Y,Z) and creates new formatted CSV files

Function Walkthrough:
  
  ### I. Convert file to use on GitHub Visualizer
  - def hs_x_y_z(file_name,new_name):
    - this function extracts 4 specific columns from a (file_name) sensor.csv file 
  (HEADER_TIME_STAMP,X,Y,Z) and writes to a new CSV file (new_name), used for visualizer
  
  ### II. Calculating Sampling_Rate/Data_loss_percentage 
  - def read_file(name):
    - extracts 'HEADER_TIME_STAMP' column from (name) file which creates a temp file with new additional
  columns of ('START_TIME','STOP_TIME','SAMPLING_RATE','DATA_LOSS_PERCENTAGE'), temp file will be used 
  in the complete_format() function 
  - def complete_format(new_name):
    - reads the temp file created by read_file(), copying the already existing columns, calculates the 
  sampling rate per second, calculates the data loss percentage, and displays the results for each
  second based on the file given. The new CSV file written is named under (new_name)
  
  ### III. Finding out abnormal sampling rates
  - def weird_data(new_name):
    - takes in newly created csv file containing sampling rates and start/stop time, iterates through 
  the data to find any sampling rates less than 30 or greater than 70, and creates new columns that
  contains the start/stop time for abnormal sampling rate. New file created is named with:
  new_name + error.csv
    
  ### IV. Graphing sampling rate vs time on plotly
  - def plot_time_vs_sample(file, graph_name):
    - takes in newly created csv file containing sampling rates and start/stop time (file), and plots Sampling Rate  
    along the Y-axis and the start time of the recorded timestamps along the X-axis, graph created will be on Plotly
    and will be named accordingly (graph_name)
    
    
 
  
  
