import os
import csv
from io import StringIO
#import subprocess
from subprocess import Popen, PIPE


java_path= r'C:\Program Files\Java\jre1.8.0_181\bin'
os.chdir(java_path)


input_ks_location =r'C:\Users\lubhayan\Documents\Clients\Internal\KeystoreConsolidation\NewGlobalKS\aws\agrewcappo055v.rbi.web.ds\el_puto.jks'
input_ks_pass = r'3point142'

list_input_ks = "keytool -list -keystore " + input_ks_location + " -storepass " + input_ks_pass
print(list_input_ks)

#list_input_ks_output = os.system(list_input_ks)

#read input from cmd
list_input_ks_output = os.popen(list_input_ks).read()
print("------------------")
print(list_input_ks_output)
print("------------------")

#remove first few unnecessary lines
split_list_input_ks_output = list_input_ks_output.split("\n",5)[5]   #split 5 times on \n and then take the 5th split value
print("------------------")
print(split_list_input_ks_output)
print("------------------")

#remove unneccessary line feeds
find_replace_input_ks_output = split_list_input_ks_output.replace(', \n',', ')
print("------------------")
print(find_replace_input_ks_output)
print("------------------")

#read string as file using buffer
buff = StringIO(find_replace_input_ks_output)

csv_reader = csv.reader(buff)   #read as csv
for line in csv_reader:  # loop through lines
    print(line[0])
    print(line[3])
    #cat1_value = line[0]  # left value
    #cat2_value = line[1]  # right value

