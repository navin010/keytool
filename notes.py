
output_path=r'C:\Users\lubhayan\Documents\Clients\Internal\KeystoreConsolidation\NewGlobalKS\aws\agrewcappo055v.rbi.web.ds\output.txt'

with open(output_path, "w") as text_file:
    text_file.write(find_replace_input_ks_output)


csv_reader = csv.reader(buff)   #read as csv
for line in csv_reader:  # loop through lines
    print(line[0])
    print(line[3])
    #cat1_value = line[0]  # left value
    #cat2_value = line[1]  # right value


test = output_path.rsplit("\\",1)[0]
print('op = ' + test)


test = 'mkdir ' + '"' + ks1_location.rsplit("\\",1)[0] + "\\" + 'keytoolcerts' + '"'
print('op = ' + test)


ks1_keytoolscerts = ks1_location.rsplit("/", 1)[0] + "/" + 'keytoolcerts'  # create dir for certs
os.system('mkdir ' + '"' + ks1_keytoolscerts + '"')  # make temporary directory for exported certs
csv_reader = csv.reader(ds)  # read as csv
next(csv_reader)  # ignore header line
for index, line in enumerate(csv_reader):  # loop through lines, enumeration required for indexing
    alias = line[0]  # left csv value
    export_cert_cmd = 'keytool -export -alias ' + '"' + alias + '"' + ' -file ' + '"' + ks1_keytoolscerts + "/" + alias + '.cer' + '"' + ' -keystore ' + '"' + ks1_location + '"' + ' -storepass ' + ks1_pass
    os.system(export_cert_cmd)
    alias_checked = keytool.check_alias_unique(alias, ds2_nd)  # check using right/second non dropped data store
    import_cert_cmd = 'keytool -importcert -file ' + '"' + ks1_keytoolscerts + "/" + alias + '.cer' + '"' + ' -keystore ' + '"' + ks2_location + '"' + ' -storepass ' + ks2_pass + ' -alias ' + '"' + str(
        alias_checked) + '"'
    os.system(import_cert_cmd)
os.system('rd /s /q ' + '"' + ks1_keytoolscerts + '"')  # remove temp dir and files(/s) quietly(/q)



terminal_output_string = subprocess.check_output(terminal_output, shell=True)  # read input from cmd


def sendCommand(self):
    sender = self.sender()  # find button sending
    if sender.text() == 'Yes':
        # return os.system('yes')
        subprocess.call('yes', shell=True)
    if sender.text() == 'No':
        command = 'keytool -importcert -file "C:/Users/lubhayan/Documents/Clients/Internal/KeystoreConsolidation/NewGlobalKS/aws/agrewcappo055v.rbi.web.ds/keytoolcerts/nexus_testing_puto.cer" -keystore "C:/Users/lubhayan/Documents/Clients/Internal/KeystoreConsolidation/NewGlobalKS/aws/agrewcappo055v.rbi.web.ds/el_puto_2.jks" -storepass 3point142 -alias "nexus_testing_puto"'
        print(command)
        subprocess.call(command, shell=True)





try:
    self.buff1 = keytool.cmd_call_format(self.ks1_list, True, 'Left')
    self.buff2 = keytool.cmd_call_format(self.ks2_list, True, 'Right')
    self.buff2_nd = keytool.cmd_call_format(self.ks2_list, False,
                                            'Right')  # buff 2 for no dropped items, do not show print as it only for internal reference
except Exception as e:
    self.l3.setText(e)