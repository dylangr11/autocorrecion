
import telnetlib
import time
import datetime
from celery import shared_task
from .connections_devices import setsnmp
from .connections_devices import walk
from .connections_devices import DataBaseHandler
from .connections_devices import telnet_commands
import ipaddress 
#import connections_devices
# from connections_devices import setsnmp
# from connections_devices import walk
# from connections_devices import DataBaseHandler
# from connections_devices import telnet_commands
import requests
from pysnmp.hlapi import *
from pymongo import MongoClient
from multiping import MultiPing
from pysnmp import debug

#debug.setLogger(debug.Debug('msgproc'))
#devices_panama= "10.247.2.172"
list_modelos =  ["ISCOM2948GF-4C-DC/D","ISCOM2924GF-4C-AC/D","ISCOM RAX711", "ISCOM2948GF-4C-AC/D","ISCOM2924GF-4GE-AC/D","ISCOM2924GF-4GE-DC/D","ISCOM2924GF-4C-DC/D","ISCOM2924GF-4GE-AC_DC","Gazelle S1508i","RAX711-L-4GC","RAX701-GC","Gazelle S1010i-GL","Gazelle S1010i","ISCOM2110EA-MA-WP"]
list_modelos2 = ["RAX711-C","RAX721-A"]
hw_scps = ["ISCOM2924GF-4C-AC_DC ""ISCOM2948GF-4C-AC_DC","ISCOM2948GF-4C-DC/D","ISCOM2924GF-4C-AC/D","ISCOM RAX711", "ISCOM2948GF-4C-AC/D","ISCOM2924GF-4GE-AC/D","ISCOM2924GF-4GE-DC/D","ISCOM2924GF-4C-DC/D","ISCOM2924GF-4GE-AC_DC","Gazelle S1508i","Gazelle S1006i","RAX711-L-4GC","RAX701-GC","RAX711-L-4GE","Gazelle S1010i-GL","Gazelle S1010i","ISCOM2110EA-MA-WP","Gazelle S1020i-2GF-4GE-GL-AC"]
hw_swas=  ["ISCOM2924GF-4C-AC_DC ","ISCOM2948GF-4C-DC/D","ISCOM2924GF-4C-AC/D", "ISCOM2948GF-4C-AC/D","ISCOM2924GF-4GE-AC/D","ISCOM2924GF-4GE-DC/D","ISCOM2924GF-4C-DC/D","ISCOM2924GF-4GE-AC_DC","ISCOM2948GF-4C-AC_DC"]
hw_snmp_servers_supported=["ISCOM2924GF-4C-AC_DC","ISCOM2948GF-4C-DC/D","ISCOM2924GF-4C-AC/D","ISCOM RAX711", "ISCOM2948GF-4C-AC/D","ISCOM2924GF-4GE-AC/D","ISCOM2924GF-4GE-DC/D","ISCOM2924GF-4C-DC/D","ISCOM2924GF-4GE-AC_DC","RAX711-L-4GC","RAX701-GC"]
hw_telnet_supported=["Gazelle S1508i","Gazelle S1006i","Gazelle S1010i-GL","Gazelle S1010i","ISCOM2110EA-MA-WP","Gazelle S1020i-2GF-4GE-GL-AC"]
current_date = str(datetime.date.today().strftime('%Y-%m-%d'))
url = 'http://10.250.55.232:8001/nosqlquery'
headers_produccion = {'Content-Type': 'application/x-www-form-urlencoded','Authorization': 'Basic M1l2bnNjN1REMUZLTVBCNmxBRm1VTjZsUWpnYTo2NzFLRkhaZll3U3ltY3pUb25yWnk3Rnp2TVlh','grant_type': 'client_credentials', 'Cookie':'route=1633372119.109.1387.952069'}
query_no_snmp_servers_scps={"query":"{\"snmp_servers.server\":{\"$ne\":\"10.250.55.26\"},\"hardware\":{\"$regex\":\"RAX711-L|RAX701|ISCOM RAX711\"}}","projection":"{\"ip_mgt\":1,\"hardware\":1,\"country\":1,\"snmp_community\":1,\"hostname\":1}"}
query_no_snmp_servers_swas={"query":"{\"snmp_servers.server\":{\"$ne\":\"10.201.0.2\"},\"hardware\":{\"$regex\":\"ISCOM29\"}}","projection":"{\"ip_mgt\":1,\"hardware\":1,\"country\":1,\"snmp_community\":1,\"hostname\":1}"}
query_no_ntp={"query":"{\"ver_discovery_control\":\""+current_date+"\",\"ntp_status\":{\"$ne\":\"3\"},\"interfaces_ip\":{\"$exists\":\"true\"},\"hardware\":{\"$regex\":\"RAX711-L|RAX701|ISCOM RAX711|ISCOM29\"}}","projection":"{\"ip_mgt\":1,\"hardware\":1,\"country\":1,\"snmp_community\":1,\"hostname\":1,\"interfaces_ip\":1,\"interfaces_ip.ip_address\":1,\"interfaces_ip.mask\":1}"}
query_no_ssh_raisecom={"query":"{\"ver_discovery_control\":\""+current_date+"\",\"ssh\":{\"$ne\":\"1\"},\"hardware\":{\"$regex\":\"RAX711-L|RAX701|ISCOM RAX711|ISCOM29\"}}","projection":"{\"ip_mgt\":1,\"hardware\":1,\"country\":1,\"snmp_community\":1,\"hostname\":1,\"interfaces_ip\":1,\"interfaces_ip.ip_address\":1,\"interfaces_ip.mask\":1}"}
#query_snmp_communities={"query":"{\"country\":{\"$regex\":\".*\"},\"ver_discovery_control\":\""+current_date+"\",\"snmp_servers\":{\"$exists\":\"true\"},\"hardware\":{\"$regex\":\"ISCOM21|Gazelle\"}}","projection":"{\"ip_mgt\":1,\"hardware\":1,\"country\":1,\"snmp_community\":1,\"hostname\":1}"}
query_snmp_communities={"query":"{\"country\":{\"$regex\":\".*\"},\"ver_discovery_control\":\""+current_date+"\",\"snmp_servers\":{\"$exists\":\"true\"},\"hardware\":{\"$regex\":\"RAX711-L|RAX701|ISCOM RAX711|ISCOM29|ISCOM21|Gazelle\"}}","projection":"{\"ip_mgt\":1,\"hardware\":1,\"country\":1,\"snmp_community\":1,\"hostname\":1}"}
#query_snmp_communities={"query":"{\"ip_mgt\":{\"$regex\":\""+devices_panama+"\"},\"snmp_servers\":{\"$exists\":\"true\"},\"hardware\":{\"$regex\":\"RAX711-L|RAX701|ISCOM RAX711|ISCOM29|ISCOM21|Gazelle\"}}","projection":"{\"ip_mgt\":1,\"hardware\":1,\"country\":1,\"snmp_community\":1,\"hostname\":1}"}
sql_group_ips=DataBaseHandler.get_all_ip_mgt()



