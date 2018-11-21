import os
from io import StringIO
import pandas as pd

import csv
#import subprocess
#from subprocess import Popen, PIPE


java_path= r'C:\Program Files\Java\jre1.8.0_181\bin'
os.chdir(java_path)


ks1_location =r'C:\Users\lubhayan\Documents\Clients\Internal\KeystoreConsolidation\NewGlobalKS\aws\agrewcappo055v.rbi.web.ds\el_puto.jks'
ks1_pass = r'3point142'

ks2_location =r'C:\Users\lubhayan\Documents\Clients\Internal\KeystoreConsolidation\NewGlobalKS\aws\agrewcappo055v.rbi.web.ds\el_puto_2.jks'
ks2_pass = r'3point142'

def cmd_command(ks_location, ks_pass):
    list_ks = "keytool -list -keystore " + '"' + ks_location + '"' + " -storepass " + ks_pass
    print(list_ks)
    return list_ks

ks1_list = cmd_command(ks1_location, ks1_pass)
ks2_list = cmd_command(ks2_location, ks2_pass)


def cmd_call_format(terminal_output):

    # read input from cmd
    terminal_output_string = os.popen(terminal_output).read()
    # list_input_ks_output = os.system(list_input_ks)
    print("------------------")
    print(terminal_output_string)
    print("------------------")

    # remove first few unnecessary lines
    terminal_output_string_remove_lines = terminal_output_string.split("\n", 5)[5]  # split 5 times on \n and then take the 5th split value
    print("------------------")
    print(terminal_output_string_remove_lines)
    print("------------------")

    # remove unnecessary line feeds
    terminal_output_string_remove_crlf = terminal_output_string_remove_lines.replace(', \n', ', ')
    print("------------------")
    print(terminal_output_string_remove_crlf)
    print("------------------")

    # read string as file using buffer
    return StringIO(terminal_output_string_remove_crlf)


buff1 = cmd_call_format(ks1_list)
buff2 = cmd_call_format(ks2_list)



def remove_columns(csv_file):
    #create pandas data frame
    df = pd.read_csv(csv_file, index_col=False, header=None, sep=',', names=['Alias','Date','Type','Fingerprint']) #read in and add headers for csv file
    print(df.shape)

    #drop unnecessary columns
    df = df.drop(df.columns[[1, 2]], axis=1)
    print(df.shape)

    #add column names
    #df.columns = ['Alias','Fingerprint']

    #convert to csv format
    #chopped_columns = df.to_csv(index=False)
    #print(chopped_columns)
    #return chopped_columns

    #drop duplicate values on data set
    df = df.drop_duplicates('Fingerprint')

    print(df.to_csv(index=False))
    return df


ds1 = remove_columns(buff1)
ds2 = remove_columns(buff2)


def merge_data_frames(df1, df2):
    df = pd.merge(df1, df2, on=['Fingerprint'], how='left', indicator=True).query('_merge == "left_only"')   #merge left, show indicator of both or left only and filter on left only
    print(df.to_csv(index=False))

    # drop unnecessary columns
    df = df.drop(df.columns[[2, 3]], axis=1)
    print(df.to_csv(index=False))

    #convert to string, then to file for csv use
    df = df.to_csv(index=False)
    df = StringIO(df)
    return df


ds = merge_data_frames(ds1,ds2)


def generate_certs(csv_data_set):

    #create dir for certs
    os.system('mkdir ' + '"' + ks1_location.rsplit("\\",1)[0] + "\\" + 'keytoolcerts' + '"')

    csv_reader = csv.reader(csv_data_set)   #read as csv
    next(csv_reader)                        # ignore header line

    for line in csv_reader:  # loop through lines
        print(line[0]) # left value
        #print(line[1]) # right value

        export_cert_cmd = 'keytool -export -alias ' + '"'  + line[0] + '"' + ' -file ' + '"' + ks1_location.rsplit("\\",1)[0] + "\\" + 'keytoolcerts' + "\\" + line[0] + '.cer' + '"' + ' -keystore ' + '"' + ks1_location + '"' + ' -storepass ' + ks1_pass
        print(export_cert_cmd)

        #generate cert one by one
        os.system(export_cert_cmd)




generate_certs(ds)




