name =r'[C:\Users\lubhayan\Documents\Clients\Internal\KeystoreConsolidation\NewGlobalKS\aws\agrewcappo055v.rbi.web.ds\output.txt]'

format_name = name.replace('[', '').replace(']','')  # remove unnecessary line feeds

print(format_name)

leftLocation='as'

if (leftLocation != ''):
    print('got a value')
else:
    print('no value')