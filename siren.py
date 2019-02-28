# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 01:49:45 2019

@author: Pranav
"""

import pyaudio  
import wave  

#define stream chunk  
count =0 
while(count<5):
    chunk = 1024  
    
    #open a wav format music  
    f = wave.open("fast.wav","rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  
    
    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  
    
    #stop stream  
    stream.stop_stream()  
    stream.close()  
    count+=1
    #close PyAudio  
    p.terminate()