import os
from io import StringIO
import pandas as pd
import csv

# Paths
java_path= r'C:\Program Files\Java\jre1.8.0_181\bin'
ks1_location =r'C:\Users\lubhayan\Documents\Clients\Internal\KeystoreConsolidation\NewGlobalKS\aws\agrewcappo055v.rbi.web.ds\el_puto.jks'
ks1_pass = r'3point142'
ks2_location =r'C:\Users\lubhayan\Documents\Clients\Internal\KeystoreConsolidation\NewGlobalKS\aws\agrewcappo055v.rbi.web.ds\el_puto_2.jks'
ks2_pass = r'3point142'


os.chdir(java_path)

def cmd_command(ks_location, ks_pass):
    list_ks = "keytool -list -keystore " + '"' + ks_location + '"' + " -storepass " + ks_pass
    print(list_ks)
    return list_ks

ks1_list = cmd_command(ks1_location, ks1_pass)
ks2_list = cmd_command(ks2_location, ks2_pass)


def cmd_call_format(terminal_output, show_print):

    # read input from cmd
    terminal_output_string = os.popen(terminal_output).read()

    # remove first few unnecessary lines
    terminal_output_string_remove_lines = terminal_output_string.split("\n", 5)[5]  # split 5 times on \n and then take the 5th split value

    # remove unnecessary line feeds
    terminal_output_string_remove_crlf = terminal_output_string_remove_lines.replace(', \n', ', ')

    if show_print == True:
        print("-------op formatted -----------")
        print(terminal_output_string_remove_crlf)
        print("------------------")

    # read string as file using buffer
    return StringIO(terminal_output_string_remove_crlf)


buff1 = cmd_call_format(ks1_list, True)
buff2 = cmd_call_format(ks2_list, True)
buff2_nd = cmd_call_format(ks2_list, False)    #buff 2 for no dropped items, do not show print as it only for internal reference

def remove_columns(csv_file, dropdup):
    #create pandas data frame
    df = pd.read_csv(csv_file, index_col=False, header=None, sep=',', names=['Alias','Date','Type','Fingerprint']) #read in and add headers for csv file

    #drop unnecessary columns
    df = df.drop(df.columns[[1, 2]], axis=1)

    #drop duplicate values on data set
    if dropdup == True:
        df = df.drop_duplicates('Fingerprint')
        print(df.to_csv(index=False))

    return df


ds1 = remove_columns(buff1,True)
ds2 = remove_columns(buff2, True)
ds2_nd = remove_columns(buff2_nd, False)        #set dropping duplicates to False


def merge_data_frames(df1, df2):
    df = pd.merge(df1, df2, on=['Fingerprint'], how='left', indicator=True).query('_merge == "left_only"')   #merge left, show indicator of both or left only and filter on left only

    # drop unnecessary columns
    df = df.drop(df.columns[[2, 3]], axis=1)
    print(df.to_csv(index=False))

    #convert to string, then to file for csv use
    df = df.to_csv(index=False)
    df = StringIO(df)
    return df


ds = merge_data_frames(ds1,ds2)


def check_alias_unique(alias_name, data_set_right):
    print("***Alias Check = " + alias_name)

    alias_ds = data_set_right.Alias
    print(alias_ds)

    exists = any(data_set_right.Alias == alias_name)    #check if alias name exists in data set column named 'Alias'
    print("Does alias exist -> " + str(exists))

    if exists == True :
        alias_name = alias_name + '9'
        print("------Alias Appended------ = " + alias_name)
        return check_alias_unique(alias_name, data_set_right)   # you have to use return when calling recursively
    else:
        print("------Alias returned-------")
        print(alias_name)
        return alias_name



def generate_certs(csv_data_set):

    #create dir for certs
    ks1_keytoolscerts = ks1_location.rsplit("\\",1)[0] + "\\" + 'keytoolcerts'

    os.system('mkdir ' + '"' + ks1_keytoolscerts + '"')

    csv_reader = csv.reader(csv_data_set)   #read as csv
    next(csv_reader)                        # ignore header line

    for line in csv_reader:  # loop through lines
        alias = line[0]  # left csv value
        print(alias)
        #print(line[1]) # right value

        export_cert_cmd = 'keytool -export -alias ' + '"'  + alias + '"' + ' -file ' + '"' + ks1_keytoolscerts + "\\" + alias + '.cer' + '"' + ' -keystore ' + '"' + ks1_location + '"' + ' -storepass ' + ks1_pass
        print(export_cert_cmd)

        #export cert one by one
        os.system(export_cert_cmd)


        #Check if alias name does not exist in the new keystore
        alias_checked = check_alias_unique(alias, ds2_nd)
        print("------Alias will be using------")
        print(alias_checked)

        #import certs one by one
        import_cert_cmd = 'keytool -importcert -file ' + '"' + ks1_keytoolscerts + "\\" + alias + '.cer' + '"' + ' -keystore ' + '"' + ks2_location + '"' + ' -storepass ' + ks2_pass + ' -alias ' + '"' + str(alias_checked) + '"'
        print(import_cert_cmd)

        #import certs one by one
        os.system(import_cert_cmd)
        os.system("pause")  #pause to allow for user input

    #remove directory and certs
    os.system('rd /s /q ' + '"' + ks1_keytoolscerts + '"')          #remove dir and files(/s) quietly(/q)


generate_certs(ds)




