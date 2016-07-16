import time
import Adafruit_DHT
import time
import datetime
import sys
import os

import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure

sensor = Adafruit_DHT.DHT11
pin=3
ts = time.time()

print("Initializing plotly connection...")

def plotInit():
    username = 'wbartos'
    api_key = 'nqjed1c0hq'
    stream_token1 = 'yadefw1l6t'
    stream_token2 = 'wjocemhh7e'
    stream_token3 = 'p29rnwd2ur'

    py.sign_in(username, api_key)

    trace1 = Scatter(
        x=[],
        y=[],
        name='Outside Temperature, C',
        stream=dict(
            token=stream_token1,
        )
    )

    trace2 = Scatter(
        x=[],
        y=[],
        name='Inside Temperature, C',
        stream=dict(
            token=stream_token2,    
        )
    )

    trace3 = Scatter(
        x=[],
        y=[],
        name='Inside Humidity, %',
        stream=dict(
            token=stream_token3,     
        )
    )


    layout = Layout(
        title = 'Inside Temp, Outside Temp, Humidity'
            )
    fig = Figure(data=[trace1, trace2, trace3], layout=layout)

    print(py.plot(fig, filename ='test'))

    stream1 = py.Stream(stream_token1)
    stream2 = py.Stream(stream_token2)
    stream3 = py.Stream(stream_token3)
    stream1.open()
    stream2.open()
    stream3.open()



    print("Sensors running...")


    while True:
    
        tempFile = open("/sys/bus/w1/devices/28-0115a3fdfaff/w1_slave")
        output = tempFile.read()
        tempFile.close()
        temp = float(output[69:])/1000
        outTemp = str(temp)

  
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:

            inTemp = str(temperature)
            inHum = str(humidity)
            #print('Indoor Temp = {0:0.1f}*C'.format(temperature)+ "\n" + 'Humidity = {0:0.1f}%'.format(humidity) + "\n")
        

        else:
            print('Faild to grab reading. Try again')

        dataToWrite = (outTemp + "\n" + inTemp + "\n" + inHum)
        writeTime = datetime.datetime.now().strftime('%H:%M:%S')
    
        stream1.write({'x':datetime.datetime.now(), 'y': temp})
        stream2.write({'x':datetime.datetime.now(), 'y': inTemp})
        stream3.write({'x':datetime.datetime.now(), 'y': inHum})
        time.sleep(10)


def runSensors():
    while True:
        
        try:
            plotInit()
        except:
            print("Error! Attempting to restart....")
            continue
      
runSensors()
    

