import os
from io import StringIO
import pandas as pd
import csv


def cmd_command(ks_location, ks_pass):
    list_ks = "keytool -list -keystore " + '"' + ks_location + '"' + " -storepass " + ks_pass
    print(list_ks)
    return list_ks

def cmd_call_format(terminal_output, show_print, ks_number):
    terminal_output_string = os.popen(terminal_output).read()   # read input from cmd
    terminal_output_string_remove_lines = terminal_output_string.split("\n", 5)[5]  # remove first few unnecessary lines - split 5 times on \n and then take the 5th split value
    terminal_output_string_remove_crlf = terminal_output_string_remove_lines.replace(', \n', ', ')  # remove unnecessary line feeds
    if show_print == True:    # Print non internal references, buff2 is used as an internal references for the alias duplicate checks
        print("-------cmd Formatted Keystore " + ks_number + "-----------")
        print(terminal_output_string_remove_crlf)
    return StringIO(terminal_output_string_remove_crlf) # read string as file using buffer

def remove_columns(csv_file, dropdup, ks_number):
    df = pd.read_csv(csv_file, index_col=False, header=None, sep=',', names=['Alias','Date','Type','Fingerprint']) # create pandas data frame & read in and add headers for csv file
    df = df.drop(df.columns[[1, 2]], axis=1)  #drop unnecessary columns
    if dropdup == True:             #drop duplicate values on data set, do not drop for ds2_nd (no drop) as we need all the alias names
        df = df.drop_duplicates('Fingerprint')
        print("-------Pandas Formatted Keystore " + ks_number + "-----------")
        print(df.to_csv(index=False))
    return df

def merge_data_frames(df1, df2):
    df = pd.merge(df1, df2, on=['Fingerprint'], how='left', indicator=True).query('_merge == "left_only"')   #merge left, show indicator of both or left only and filter on left only
    df = df.drop(df.columns[[2, 3]], axis=1)  # drop unnecessary columns
    print("-------Pandas Merged -----------")
    print(df.to_csv(index=False))
    df = df.to_csv(index=False)    # convert to string, then to file for csv use
    df = StringIO(df)
    return df


def check_alias_unique(alias_name, data_set_right):
    exists = any(data_set_right.Alias == alias_name)    #check if alias name exists in data set column named 'Alias'
    print('Does alias ' + alias_name  + ' exist :' + str(exists))

    if exists == True :
        alias_name = alias_name + '9'
        print("Alias appended = " + alias_name)
        return check_alias_unique(alias_name, data_set_right)   # you have to use return when calling recursively
    else:
        print("Alias returned")
        print(alias_name)
        return alias_name


def generate_certs(csv_data_set, ds2_nd, ks1_location, ks1_pass, ks2_location, ks2_pass):
    print("-------Make Directory-----------")
    ks1_keytoolscerts = ks1_location.rsplit("/",1)[0] + "/" + 'keytoolcerts'  # create dir for certs
    print(ks1_keytoolscerts)
    os.system('mkdir ' + '"' + ks1_keytoolscerts + '"')   # make temporary directory for exported certs


    csv_reader = csv.reader(csv_data_set)   # read as csv
    next(csv_reader)                        # ignore header line

    for index, line in enumerate(csv_reader):  # loop through lines, enumeration required for indexing
        alias = line[0]  # left csv value

        # export cert one by one
        print('-------Export Certificate[' + str(index) + '] ' + '"' + alias + '"' + "-----------")
        export_cert_cmd = 'keytool -export -alias ' + '"'  + alias + '"' + ' -file ' + '"' + ks1_keytoolscerts + "/" + alias + '.cer' + '"' + ' -keystore ' + '"' + ks1_location + '"' + ' -storepass ' + ks1_pass
        print(export_cert_cmd)
        os.system(export_cert_cmd)

        #Check if alias name does not exist in the new keystore
        print("-------Check Alias[" + str(index) + '] ' + '"' + alias + '"' + " Does Not Exist in Right Keystore -----------")
        alias_checked = check_alias_unique(alias, ds2_nd)   #check using right/second non dropped data store

        # import certs one by one
        print('-------Import Certificate[' + str(index) + '] ' + '"' + alias + '" as "' + alias_checked  + '"-----------')
        import_cert_cmd = 'keytool -importcert -file ' + '"' + ks1_keytoolscerts + "/" + alias + '.cer' + '"' + ' -keystore ' + '"' + ks2_location + '"' + ' -storepass ' + ks2_pass + ' -alias ' + '"' + str(alias_checked) + '"'
        print(import_cert_cmd)
        os.system(import_cert_cmd)
        #os.system("pause")  #pause to allow for user input

    os.system('rd /s /q ' + '"' + ks1_keytoolscerts + '"')          #remove temp dir and files(/s) quietly(/q)
    print("-------Complete-----------")