def get_query(url,query):    
    
    response = requests.request("POST",url,data=query)
    jresponse= response.json()
    print("EL TAMAÑO DE JRESPONSE "+str(len(jresponse)))
    return jresponse

##Verificar acceso por telnet en equipos Raisecom##
def verifAcceso(host,username,password):

    command= "clear\n"
    command2="exit\n"
    term= "term len 0"
    regex = [
        b"[Ll]ogin.",
        b"[Uu]sername",
        b"[Pp]assword",
        b"expired!",
        b'$']
    try:    
        tn = telnetlib.Telnet(host, timeout = 5)
        tn.setsnmp_debuglevel(1)
        tn.expect([b"Login:"],5)
        tn.write(username.encode('ascii'))
        tn.expect([b"Password:"],5)
        tn.write(password.encode('ascii'))
        tn.expect([b".*#"],3)
        tn.expect(regex,3)
        tn.write(command.encode('ascii')+b"\n")
        tn.write(command2.encode('ascii')+b"\n")
        a= tn.read_until(b".*#",3)
        tn.close()
        b=a.decode("ascii")
        #print(type(b))
        if str("#") not in b:
            var_registro=("Login Fail @@@@ "+host+"\n")
        else:
            var_registro=("Login OK @@@@ "+host+"\n")
    except:
        var_registro=("Login Fail "+host+"\n")
    op=open ("outputValidacionAcceso.txt", "a").write(var_registro)
    print (var_registro)
    
def singleTacacsServer(host,username,password, server):
    command_end = "end\n"
    command_exit = "exit\n"
    command_write = "write\n"
    term= "terminal page-break disable\n"
    regex = [
        b"[Ll]ogin.",  # b"[Ll]ogin" works here
        b"[Uu]sername",
        b"[Pp]assword",
        b"expired!",
        b'$']

    print ("Inicio")

    if server == "1":
        with open ("commands_single_server_GT.txt", "r") as commandlist:
          commandslist = []
          commandslist = commandlist.readlines()
    elif server == "2":
        with open ("commands_single_server_CO.txt", "r") as commandlist:
          commandslist = []
          commandslist = commandlist.readlines()


    print ("Ejecutando: "+host)
    try:
        tn = telnetlib.Telnet(host, timeout = 10)
        tn.setsnmp_debuglevel(1)
        tn.expect([b"Login:"],5)
        tn.write(username.encode('ascii'))
        tn.expect([b"Password:"],5)
        tn.write(password.encode('ascii'))
        tn.expect([b".*#"],3)
        tn.expect(regex,3)
        tn.write(term.encode('ascii'))
        for commands in commandslist:
            tn.expect([b".*#"],3)
            tn.write(commands.encode('ascii')+b"\n")    
        tn.expect([b".*#"],10)
        tn.write(command_write.encode('ascii')+b"\n")
        tn.expect([b".*#"],3)
        tn.write(command_exit.encode('ascii')+b"\n")
        tn.expect([b".*#"],3)
        read = tn.read_until(b".*#",8)
        tn.close()
        output=read.decode("ascii")
        if str("#") in output:
            var_registro=("OK @@@@ "+host+"\n")
        else:
            var_registro=("FAIL @@@@ "+host+"\n")
    except:
        var_registro=("FAIL @@@@ "+host+"\n")
    op=open ("outputrevision.txt", "w").write(var_registro)
    print (var_registro)

