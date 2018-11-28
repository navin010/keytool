
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

