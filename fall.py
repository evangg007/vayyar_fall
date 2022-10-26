#coding=utf-8
'''
Vayyar摔倒简易测试demo V1.1  演示用
ARENA="-1, 1, 0.2, 2.7, 0.1, 2"
SENSOR_HEIGHT=1.5

3s    存在感应
10s   摔倒预警
20s   摔倒报警(预警后20s内倒地未起或者无第二个目标被检测到)
10s   取消报警 取消预警 离场确认

ps:运行脚本前，最好重新插拔一下usb power 刷新下缓存
'''

import serial 
import time 
import matplotlib.pyplot as plt
import numpy as np
# import numbers
import unicodedata
ser = serial.Serial("COM3",921600,timeout = 5) # 开启com3口，波特率921600，超时1
ser.flushInput() # 清空缓冲区
datasize = 42

p0 = plt.imread('presence0.jpg')
p1 = plt.imread('presence1.jpg')
f0 = plt.imread('fall0.jpg')
f1 = plt.imread('fall1.jpg')
f2 = plt.imread('fall2.jpg')
# pp=[0,0,0,0,0]
# ff=[0,0,0,0,0]
global falltimes
falltimes = 0

def main():
  global falltimes
  while True:    
    count = ser.inWaiting() # 获取串口缓冲区数据
    if count !=0 :
      recv = ser.read(ser.in_waiting).decode("gbk") # 读出串口数据，数据采用gbk编码
      #print(recv) 
      if len(recv) > datasize:
            data = recv[0:datasize]
            index_f=recv.find('Fall')
            index_p=recv.find('Presence')
            f = (recv[index_f+5])
            p = (recv[index_p+9])
            print('f',f)
            print('p',p)
            A =f.isdigit()
            B =p.isdigit()
            if f.isdigit() and p.isdigit():
                  f = int(f)
                  p = int(p)
                  if p==0 and f==0:
                        plt.figure(1)
                        plt.clf()
                        plt.imshow(p0)
                        falltimes = 0

                  elif f==1 or f==2 :
                        if falltimes >= 35:
                        #     current_time = time.strftime("%y_%m_%d %H.%M", time.localtime())
                        #     output_name = 'fall%s' % current_time
                        #     output_file = open(output_name, "w")        
                            plt.figure(1)
                            plt.clf()
                            plt.imshow(f2)
                        else:
                            plt.figure(1)
                            plt.clf()
                            plt.imshow(f1)
                            falltimes += 1
      
                  else:
                        plt.figure(1)
                        plt.clf()
                        plt.imshow(p1)
                        falltimes = 0
     
                  plt.axis('off')
                  plt.ion()
                  plt.show()
                  plt.pause(0.05)  
                        
      data=' '
      count=0
      ser.flushInput()
      #print('falltime:',falltimes)
    time.sleep(0.2)
    
 

 
if __name__ == '__main__':
  main()