def snmp_server_traps (ip_address,community,hw,device_type):
    if device_type!=None:
        oid_ip= '1.3.6.1.6.3.12.1.2.1.7' #Se le envia un string con la IP
        oid_comunnity='1.3.6.1.6.3.12.1.3.1.4' #Se le envia un string con la comunidad ufinet
        oid_ip_port = '1.3.6.1.6.3.12.1.2.1.3' #Se le envia un hex 0A C9 00 02 00 A2 (CR) y '0A FA 37 1A 00 A2' (GT)
        oid_object_id= '1.3.6.1.6.3.12.1.2.1.2.' #Se le envia un estandar Object id 1.3.6.1.6.1.1
        oid_snmp_version='1.3.6.1.6.3.12.1.3.1.3' #se le envia un int 2
        oid_value = '1.3.6.1.6.3.12.1.3.1.2' #se le envia un 1
        oid_value2= '1.3.6.1.6.3.12.1.3.1.5' #se le envia un 1
        oid_standar= '1.3.6.1.6.3.12.1.2.1.6' #Se envia un string 'rfc1493 tmscom rfc2233 rfc1757 rfc1907 rfc1850'
        oid_activate_param='1.3.6.1.6.3.12.1.3.1.7' #Se envia un integer de 1 
        oid_activate_status= '1.3.6.1.6.3.12.1.2.1.9' #Se envia un integer de 1
        server_gt_code='49.48.46.50.53.48.46.53.53.46.50.54'
        server_cr_code='49.48.46.50.48.49.46.48.46.50'
        server_gt = '10.250.55.26'
        server_cr = '10.201.0.2'
        str_cr_p='0AC9000200A2'
        base16INTcr = OctetString(hexValue='0AC9000200A2')
        str_gt_p='0AFA371A00A2'
        base16INTgt = OctetString(hexValue='0AFA371A00A2')
        lista_servers=[]
        print("LLAMADO DE WALK")
        snmp_servers=walk(str(ip_address),community,'1.3.6.1.6.3.12.1.2.1.3')
        print(snmp_servers)
        for key in snmp_servers:
            list_values = key.split(".")
            new_list=[]
            for number in list_values:
                ip_cast=chr(int(number))
                new_list.append(ip_cast)

            server_ip_trap= ''.join(new_list)
            lista_servers.append(server_ip_trap)
        data=[]
        data.append(ip_address)
        community_to_apply='ufinet' if device_type=='SCP' else 'pnrw-med'
        server_to_apply_cr= True if device_type=='SWA' else False
        save=False
        if lista_servers!=None and (not server_gt in lista_servers or not server_cr in lista_servers):
            if not server_cr in lista_servers and server_to_apply_cr and hw in hw_snmp_servers_supported:
                data.append(setsnmp(str(ip_address),community,oid_ip+'.'+server_cr_code,str(server_cr)))
                data.append(setsnmp(str(ip_address),community,oid_comunnity+'.'+server_cr_code,str(community_to_apply)))
                data.append(setsnmp(str(ip_address),community,oid_ip_port+'.'+server_cr_code,base16INTcr))
                data.append(setsnmp(str(ip_address),community,oid_object_id+'.'+server_cr_code,str('1.3.6.1.6.1.1')))
                data.append(setsnmp(str(ip_address),community,oid_snmp_version+'.'+server_cr_code,Integer32(2)))
                data.append(setsnmp(str(ip_address),community,oid_value+'.'+server_cr_code,Integer32(1)))
                data.append(setsnmp(str(ip_address),community,oid_value2+'.'+server_cr_code,Integer32(1)))
                data.append(setsnmp(str(ip_address),community,oid_standar+'.'+server_cr_code,str('rfc1493 tmscom rfc2233 rfc1757 rfc1907 rfc1850')))
                data.append(setsnmp(str(ip_address),community,oid_activate_param+'.'+server_cr_code,int(1)))
                data.append(setsnmp(str(ip_address),community,oid_activate_status+'.'+server_cr_code,int(1)))
                save=True
            if not server_cr in lista_servers and server_to_apply_cr and hw in hw_telnet_supported:
                list_commands_rc=["config t","snmp-server host "+str(server_cr)+" version 2c "+str(community_to_apply),'exit']
                telnet_commands(ip_address,"dgonzalo\n","Gonza27*\n",list_commands_rc,8)

            if not server_gt in lista_servers and not server_to_apply_cr and hw in hw_snmp_servers_supported:
                data.append(setsnmp(str(ip_address),community,oid_ip+'.'+server_gt_code,str(server_gt)))
                data.append(setsnmp(str(ip_address),community,oid_comunnity+'.'+server_gt_code,str(community_to_apply)))
                data.append(setsnmp(str(ip_address),community,oid_ip_port+'.'+server_gt_code,base16INTgt))
                data.append(setsnmp(str(ip_address),community,oid_object_id+'.'+server_gt_code,str('1.3.6.1.6.1.1')))
                data.append(setsnmp(str(ip_address),community,oid_snmp_version+'.'+server_gt_code,Integer32(2)))
                data.append(setsnmp(str(ip_address),community,oid_value+'.'+server_gt_code,Integer32(1)))
                data.append(setsnmp(str(ip_address),community,oid_value2+'.'+server_gt_code,Integer32(1)))
                data.append(setsnmp(str(ip_address),community,oid_standar+'.'+server_gt_code,str('rfc1493 tmscom rfc2233 rfc1757 rfc1907 rfc1850')))
                data.append(setsnmp(str(ip_address),community,oid_activate_param+'.'+server_gt_code,int(1)))
                data.append(setsnmp(str(ip_address),community,oid_activate_status+'.'+server_gt_code,int(1)))
                save=True
            
            if not server_gt in lista_servers and not server_to_apply_cr and hw in hw_telnet_supported:
                list_commands_rc=["config t","snmp-server host "+str(server_gt)+" version 2c "+str(community_to_apply),'exit']
                telnet_commands(ip_address,"dgonzalo\n","Gonza27*\n",list_commands_rc,8)

            time.sleep(2)
            if save:
                save_config_raisecom(ip_address,community)
        
        else:
            data.append(lista_servers)
            print(str(data) +" Ya configurado")
    else:
        print("Device Type NONE")

