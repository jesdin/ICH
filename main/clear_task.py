import threading
import os, stat, time

PATH = "assets/tmp/"

def clear_temp():
  # get list of files in tmp directory
  f = []
  for root, dirs, files in os.walk(PATH):
  	for file in files:
  		f.append(os.path.join(root,file))  

  # get local time
  localTime = time.mktime(time.localtime())
  for file in f:
    # get access time of file
    accessTime = time.ctime ( os.stat(file) [ stat.ST_ATIME ] )  
    accessTime = time.strptime(accessTime)

    # get time dif in minutes
    dif = (localTime - time.mktime(accessTime))/60

    # if last accessed is more than 60 mins del file
    if (dif > 60):
      os.remove(file)
      
  threading.Timer(3600.0, clear_temp).start()