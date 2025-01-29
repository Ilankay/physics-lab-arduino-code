import pyfirmata
import pandas as pd
import numpy as np
import time
import threading

def high_precision_sleep(duration):
    start_time = time.perf_counter()
    while True:
        elapsed_time = time.perf_counter() - start_time
        remaining_time = duration - elapsed_time
        if remaining_time <= 0:
            break
        if remaining_time > 0.02:  # Sleep for 5ms if remaining time is greater
            time.sleep(max(remaining_time/2, 0.0001))  # Sleep for the remaining time or minimum sleep interval
        else:
            pass

def read_input(board, dur, cr,path = ""):
    interval = 1/cr
    time_array = np.arange(time.perf_counter(), time.perf_counter()+dur, interval)
    results = np.zeros(time_array.shape)
    
    for i in range(len(results)):
        val = board.analog[0].read()
        results[i] = val
        
        high_precision_sleep(interval)

    df = pd.DataFrame({'time': time_array, 'voltage': results})
    df.to_csv(path+'results.csv')
    print(results)

def experiment(input_board,output_board,dur,cr_in,cr_out):
    interval = 1/cr_in
    time_array = np.arange(time.perf_counter(), time.perf_counter()+dur, interval)
    results = np.zeros(time_array.shape)
    arr = np.array([0]*int(1/cr_out), [1]*int(1/cr_out))
    random_data = np.tile(arr, len(time_array))
    random_data = random_data[:len(time_array)]
    for i in range(len(time_array)):
        val = input_board.analog[0].read()
        results[i] = val
        output_board.digital[12].write(random_data[i])
        high_precision_sleep(interval)
        time_array[i] = time.perf_counter()
        
    df = pd.DataFrame({'time': time_array, 'voltage': results})
    df_out = pd.DataFrame({'time': time_array, 'output': random_data})
    df.to_csv("results.csv")
    df_out.to_csv("output.csv")

    
    
def make_output(board,dur,cr,path=""):
    interval = 1/cr
    time_array = np.arange(time.perf_counter(), time.perf_counter()+dur, interval)
    arr = np.array([0,1])
    random_data = np.tile(arr, len(time_array))
    random_data = random_data[:len(time_array)]
    for i in range(len(time_array)):
        output_board.digital[12].write(random_data[i])
        time_array[i] = time.perf_counter()
        high_precision_sleep(interval)
                
    df_out = pd.DataFrame({'time': time_array, 'output': random_data})
    df_out.to_csv(path+"output.csv")

if __name__=="__main__":
    output_board = pyfirmata.Arduino('/dev/ttyACM0')
    
    output_board.digital[12].mode = pyfirmata.OUTPUT
    it1 = pyfirmata.util.Iterator(output_board)  
    it1.start()
    
    
   # input_board = pyfirmata.Arduino('/dev/ttyACM1')

   # input_board.analog[0].mode = pyfirmata.INPUT  
   # it = pyfirmata.util.Iterator(input_board)  
   # it.start()  


    print("starting threads")
    make_output(output_board,5,4,path = "results/")