def save_config_raisecom(ip_address,community):
    write=setsnmp(str(ip_address),community,'1.3.6.1.4.1.8886.1.2.1.1.0',Integer32(2))
    print(str(ip_address)+' '+str(write))

def device_type_classifier(hardware,hostname):
    dev_type=''
    if 'SWAUFN' in hostname and hardware in hw_swas:
        dev_type='SWA'
    elif hardware in hw_scps:
        dev_type='SCP'
    else:
        dev_type='UNDEFINED'
    return dev_type

##QUERYs TO CALL METHODS FOR SNMP_SERVERS
#devices_snmp_communities=get_query(url,query_snmp_communities)

@shared_task(bind=True)   
def main_basic(self):
    #SNMP_SERVERS_DEMARCADORES
    devices_snmp_servers=get_query(url,query_no_snmp_servers_scps)
    for devices in devices_snmp_servers:
        process_snmp.delay(devices)
    #SNMP_SERVERS_SWAS
    devices_snmp_servers=get_query(url,query_no_snmp_servers_swas)
    for devices in devices_snmp_servers:
        process_snmp.delay(devices)
    #NO NTP
    devices_ntp=get_query(url,query_no_ntp)
    for device_ntp in devices_ntp:
        if "ip_mgt" in device_ntp.keys() and "interfaces_ip" in device_ntp.keys() and "snmp_community" in device_ntp.keys():
            ip_addr=device_ntp["ip_mgt"]
            interfaces_ips=device_ntp["interfaces_ip"]
            community_snmp=device_ntp["snmp_community"]
            community_rw=community_snmp["community"]
            ntp_configurator.delay(ip_addr,interfaces_ips,community_rw)
    #NO SSHs
    devices_without_ssh=get_query(url,query_no_ssh_raisecom)
    for device_no_ssh in devices_without_ssh:
        ssh_configurator.delay(device_no_ssh)
    #COMUNIDADES SNMP
    
    devices_snmp_communities=get_query(url,query_snmp_communities)
    print(devices_snmp_communities)
    for devices in devices_snmp_communities:
        procces_communities.delay(devices)

def main_basic_sync():
    #SNMP_SERVERS_DEMARCADORES
    devices_snmp_servers=get_query(url,query_no_snmp_servers_scps)
    for devices in devices_snmp_servers:
        process_snmp(devices)
    #SNMP_SERVERS_SWAS
    devices_snmp_servers=get_query(url,query_no_snmp_servers_swas)
    for devices in devices_snmp_servers:
        process_snmp(devices)
    #NO NTP
    devices_ntp=get_query(url,query_no_ntp)
    for device_ntp in devices_ntp:
        if "ip_mgt" in device_ntp.keys() and "interfaces_ip" in device_ntp.keys() and "snmp_community" in device_ntp.keys():
            ip_addr=device_ntp["ip_mgt"]
            interfaces_ips=device_ntp["interfaces_ip"]
            community_snmp=device_ntp["snmp_community"]
            community_rw=community_snmp["community"]
            ntp_configurator(ip_addr,interfaces_ips,community_rw)
    #NO SSHs
    devices_without_ssh=get_query(url,query_no_ssh_raisecom)
    for device_no_ssh in devices_without_ssh:
        ssh_configurator(device_no_ssh)
    #COMUNIDADES SNMP
    
    devices_snmp_communities=get_query(url,query_snmp_communities)
    print(devices_snmp_communities)
    for devices in devices_snmp_communities:
        procces_communities(devices)

@shared_task(bind=True)   
def process_snmp(self,devices):
    list_ip=[]
    ip_addr=devices["ip_mgt"]
    hardware=devices["hardware"]
    hostname=devices["hostname"]
    communities=devices["snmp_community"]
    valid=False
    community_rw=communities["rw"]
    if community_rw:
        community=communities["community"]
        valid=True
    else:
        print("No es de escritura")
        valid=False
    dev_type=device_type_classifier(hardware,hostname)
    list_ip.append(ip_addr)
    ping_host= MultiPing(list_ip)
    ping_host.send()
    response, no_responses=ping_host.receive(1)
    print("INICIANDO")
    print(no_responses)
    if response and valid:
        print(ip_addr)
        print(hardware)
        print(community)
        print("Processing "+ip_addr+" hardware "+hardware)
        snmp_server_traps(ip_addr,community,hardware,dev_type)

