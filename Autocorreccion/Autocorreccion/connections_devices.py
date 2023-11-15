from asyncio import open_connection
import logging
import sys
import pyodbc
import telnetlib
from pysnmp.hlapi import *
from pymongo import MongoClient
from multiping import MultiPing
from pprint import pprint
from celery import shared_task


def nextwalk(host, community, oid_walk):
    iterator=nextCmd(SnmpEngine(), 
        CommunityData(community), UdpTransportTarget((host, 161)), ContextData(), 
        ObjectType(ObjectIdentity(oid_walk),'ifTable'), lexicographicMode=False)
    MAX_REPS = 500
    count = 0
    while(count < MAX_REPS):
        try:
            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
            print(varBinds[0].prettyPrint())
        except StopIteration:
            break

        count += 1

def walk(host, community, oid_walk):
    val_return = {}
    for (errorIndication,errorStatus,errorIndex,varBinds) in nextCmd(SnmpEngine(), 
        CommunityData(community), UdpTransportTarget((host, 161)), ContextData(), 
        ObjectType(ObjectIdentity(oid_walk)), lexicographicMode=False):
        if errorIndication:
            print(errorIndication, file=sys.stderr)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), 
                                file=sys.stderr)             
            break
        else:
            for oid, val in varBinds:
                id = (str(oid)[(len(str(oid_walk))+1):(len(str(oid)))])
                val_return[id] = str(val)
    return val_return
def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(ObjectType(ObjectIdentity(oid)))
    return object_types

def bulk(host, community, oid_walk):
    list_g=[]
    g = bulkCmd(SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((host, 161)),ContextData(),0, 25,
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr')))
    next(g)
    print(g)
    #list_g.append(g)
    return list_g

def setsnmp(host, community, oid_set, value):
    val_return = {}
    settest=setCmd(SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, 161)), 
        ContextData(),
        ObjectType(ObjectIdentity(oid_set), value),
        lookupMib=False)
    next(settest)
    for (errorIndication,errorStatus,errorIndex,varBinds) in settest:
        if errorIndication:
            print(errorIndication, file=sys.stderr)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'),file=sys.stderr)             
            break
        else:
            for oid, val in varBinds:
                #print('  %s = %s' % (oid, val))
                id = (str(oid)[(len(str(oid_set))+1):(len(str(oid)))])
                val_return[id] = str(val)
    return val_return
@shared_task(bind=True)
def telnet_commands(self,host,username,password,commandslist,wait):
    command_end = "end"
    command_exit = "exit"
    command_write = "write"
    term= "terminal page-break disable\n"
    list_enable_pass=["uficap07","Uf1n3t.C0l","raisecom"]
    regex = [
        b"[Ll]ogin.",  # b"[Ll]ogin" works here
        b"[Uu]sername",
        b"[Pp]assword",
        b"expired!",
        b'$']
    print ("Inicio")
    print ("Ejecutando: "+host)
    try:
        tn = telnetlib.Telnet(host, timeout = 20)
        tn.expect([b"Login:"],8)
        tn.write(username.encode('ascii'))
        tn.expect([b"Password:"],8)
        tn.write(password.encode('ascii'))
        need_enable= tn.expect([b".*>"],3)
        if '>' in str(need_enable):
            for passw in list_enable_pass:
                tn.write("enable".encode('ascii')+b"\n")
                tn.expect([b"Password:"],8)
                tn.write(passw.encode('ascii')+b"\n")
                check_enable_pass=tn.expect([b".*#"],3)
                print(check_enable_pass)
                if '#' in str(check_enable_pass): break
        tn.expect([b".*#"],3)
        tn.expect(regex,3)
        tn.write(term.encode('ascii'))
        for commands in commandslist:
            tn.expect([b".*#"],wait)
            tn.write(commands.encode('ascii')+b"\n")    
        tn.expect([b".*#"],10)
        tn.write(command_write.encode('ascii')+b"\n")
        save_message=tn.expect([b".*#"],15)
        tn.write(command_exit.encode('ascii')+b"\n")
        tn.expect([b".*#"],3)
        tn.close()
        #output=read.decode("ascii")
        if str(" successfully") in str(save_message):
            print(str(save_message))
            var_registro=("OK @@@@ "+host+"\n")
        else:
            print(str(save_message))
            var_registro=("FAIL @@@@ "+host+"\n")
    except:
        var_registro=("FAIL @@@@ "+host+"\n")
        #op=open ("outputrevision.txt", "w").write(var_registro)
    print (var_registro)

IS_DEV=False
class DataBaseHandler():

    def re_open_connection(self):
        try:
            if IS_DEV:    
                self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=aprovdev.database.windows.net;UID=ufntsa;PWD=Q%2A8Ycn*Gcse6/%;DATABASE=UfinetProvisioning;')
            else:
                self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=aprov.database.windows.net;UID=ufntsa;PWD=T$2A8Bcn*Gcs36$%;DATABASE=UfinetProvisioning;')
            
            self.cursor = self.conn.cursor()
        except Exception as e:
            logging.exception(e)
            pass

    def get_all_ip_mgt():
        try:  
            if IS_DEV:    
                conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=aprovdev.database.windows.net;UID=ufntsa;PWD=Q%2A8Ycn*Gcse6/%;DATABASE=UfinetProvisioning;')
            else:
                conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=aprov.database.windows.net;UID=ufntsa;PWD=T$2A8Bcn*Gcs36$%;DATABASE=UfinetProvisioning;')
            
            cursor = conn.cursor()
        except Exception as e:
            logging.exception(e)
            pass
        try:
            query = """SELECT *
                        FROM vlan_management_group 
                        """
            if conn.closed:
                open_connection()
            return list(cursor.execute(query))
        except Exception as e:
            logging.exception(e)
            conn.close()
            pass