#test= {"ip_mgt":"10.234.159.9",'hardware':'RAX711-L-4GC','hostname':'CRSJEZULABSCPUFN03','snmp_community':{"community":"private",'rw':True}}
#process_snmp(test)
    



#     #CAMBIO DE USER LOGIN 
def change_user_login(usermethod,addr,community):
#       #" 1 - Autenticacion local"+'\n',"9 - Autenticacion de tacacs_local_no_response")
        if usermethod == "1" or usermethod =="9": 
            oid_user_method = '1.3.6.1.4.1.8886.1.2.2.1.0'
            model=walk(str(addr),community,'1.3.6.1.4.1.8886.6.1.1.1.19')
            if not model:
                model=walk(str(addr),community, '1.3.6.1.4.1.8886.6.1.1.1.2')
            if str(model.get("0")) in list_modelos:
                try:
                    setsnmpvalue=setsnmp(str(addr),community, oid_user_method ,Integer32(usermethod))
                    print(addr,"Se aplico el valor", usermethod, setsnmpvalue)
                except:
                    print("Error: ", addr)
            else:
                print(addr," Equipo no responde a comunidad o modelo inválido:", model.get("0"))
        else:
           print("Numero invalido")
def create_emergency_user_raisecom(addr,community):
        oid_privilage = '1.3.6.1.4.1.8886.1.2.2.5.1.3.0.0.0.0.10.101.109.101.114.103.101.110.99.105.97'
        value_privilage= Integer32(15)
        emergUser = '0.0.0.0.10.101.109.101.114.103.101.110.99.105.97'
        oid_password = '1.3.6.1.4.1.8886.1.2.2.5.1.6.0.0.0.0.10.101.109.101.114.103.101.110.99.105.97'
        value_password = OctetString(hexValue='56cd6c12fa0fd4188cb85bb826370be7')
        oid_user = '1.3.6.1.4.1.8886.1.2.2.5.1.8.0.0.0.0.10.101.109.101.114.103.101.110.99.105.97'
        value_user = Integer32(4)
        try:
            model=walk(str(addr),community,'1.3.6.1.4.1.8886.6.1.1.1.19')
            if str(model.get("0")) in list_modelos:
                users=walk(str(addr),community,'1.3.6.1.4.1.8886.1.2.2.5.1.8')
                print(users)
                if emergUser not in users:
                    setsnmp(addr,community,oid_privilage,value_privilage)
                    setsnmp(addr,community,oid_password,value_password)
                    setsnmp(addr,community,oid_user,value_user)
                else:
                    print(addr,' El usuario emergencia ya existe')
            else:
                print(addr," Equipo no responde a comunidad o modelo inválido:", model.get("0"))
        except:
            print("Error")
def serverAAA_config(serverAAA,addr,community):
        #(" 1 - Servidor de Guatemala"+'\n',"2 - Servidor de Colombia"+'\n')
        if serverAAA == "1" or serverAAA == "2":
            user= "emergencia"+"\n"
            passw = "3m3r1asd@"+"\n"
            model=walk(str(addr),'private','1.3.6.1.4.1.8886.6.1.1.1.19')
            if str(model.get("0")) in list_modelos:
                singleTacacsServer(addr,user,passw,serverAAA)
            else:
                print(addr," Equipo de otro modelo ", model)
        else:
            print("Seleccion incorrecta")
def delete_emergency_user_raisecom(addr,community):
        oid_user= '1.3.6.1.4.1.8886.1.2.2.5.1.8.0.0.0.0.10.101.109.101.114.103.101.110.99.105.97'
        emergUser = '0.0.0.0.10.101.109.101.114.103.101.110.99.105.97'
        model=walk(str(addr),'private','1.3.6.1.4.1.8886.6.1.1.1.19')
        if str(model.get("0")) in list_modelos:
            users=walk(str(addr),community,'1.3.6.1.4.1.8886.1.2.2.5.1.8')
            countUsers = sum(map(len, users.values()))
            if (countUsers > 1) and (emergUser in users):
                try:
                    ejecutarsetsnmp = setsnmp(str(addr),community, oid_user ,Integer32(6))
                    print(addr,"Se eliminó el usuario" , ejecutarsetsnmp)
                except:
                    print(addr," Error")
            else:
                print(addr, " Unico usuario", countUsers, " o usuario no existe, se debe crear")
        else:
            print(addr," Equipo no responde a comunidad o modelo inválido:", model.get("0"))
def verificar_usuario_aaa(addr,community):
        emergUser = '0.0.0.0.10.101.109.101.114.103.101.110.99.105.97'
        #try:
        model=walk(str(addr),community,'1.3.6.1.4.1.8886.6.1.1.1.19')
        if not model:
            model=walk(str(addr),community, '1.3.6.1.4.1.8886.6.1.1.1.2')
        if str(model.get("0")) in list_modelos: 
            users=walk(str(addr),community,'1.3.6.1.4.1.8886.1.2.2.5.1.8')
            auth=walk(str(addr),community,'1.3.6.1.4.1.8886.1.2.2.1')
            countUsers = sum(map(len, users.values()))
            print(users)
            if emergUser in users:
                print(addr,"- Si existe el usuario de emergencia - la autenticacion es:", auth)
            else:
                print(addr,"- No existe el usuario de emergencia- la autenticacion es:", auth)       
           # except:
           #     print("ERROR")
def verify_access(addr,community,user,passw):
        #print(user)
        #print(passw)
        username= user+"\n"
        password= passw+"\n"
        model=walk(str(addr),'private','1.3.6.1.4.1.8886.6.1.1.1.19')
        if str(model.get("0")) in list_modelos:
            verifAcceso(addr,str(username),str(password))
        else:
            print(addr," Equipo de otro modelo ", model) 

def lldp_neigh_verify(addr,community):
    #try:
        #admin_status=walk(str(addr),'private','1.3.6.1.2.1.2.2.1.7')
        oper_status=walk(str(addr),community,'1.3.6.1.2.1.2.2.1.8')
        lldp_status=walk(str(addr),community,'1.3.6.1.4.1.8886.6.1.57.2.1.1')
        #model=walk(str(addr),'private','1.3.6.1.4.1.8886.6.1.1.1.19')       
        if lldp_status.get("0")== "2":
            print(addr+"@@ LLDP DISABLE")
        elif lldp_status.get("0")== "1":
            #print(addr+" LLDP ENABLE")
            lldp_ports = walk(str(addr),community,'1.3.6.1.4.1.8886.6.1.57.2.2.1.1.2')
            for port in lldp_ports: 
                if lldp_ports.get(port) =="2":
                    print(addr+"@@ puerto @@"+port+"@@ LLDP_DISABLE @@"+ str(oper_status.get(port)))
                if lldp_ports.get(port) =="1":
                    print(addr+"@@ puerto @@"+port+"@@ LLDP_ENABLE @@"+str(oper_status.get(port)))
    #except:
        #print(addr," Error")
def lldp_neighbor_activation(device):       
    #try:
        #admin_status=walk(str(addr),'private','1.3.6.1.2.1.2.2.1.7')
        oid_lldp='1.3.6.1.4.1.8886.6.1.57.2.1.1.0'
        #REVISAR el query con el API
        #query=db_inventory.Devices.find({"ip_mgt":addr},{"interfaces":1,"hostname":1,"_id":0,"interfaces.name":1,"interfaces.qinq":1,"interfaces.description":1,"interfaces.operational_status":1,"interfaces.switchport_mode":1,"_id":0, "interfaces.index":1, "interfaces.admin_status":1})
        oid_lldp_ports='1.3.6.1.4.1.8886.6.1.57.2.2.1.1.2'
        for record in device:
            dev=record
            addr=record["ip_mgt"]
        ##Se debe obtener toda la información de device
        #print(dev)
        #admin_status=walk(str(addr),'private','1.3.6.1.2.1.2.2.1.8')
        lldp_status=walk(str(addr),'private','1.3.6.1.4.1.8886.6.1.57.2.1.1')
        if lldp_status.get("0")== "2":
            print(addr+"@@ LLDP DISABLE")
            lldp_activate = setsnmp(str(addr),'private', oid_lldp ,Integer32(1))
            lldp_status2=walk(str(addr),'private','1.3.6.1.4.1.8886.6.1.57.2.1.1')  
        #model=walk(str(addr),'private','1.3.6.1.4.1.8886.6.1.1.1.19')       
            if lldp_status2.get("0") == "1":
                lldp_ports = walk(str(addr),'private','1.3.6.1.4.1.8886.6.1.57.2.2.1.1.2')
                for value in dev["interfaces"]:
                    if "switchport_mode" in value.keys() and "qinq" in value.keys():
                        admin_status=value["admin_status"]
                        switchport_mode=value["switchport_mode"]
                        operational_status=value["operational_status"]
                        qinq=value["qinq"]
                        port=value["index"]
                        if admin_status=="1" and switchport_mode=="2" and lldp_ports.get(port)=="2" and qinq =="1":                    
                            lldp_port_activate = setsnmp(str(addr),'private', oid_lldp_ports+"."+port,Integer32(1))
                            print(addr+"@@ puerto @@"+port+ " status " + str(lldp_port_activate) +" "+admin_status)
                        elif lldp_ports.get(port) =="1":
                            print(addr+"@@ puerto @@"+port+"@@ No changes needed @@"+admin_status)
            else:
                print(addr+"@@ ERROR LLDP ACTIVATION")
        elif lldp_status.get("0")== "1":              
            lldp_ports = walk(str(addr),'private','1.3.6.1.4.1.8886.6.1.57.2.2.1.1.2')
            for value in dev["interfaces"]:
                if "switchport_mode" in value.keys() and "qinq" in value.keys():
                    admin_status=value["admin_status"]
                    switchport_mode=value["switchport_mode"]
                    operational_status=value["operational_status"]
                    qinq=value["qinq"]
                    port=value["index"]
                    if admin_status=="1" and switchport_mode=="2" and lldp_ports.get(port)=="2" and qinq =="1":                    
                        lldp_port_activate = setsnmp(str(addr),'private', oid_lldp_ports+"."+port,Integer32(1))
                        print(addr+"@@ puerto @@"+port+ " status " + str(lldp_port_activate) +" "+admin_status)
                    elif lldp_ports.get(port) =="1":
                        print(addr+"@@ puerto @@"+port+"@@ No changes needed @@"+admin_status)
        #print(addr," Error")
def snmp_server_traps_validator(addr,community):
    lista_servers=[]
    snmp_servers=walk(str(addr),community,'1.3.6.1.6.3.12.1.2.1.3')
    for key in snmp_servers:
        list_values = key.split(".")
        new_list=[]
        for number in list_values:
            ip_cast=chr(int(number))
            new_list.append(ip_cast)

        server_ip_trap= ''.join(new_list)
        lista_servers.append(server_ip_trap)
    print(lista_servers)
def delete_snmp_server_traps(addr,community):
    print(" 1 - Eliminar Servidor CR"+'\n',"2 - Eliminar Servidor GT"+'\n',"3 - Eliminar Servidor Spectrum"+'\n',"4 - Eliminar todos los servidores")
    serverdelete=input("Ingrese la opcion a configurar [1-4]:")
    oid_activate_param='1.3.6.1.6.3.12.1.3.1.7' #Se envia un integer de 6 para eliminar
    oid_activate_status= '1.3.6.1.6.3.12.1.2.1.9' #Se envia un integer de 6 para eliminar
    server_gt_code='49.48.46.50.53.48.46.53.53.46.50.54'
    server_cr_code='49.48.46.50.48.49.46.48.46.50'
    server_spectrum_code='49.48.46.49.48.57.46.50.49.48.46.49.48'
    server_gt = '10.250.55.26'
    server_cr = '10.201.0.2'
    server_spectrum = '10.109.210.10'
    server_pf='10.109.210.14'
    server_pf_code='49.48.46.49.48.57.46.50.49.48.46.49.52'
    lista_servers=[]
    snmp_servers=walk(str(addr),'private','1.3.6.1.6.3.12.1.2.1.3')
    for key in snmp_servers:
        list_values = key.split(".")
        new_list=[]
        for number in list_values:
            ip_cast=chr(int(number))
            new_list.append(ip_cast)

        server_ip_trap= ''.join(new_list)
        lista_servers.append(server_ip_trap)
    data=[]
    data.append(addr)
    change=False
    if lista_servers!=None and ( server_gt in lista_servers or server_cr in lista_servers or server_pf in lista_servers or server_spectrum in lista_servers) and serverdelete in ["1","2","3","4"]:
        print(lista_servers)
        if server_cr in lista_servers and (serverdelete=="1" or serverdelete=="4"):
            data.append(setsnmp(str(addr),'private',oid_activate_param+'.'+server_cr_code,int(6)))
            data.append(setsnmp(str(addr),'private',oid_activate_status+'.'+server_cr_code,int(6)))
            change=True
        
        if server_gt in lista_servers and (serverdelete=="2" or serverdelete=="4"):
            data.append(setsnmp(str(addr),'private',oid_activate_param+'.'+server_gt_code,int(6)))
            data.append(setsnmp(str(addr),'private',oid_activate_status+'.'+server_gt_code,int(6)))
            change=True

        if (serverdelete=="3" or serverdelete=="4"):
            if server_spectrum in lista_servers:
                data.append(setsnmp(str(addr),'private',oid_activate_param+'.'+server_spectrum_code,int(6)))
                data.append(setsnmp(str(addr),'private',oid_activate_status+'.'+server_spectrum_code,int(6)))
                change=True
            if server_pf in lista_servers:
                data.append(setsnmp(str(addr),'private',oid_activate_param+'.'+server_pf_code,int(6)))
                data.append(setsnmp(str(addr),'private',oid_activate_status+'.'+server_pf_code,int(6)))
                change=True
        
        print(data)
        if change:
            time.sleep(1)
            write=setsnmp(str(addr),'private','1.3.6.1.4.1.8886.1.2.1.1.0',Integer32(2))            
    else:
        data.append(lista_servers)
        print(str(data) +" No hay servers que eliminar/Entrada incorrecta")
@shared_task(bind=True)
def procces_communities(self,devices):
    list_ip=[]
    ip_addr=devices["ip_mgt"]
    hardware=devices["hardware"]
    hostname=devices["hostname"]
    communities=devices["snmp_community"]
    valid=False
    community_rw=communities["rw"]
    if community_rw:
        community=communities["community"]
        valid=True
    else:
        print("No es de escritura")
        valid=False
    dev_type=device_type_classifier(hardware,hostname)
    list_ip.append(ip_addr)
    ping_host= MultiPing(list_ip)
    ping_host.send()
    response, no_responses=ping_host.receive(1)
    print("INICIANDO PRUEBAS DE PING Y VALIDACION DE COMUNIDAD")
    if response and valid:
        if dev_type == 'SWA' and 'ISCOM29' in hardware:
            standard_communities(ip_addr,community,'pnrw-med',True)
        elif dev_type == 'SCP' and ('RAX711-L' in hardware or 'RAX701' in hardware or 'ISCOM RAX711' in hardware or 'ISCOM29' in hardware):
            standard_communities(ip_addr,community,'ufinet',True)
        elif dev_type == 'SCP' and ('Gazelle' in hardware or 'ISCOM21' in hardware):
            standard_communities(ip_addr,community,'ufinet',False)
        else:
            print("ENTRO Dispositivo "+hardware+" de tipo "+dev_type+" con la ip "+ip_addr+" respondio "+str(response)+" la comunidad es valida "+str(valid))
    else:
        print("Dispositivo de tipo "+dev_type+" con la ip "+ip_addr+" respondio "+str(response)+" la comunidad es valida "+str(valid))
        
#CONFIGURAR COMUNIDAD EN SWITCHES DE ACCESO Y SWITCHES RAISECOM MODELOS RAX e ISCOM ( new_community 'ufinet' o 'pnrw-med')
def standard_communities(addr,snmp_community,new_community,snmp_support):
        comunidad='1.3.6.1.4.1.8886.6.1.10.1.1.2' # -> String 'pnrw-med'
        comm_view='1.3.6.1.4.1.8886.6.1.10.1.1.3' #-> String 'internet'
        permisos='1.3.6.1.4.1.8886.6.1.10.1.1.4' #-> i = 1 (Permisos de lectura = 1 y escritura = 2)
        status='1.3.6.1.4.1.8886.6.1.10.1.1.5' #-> i = 4 (1 activo y 4 es createandgo) 
        community='pnrw-med'
        comm=[]
        index_free=''
        community_list=walk(str(addr),snmp_community,'1.3.6.1.4.1.8886.6.1.10.1.1.2')
        comm.append(addr)
        for index in community_list:
            if community_list[index]=="":
                index_free=index
                break     
        if not str(new_community) in community_list.values() and not index_free == "" and snmp_support:
            comm.append(setsnmp(str(addr),snmp_community,comunidad+'.'+str(index_free),OctetString(new_community)))
            comm.append(setsnmp(str(addr),snmp_community,comm_view+'.'+str(index_free),OctetString("internet")))
            comm.append(setsnmp(str(addr),snmp_community,permisos+'.'+str(index_free),Integer32(1)))
            comm.append(setsnmp(str(addr),snmp_community,status+'.'+str(index_free),Integer32(4)))
            time.sleep(2)
            comm.append(setsnmp(str(addr),snmp_community,'1.3.6.1.4.1.8886.1.2.1.1.0',Integer32(2)))
            print(str(comm) +"Se configuro la comunidad")
        elif not snmp_support and not str(new_community) in community_list.values():
            list_commands_rc=["config t","snmp-server community ufinet ro",'exit']
            telnet_commands(addr,"dgonzalo\n","Gonza27*\n",list_commands_rc,8)
            print(str(comm)+" Se configuro la comunidad por telnet")
        elif index_free=='':
            print(str(comm) +" no hay index disponibles") 
        else:
            print(str(comm) +" ya esta la comunidad")        
@shared_task(bind=True)
def ntp_configurator(self,addr,interfaces_ip,community):
    validation1=False
    validation2=False
    list_comando=[]
    ip_network=None
    comando_raisecom="ntp server"
    try:
        if interfaces_ip != None:
            list_ip=[]
            for interfaces in interfaces_ip:
                if "ip_address" in interfaces.keys() and "mask" in interfaces.keys():
                    ip_add=interfaces["ip_address"]
                    if ip_add==addr:
                        netmask=interfaces["mask"]
                        list_ip.append(addr)
                        list_ip.append(netmask)
                        ipaddr_mask="/".join(list_ip)
                        print(ipaddr_mask)
                        ip_network=str(ipaddress.IPv4Network(ipaddr_mask,strict=False))
                        if ip_network!=None:
                            validation1=True
                            print(validation1)
                            break
                        print("La red del equipo "+ip_network)
                        
            for tuplas in sql_group_ips:
                network=str(tuplas[1])
                gateway=str(tuplas[8])
                if network==ip_network:
                    ip_gateway=gateway
                    if ip_gateway!=None:
                        validation2=True
                        print(validation2)
                        break
            if validation1 & validation2:
                comando=comando_raisecom+" "+ip_gateway
                list_comando=["clock timezone - 0 0 UTC","config t"]
                list_comando.append(comando)
                telnet_commands(addr,"dgonzalo\n","Gonza27*\n",list_comando,3)
                time.sleep(1)
                save_config_raisecom(addr,community)
    except:
        print("Hubo un error")


@shared_task(bind=True)
def ssh_configurator(self,device):
    ip_address=device["ip_mgt"]
    communities=device["snmp_community"]
    valid=False
    community_rw=communities["rw"]
    if community_rw:
        community=communities["community"]
        valid=True
    list_commands_rc=["config t","generate ssh-key 2048","ssh2 server",'exit']
    if ip_address:
        telnet_commands(ip_address,"dgonzalo\n","Gonza27*\n",list_commands_rc,120)
        time.sleep(3)
        if valid:
            save_config_raisecom(ip_address,community)

#main_basic_sync()
#main_basic()

