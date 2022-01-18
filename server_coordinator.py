from concurrent import futures

import hvac
import os
import time
import datetime
from datetime import timedelta
from google.protobuf.timestamp_pb2 import Timestamp
import grpc
import pymysql
from config import conn
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import ipaddress 
from dateutil import parser
import logging

import tags_pb2_grpc as tags_service
import tags_pb2 as tags_message

import serverAvailability_pb2_grpc as serverAvail_service
import serverAvailability_pb2 as serverAvail_message

import authorize_pb2_grpc as authorize_service
import authorize_pb2 as authorize_message

import serverTopology_pb2_grpc as serverTopology_service
import serverTopology_pb2 as serverTopology_message

import tagsList_pb2_grpc as tagsList_service
import tagsList_pb2 as tagsList_message

import smuTags_pb2_grpc as smuTags_service
import smuTags_pb2 as smuTags_message

import smuTags_path_pb2_grpc as smuTags_path_service
import smuTags_path_pb2 as smuTags_path_message
import smuTags_path_all_pb2 as smuTags_path_message_all
import smuTags_path_all_pb2_grpc as  smuTags_path_service_all

import smuTags_path_query_pb2 as  smuTags_path_query_message
import smuTags_path_query_pb2_grpc as  smuTags_path_query_service

import smuTags_tag_query_pb2 as  smuTags_tag_query_message
import smuTags_tag_query_pb2_grpc as  smuTags_tag_query_service

#!/usr/bin/env python

import sys, time, platform, os, sys, math, hashlib
from datetime import datetime, tzinfo, timedelta
from dateutil import tz
import threading
import signal

from pyad import aduser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("userlog.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logging.basicConfig(filename="systemlog.log", level=logging.ERROR, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")

try:
    import argparse
except:
    print("Cannot load argparse module")
    print("Please install latest python 2.7 or later package")
    sys.exit(1)

if 'gen-py' not in sys.path:
    if not os.path.isdir('gen-py'):
        print("Cannot load gen-py folder")
        print("Please install run build.bat first to create generated files")
        sys.exit(1)
    sys.path.append('gen-py')

import topology
from taggetset import TagGetSetService
from tag import TagServer, DataListener, UnsolTagServer
from topology import TopologyService
from bcl.ttypes import *
from tag.ttypes import *
#from config.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import taglib
import inspect, os

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

updown = False

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

class TagService(tags_service.Tags):

    def queryTags(self, request, context):
        try:
            with conn.cursor() as cursor:

                sql = "SELECT distinct d.id AS device_id, t.id AS tag_id, CONCAT(d.path,t.name) AS tagname FROM catalina_hmi.besqlt_devices d "
                sql = sql + " INNER JOIN catalina_hmi.besqlt_tagdef t ON t.type= d.devicetype WHERE d.deleted_at IS NULL "

                #sql = sql + " AND ( t.name LIKE "'"Devices_YPM_DCDC_N%_Minor_Rev"'")"
                if len(request.searchpatterns) == 1:
                    for sp in request.searchpatterns:
                        sql = sql + " AND ( t.name LIKE " + sp.pattern + " )"
                else:
                    request.searchpatterns[0].pattern
                    sql = sql + " AND ( t.name LIKE " + request.searchpatterns[0].pattern
                    i = 1
                    while i < len(request.searchpatterns):
                        sql = sql + " OR  t.name LIKE " + request.searchpatterns[i].pattern
                        i += 1
                        sql = sql + " )"

                cursor.execute(sql)
                result_set = cursor.fetchall()

                status = ''
                sr = tags_message.StatusRes()
                for row in result_set:
                    rr = tags_message.ReturnRow()
                    rr.device_id = str(row["device_id"])
                    rr.tag_id = str(row["tag_id"])
                    rr.tagname = row["tagname"]
                    sr.returnrows.append(rr)

                    #status = str(row["device_id"]) + " " + status
                #print(str(sr))
                #status = ""
                #for row in request.searchpatterns:
                #    status = status + str(row)
                #length = cursor.rowcount
                # if (length == 1):
                #    r = str(result_set[0])
                #result = tags_message.StatusRes(status=str(sql))
                result = tags_message.StatusRes(returnrows=sr.returnrows)
        except Exception as e:
            result = tags_message.StatusRes(status=str(e)+"a")
            #result = tags_message.StatusRes(status='a')

        return result


class ServerAvailService(serverAvail_service.serverAvail):
    def serverAvailability(self, request, context):
        try:
            # Option for the number of packets as a function of
            param = '-n' if platform.system().lower()=='windows' else '-c'

            # Building the command. Ex: "ping -c 1 google.com"
            print(request.hostname)
            command = ['ping', param, '1', request.hostname]
            if (subprocess.call(command) == 0):
                updown = True
            else:
                updown = False
            print("Server is up?")
            print(updown)
            result = serverAvail_message.AvailabilityResponse(up = updown, serverid=100975)

            f = open("gRPClog.txt", "a")
            f.write("User "+ 'kp2001' + " called ServerAvailService function (" + request.hostname + ")@" + str(datetime.datetime.now())+"\n")
            f.close()

        except Exception as e:
            result = str(e)
            f = open("gRPClog.txt", "a")
            f.write("User "+ 'kp2001' + " called ServerAvailService function (" + request.hostname + ")@" + str(datetime.datetime.now())+str(e)+"\n")
            f.close()

        return result 


class Authorization(authorize_service.authorizeService):
    def authorizeClient(self, request, context):
        try:
            ar = authorize_message.AuthorizeResponse()
            ar.clientid = "client12345orHashid"
            ar.serverid = "server179"
            result = ar


            f = open("gRPClog.txt", "a")
            f.write("User "+ 'kp2001' + " called Authorization function @" + str(datetime.datetime.now())+"\n")
            f.close()

        except Exception as e:
            result = str(e)
            f = open("gRPClog.txt", "a")
            f.write("User "+ 'kp2001' + " called Authorization function @" + str(datetime.datetime.now())+str(e)+"\n")
            f.close()
        return result 


class ServerTopologyService(serverTopology_service.topologyService):
    def serverTopology(self, request, context):
        try:
            trs = serverTopology_message.topologyResponse()
            tr =  serverTopology_message.Node()
            tr.nodename = "TST9801"
            tr.devicetype = "PWM"
            tr.deviceid = "1"
            tr.tagname = "TST9801/PWM/1/MC_Watchdog"
            trs.topologyrows.append(tr)
            tr.nodename = "TST9801"
            tr.devicetype = "PWM"
            tr.deviceid = "2"
            tr.tagname = "TST9801/PWM/2/MC_Watchdog"
            trs.topologyrows.append(tr)
            tr.nodename = "TST9801"
            tr.devicetype = "PWM"
            tr.deviceid = "3"
            tr.tagname = "TST9801/PWM/3/MC_Watchdog"
            trs.topologyrows.append(tr)
            tr.nodename = "TST9802"
            tr.devicetype = "PWM"
            tr.deviceid = "1"
            tr.tagname = "TST9802/PWM/1/MC_Watchdog"
            trs.topologyrows.append(tr)
            tr.nodename = "TST9802"
            tr.devicetype = "PWM"
            tr.deviceid = "2"
            tr.tagname = "TST9802/PWM/2/MC_Watchdog"
            trs.topologyrows.append(tr)
            tr.nodename = "TST9802"
            tr.devicetype = "PWM"
            tr.deviceid = "3"
            tr.tagname = "TST9802/PWM/3/MC_Watchdog"
            trs.topologyrows.append(tr)
            result = trs
            print("Topology Created")

            f = open("gRPClog.txt", "a")
            f.write("User "+ 'kp2001' + " called ServerTopologyService function @" + str(datetime.datetime.now())+"\n")
            f.close()

        except Exception as e:
            result = str(e)
            f = open("gRPClog.txt", "a")
            f.write("User "+ 'kp2001' + " called ServerTopologyService function @" + str(datetime.datetime.now())+str(e)+"\n")
            f.close()
        return result 
        

class CreateTagListService(tagsList_service.tagsListservice):
    def createTagslist(self, request, context):
        try:
            ctr = tagsList_message.createTagsResponse()
            tr =  tagsList_message.Node()
            tr.tagname = "TST9801/PWM/1/MC_Watchdog"
            tr.tagid = "61757"
            tr.tagtimestamp = "2021-08-25 15:20:17-08:00"
            tr.status = "S_TAG_GOOD"
            ctr.tagslist.append(tr)

            tr.tagname = "TST9801/PWM/2/MC_Watchdog"
            tr.tagid = "61690"
            tr.tagtimestamp = "2021-08-25 15:20:17-08:00"
            tr.status = "S_TAG_GOOD"
            ctr.tagslist.append(tr)

            tr.tagname = "TST9801/PWM/3/MC_Watchdog"
            tr.tagid = "61734"
            tr.tagtimestamp = "2021-08-25 15:20:17-08:00"
            tr.status = "E_TAG_DEVICEFAIL"
            ctr.tagslist.append(tr)
       
            tr.tagname = "TST9802/PWM/1/MC_Watchdog"
            tr.tagid = "25079"
            tr.tagtimestamp = "2021-08-25 15:20:17-08:00"
            tr.status = "S_TAG_GOOD"
            ctr.tagslist.append(tr)

            tr.tagname = "TST9802/PWM/2/MC_Watchdog"
            tr.tagid = "25044"
            tr.tagtimestamp = "2021-08-25 15:20:17-08:00"
            tr.status = "S_TAG_GOOD"
            ctr.tagslist.append(tr)

            tr.tagname = "TST9802/PWM/3/MC_Watchdog"
            tr.tagid = "25100"
            tr.tagtimestamp = "2021-08-25 15:20:17-08:00"
            tr.status = "E_TAG_DEVICEFAIL"
            ctr.tagslist.append(tr)

            result = ctr
            print("Tags List Created")

            f = open("gRPClog.txt", "a")
            f.write("User "+ 'kp2001' + " called CreateTagListService function @" + str(datetime.datetime.now())+"\n")
            f.close()


        except Exception as e:
            result = str(e)
            f = open("gRPClog.txt", "a")
            f.write("User "+ 'kp2001' + " called CreateTagListService function @" + str(datetime.datetime.now())+str(e)+"\n")
            f.close()
        return result 


  
# Processor which stores state information on thread 
class ThreadContextProcessor(Thrift.TProcessor):
  """Wrapper class for processor to expose underlying transport"""
  __tls = threading.local()

  def __init__(self, proc):
    self.__proc = proc
    
  def process(self, iprot, oprot):
    try:
      # save iprot and prot on tls for later retrieval
      ThreadContextProcessor.__tls.iprot = iprot
      ThreadContextProcessor.__tls.oprot = oprot
      self.__proc.process(iprot, oprot)			
    finally:
      # reset tls variables
      ThreadContextProcessor.__tls.iprot = None
      ThreadContextProcessor.__tls.oprot = None
      
  def getInputProcessor():
    return ThreadContextProcessor.__tls.iprot
    
  def getOutputProcessor():
    return ThreadContextProcessor.__tls.iprot

# Framed transport which exposes underlying transport
class TagFramedTransport(TTransport.TFramedTransport, TTransport.CReadableTransport):

  class Factory:
    """Factory transport that builds buffered transports"""
    def getTransport(self, trans):
      buffered = TagFramedTransport(trans)
      return buffered

  def __init__(self, trans,):
    TTransport.TFramedTransport.__init__(self, trans)
    
  def getUnderlyingTransport(self):
    return self.__trans

class smuTagsClass(smuTags_service.smuTags_Service):

    def smuTags_rpc(self, request, context):
        rt = smuTags_message.smuTagsResponse()

        def NormalizePath( value ):
            return value.replace(".","_") if value else None 

        filehash = "0123456789ABCDEF"
        def generateHashString():
            return filehash

        def generateAuthRequest():
            authreq = AuthorizeRequest()
            authreq.clientTime = taglib.getDateTimeNow()
            authreq.hostname = str(platform.node())
            authreq.username = os.environ.get('USERNAME', 'nobody')
            authreq.clientkey = generateHashString()
            return authreq

        def generateAuthResponse(id):
            authresp = AuthorizeResponse()
            authresp.clientid = id
            authresp.serverid = id
            return authresp

        def generateConfigRequest():
            confreq = topology.ttypes.ConfigRequest()
            confreq.clientid = 1
            confreq.clientTime = taglib.getDateTimeNow()
            return confreq

        def getTopology(server='localhost', port=topology.ttypes.DefaultServicePorts.BINARY_TOPOLOGY_SERVICE):
            transport = None
            try:
                # Make Framed Socket using Binary Protocol to talk to TagServer
                transport = TSocket.TSocket(server, port)
                transport = TagFramedTransport(transport)
                protocol = TBinaryProtocol.TBinaryProtocol(transport)
                client = TopologyService.Client(protocol)
                transport.open()
                
                confreq = generateConfigRequest()
                confresp = client.GetTopologyConfig(confreq)	
               
                transport.close()
                return confresp.topology
            except Thrift.TException as tx:
                print(('%s' % (tx.message)))
            except Exception as ex:
                print(('%s' % (ex.message)))
            finally:
                if transport: transport.close()
            return None

        def simpleClientTest(server_name, device_type, taglist):
            transport = None
            
            try: 
                timestamp = Timestamp()
                timestamp.GetCurrentTime()
                print(str(timestamp))
                #print(str(gt.Timestamp.GetCurrentTime))
            except:
                print("error")

            try:
                rtt = smuTags_message.returnTag()
                try:
                    topology = getTopology(server_name)
                except:
                    print("No server found.")
                    rtt.tagname =""
                    rt.result.append(rtt)
                    return
                
                if not topology: return
            
                tagnames = []
                for node in topology.NetworkNodes:
                    nodename = NormalizePath(node.Name)
                    #print(nodename)
                    #print(node.NetworkDevices)
                    for device in node.NetworkDevices:
                        #print(device.Type)
                        if device.Type == device_type:
                            #print(device_type)
                            #print(str(device.ID))
                            #tagnames.extend( "%s/%s/%s/%s"%(nodename, device.Type, str(device.ID), name) for name in taglist )
                            #tagnames.extend( "%s/%s/%s/%s"%(nodename, device.Type, str(device.ID), taglist) )
                            tagstring = ("%s/%s/%s/%s"%(nodename, device.Type, str(device.ID), taglist))
                            tagnames.append(tagstring)
                if not tagnames:
                    print("No devices found.")
                    rtt.tagname ="No devices found."
                    rt.result.append(rtt)
                    return
                
                #print("tagnames")
                #print(tagnames)
                #return

                # Make Framed Socket using Binary Protocol to talk to TagServer
                transport = TSocket.TSocket(server_name, DefaultServicePorts.BINARY_TAG_SERVICE)
                transport = TagFramedTransport(transport)
                protocol = TBinaryProtocol.TBinaryProtocol(transport)
                client = UnsolTagServer.Client(protocol)
                transport.open()
                
                authreq = generateAuthRequest()

                #print(authreq)

                authresp = client.Authorize(authreq)
                clientid = authresp.clientid # client authorization id
                defaultTimeout = taglib.convertToTimeSpan(timedelta(seconds=15))

                readreq = ReadTagRequest()
                readreq.clientid = clientid
                readreq.reqtime = taglib.getDateTimeNow()
                readreq.timeout = defaultTimeout
                readreq.waitForSuccess = True
                readreq.tag = taglib.buildSimpleTagList( tagnames )
                
                #print("readreq.tag")
                #print(readreq.reqtime)
                #print(readreq.tag)
                #return
                
                readresp = client.ReadTags(readreq, defaultTimeout)
                
                #print(readresp)

                try: 
                    for tag in readresp.tag:
                        #print(str(tag.value))
                        
                        rtt.tagname = tag.name
                        rtt.value = str(taglib.convertFromVariant(tag.value))
                        #rtt.datetime =taglib.convertFromDateTimeToLocal(tag.tstamp)
                        #rtt.datetime =  int(tag.tstamp.value)
                        #print(taglib.ticks_to_utc(tag.tstamp.value))
                        rtt.datetime = str(taglib.ticks_to_utc(tag.tstamp.value))
                        
                        rtt.ticks = tag.tstamp.value
                        #rtt.datetime = taglib.ticks_to_utc(tag.tstamp.value)
                        #print(taglib.convertFromDateTimeToLocal(tag.tstamp))

                        rtt.status = taglib.getTagStatusString(tag.status)

                        #rtt.rt = "%-45s %-15s %s   %s"%( 
                        #    tag.name, 
                        #    str(taglib.convertFromVariant(tag.value)), 
                        #    taglib.convertFromDateTimeToLocal(tag.tstamp), 
                        #    taglib.getTagStatusString(tag.status) 
                        #)
                        rt.result.append(rtt)

                        #res.append("%-45s %-15s %s   %s"%( 
                        #    tag.name, 
                        #    str(taglib.convertFromVariant(tag.value)), 
                        #    taglib.convertFromDateTimeToLocal(tag.tstamp), 
                        #   taglib.getTagStatusString(tag.status) 
                        #))

                        #print(("%-45s %-15s %s   %s"%( 
                        #    tag.name, 
                        #    str(taglib.convertFromVariant(tag.value)), 
                        #    taglib.convertFromDateTimeToLocal(tag.tstamp), 
                        #    taglib.getTagStatusString(tag.status) 
                        #)))
                except:
                    print("No tags found.")
                    rtt.tagname="No tags found."
                    rt.result.append(rtt)
                #print(str(len(res)))
                #print(res)
                #print("#2")
                #print(res[2])
                #rt = str(res[2])
            except Thrift.TException as tx:
                # print(('%s' % (tx.message)))
                rtt.tagname=""
                rt.result.append(rtt)
            finally:
                if transport: transport.close()


        simpleClientTest(request.hostname,request.devicetype, request.taglist)	

        return rt  

class smuTagsClass_path(smuTags_path_service.smuTags_path_Service):

    def smuTags_path_rpc(self, request, context):
        rt = smuTags_path_message.smuTagsResponse()

        def NormalizePath( value ):
            return value.replace(".","_") if value else None 

        filehash = "0123456789ABCDEF"
        def generateHashString():
            return filehash

        def generateAuthRequest():
            authreq = AuthorizeRequest()
            authreq.clientTime = taglib.getDateTimeNow()
            authreq.hostname = str(platform.node())
            authreq.username = os.environ.get('USERNAME', 'nobody')
            authreq.clientkey = generateHashString()
            return authreq

        def generateAuthResponse(id):
            authresp = AuthorizeResponse()
            authresp.clientid = id
            authresp.serverid = id
            return authresp

        def generateConfigRequest():
            confreq = topology.ttypes.ConfigRequest()
            confreq.clientid = 1
            confreq.clientTime = taglib.getDateTimeNow()
            return confreq

        def getTopology(server='localhost', port=topology.ttypes.DefaultServicePorts.BINARY_TOPOLOGY_SERVICE):
            transport = None
            try:
                # Make Framed Socket using Binary Protocol to talk to TagServer
                transport = TSocket.TSocket(server, port)
                transport = TagFramedTransport(transport)
                protocol = TBinaryProtocol.TBinaryProtocol(transport)
                client = TopologyService.Client(protocol)
                transport.open()
                
                confreq = generateConfigRequest()
                confresp = client.GetTopologyConfig(confreq)	
               
                transport.close()
                return confresp.topology
            except Thrift.TException as tx:
                print(('%s' % (tx.message)))
            except Exception as ex:
                print(('%s' % (ex.message)))
            finally:
                if transport: transport.close()
            return None

        def grabTags(ipaddress,server_name, device_type, taglist,sector,groupby):
            transport = None
            try:
                stcomputer = smuTags_path_message.smuTags_computer()
                try: 
                    if groupby.upper() != 'ALL':
                        stcomputer.computername = server_name
                        #stcomputer.ipaddress = ipaddress
                        stcomputer.devicetype = device_type
                    else:
                        print(groupby)
                except:
                    print("Parameter Error")

                try:
                    topology = getTopology(ipaddress)
                except:
                    print("No server found.")
                    #rtt.tagname =""
                    #rt.result.append(rtt)
                    return
                if not topology: return
            
                tagnames = []
                for node in topology.NetworkNodes:
                    nodename = NormalizePath(node.Name)
                    for device in node.NetworkDevices:

                        if (device.Type == device_type and str(device.ID) == str(sector)):
                            tagstring = ("%s/%s/%s/%s"%(nodename, device.Type, str(device.ID), taglist))
                            print(tagstring)
                            tagnames.append(tagstring)
                                           
                        if device.Type == device_type and str(sector) == '-1':
                            tagstring = ("%s/%s/%s/%s"%(nodename, device.Type, str(device.ID), taglist))
                            print(tagstring)
                            tagnames.append(tagstring)

                if not tagnames:
                    print("No devices found.")
                    #rtt.tagname ="No devices found."
                    #rt.result.append(rtt)
                    rt.smuTags_computers.append(stcomputer)
                    return

                transport = TSocket.TSocket(ipaddress, DefaultServicePorts.BINARY_TAG_SERVICE)
                transport = TagFramedTransport(transport)
                protocol = TBinaryProtocol.TBinaryProtocol(transport)
                client = UnsolTagServer.Client(protocol)
                transport.open()                
                authreq = generateAuthRequest()

                authresp = client.Authorize(authreq)
                clientid = authresp.clientid # client authorization id
                defaultTimeout = taglib.convertToTimeSpan(timedelta(seconds=15))

                readreq = ReadTagRequest()
                readreq.clientid = clientid
                readreq.reqtime = taglib.getDateTimeNow()
                readreq.timeout = defaultTimeout
                readreq.waitForSuccess = True
                readreq.tag = taglib.buildSimpleTagList( tagnames )

                readresp = client.ReadTags(readreq, defaultTimeout)

                try: 
                    rtt = smuTags_path_message.returnTag()
                    for tag in readresp.tag:
                        rtt.tagname = tag.name
                        rtt.value = str(taglib.convertFromVariant(tag.value))
                        rtt.datetime = str(taglib.ticks_to_utc(tag.tstamp.value))
                        #rtt.ticks = tag.tstamp.value
                        rtt.status = taglib.getTagStatusString(tag.status)
                        stcomputer.result.append(rtt)

                except:
                    print("No tags found.")
                    rtt.tagname="No tags found."
                    stcomputer.result.append(rtt)

            except Thrift.TException as tx:
                print(('%s' % str(tx)))
                #rtt.tagname=""
                #rt.result.append(rtt)
            finally:
                if transport: transport.close()
            rt.smuTags_computers.append(stcomputer)

        def createErrormessage(server_name,device_type):
            stcomputer = smuTags_path_message.smuTags_computer()
            stcomputer.computername = server_name                    
            stcomputer.devicetype = device_type
            rtt = smuTags_path_message.returnTag()
            rtt.tagname = "Intake path format is wrong"
            stcomputer.result.append(rtt)
            rt.smuTags_computers.append(stcomputer)

        def queryIP(computername):
            ipaddress = '0.0.0.0'
            computernm = 'pending'
            ip_computer = []
            try:
                with conn.cursor() as cursor:
                    
                    sql = "SELECT DISTINCT a.computerName, b.ipaddress from besqlt_devices a LEFT JOIN besqlt_computers b "
                    sql = sql + " ON a.computerName = b.hostname WHERE substring(a.computerName,1,6) ='"+computername+"'"

                    #print(sql)
                    try:
                        cursor.execute(sql)
                        result_set = cursor.fetchall()
                    except Exception as e:
                        print(str(e))

                    for row in result_set:
                        ipaddress = str(row["ipaddress"])
                        computernm = str(row["computerName"])
                        ip_computer.append(ipaddress)
                        ip_computer.append(computernm)
                    return ip_computer
            except Exception as e:
                return ipaddress

        def smuTags_path(groupby, paths):
            try:
                print(paths)       
                for path in paths:
                    print("segments:")
                    print(len(path.split('/')))
                    if len(path.split('/')) == 4:
                        computer = path.split('/')[0][0:6]
                        device = path.split('/')[1]
                        sector = path.split('/')[2]
                        tagpattern = path.split('/')[3]
                        try:
                            ipaddress = queryIP(computer)[0]
                            computernm = queryIP(computer)[1]

                            print(ipaddress)
                            print(computernm)
                            print(device)
                            print(sector)
                            print(tagpattern)
                        except:
                            print("No IP found")
                        grabTags(ipaddress,computernm,device, tagpattern,sector,groupby)	

                    else:
                        computer = path.split('/')[0]
                        device = path.split('/')[1]
                        createErrormessage(computer,device)
   
            except Exception as e:

                 print(str(e))
            #print(rt)

        #simpleClientTest(request.hostname,request.devicetype, request.taglist)	

        smuTags_path(request.groupby,request.paths)

        return rt  

class smuTagsClass_path_all(smuTags_path_service_all.smuTags_path_Service):

    def smuTags_path_rpc(self, request, context):
        rt_all = smuTags_path_message_all.smuTagsResponse()

        def NormalizePath( value ):
            return value.replace(".","_") if value else None 

        filehash = "0123456789ABCDEF"
        def generateHashString():
            return filehash

        def generateAuthRequest():
            authreq = AuthorizeRequest()
            authreq.clientTime = taglib.getDateTimeNow()
            authreq.hostname = str(platform.node())
            authreq.username = os.environ.get('USERNAME', 'nobody')
            authreq.clientkey = generateHashString()
            return authreq

        def generateAuthResponse(id):
            authresp = AuthorizeResponse()
            authresp.clientid = id
            authresp.serverid = id
            return authresp

        def generateConfigRequest():
            confreq = topology.ttypes.ConfigRequest()
            confreq.clientid = 1
            confreq.clientTime = taglib.getDateTimeNow()
            return confreq

        def getTopology(server='localhost', port=topology.ttypes.DefaultServicePorts.BINARY_TOPOLOGY_SERVICE):
            transport = None
            try:
                # Make Framed Socket using Binary Protocol to talk to TagServer
                transport = TSocket.TSocket(server, port)
                transport = TagFramedTransport(transport)
                protocol = TBinaryProtocol.TBinaryProtocol(transport)
                client = TopologyService.Client(protocol)
                transport.open()
                
                confreq = generateConfigRequest()
                confresp = client.GetTopologyConfig(confreq)	
               
                transport.close()
                return confresp.topology
            except Thrift.TException as tx:
                print(('%s' % (tx.message)))
            except Exception as ex:
                print(('%s' % (ex.message)))
            finally:
                if transport: transport.close()
            return None

        def tagGetSetService(server='localhost', port=topology.ttypes.DefaultServicePorts.BINARY_TOPOLOGY_SERVICE):
            transport = None
            try:
                # Make Framed Socket using Binary Protocol to talk to TagServer
                transport = TSocket.TSocket(server, port)
                transport = TagFramedTransport(transport)
                protocol = TBinaryProtocol.TBinaryProtocol(transport)
                client = TagGetSetService.Client(protocol)
                transport.open()
                
                confreq = generateConfigRequest()
                print("confreq")
                print(confreq)
                confresp = client.FetchTags(confreq)	
               
                transport.close()
                print("confresp")
                print(confresp)
                #return confresp.topology
            except Thrift.TException as tx:
                print(('%s' % (tx.message)))
            except Exception as ex:
                print(('%s' % (ex.message)))
            finally:
                if transport: transport.close()
            return None


        def grabTags(ipaddress,server_name, device_type, taglist,sector,path):
            transport = None
            #print("taglist")
            #print(taglist)
            try:
                stp_all_rt = smuTags_path_message_all.returnTag()

                try:
                    topology = getTopology(ipaddress)
                except:
                    #rint("No server found.")
                    #rtt.tagname =""
                    #rt.result.append(rtt)
                    logger.info("User "+ 'kp20010503' + " called Tag service (" +server_name +")")
                    logger.info("E_SERVERDOWN: No server found")
                    return
                if not topology: 
                    logger.info("User "+ 'kp20010503' + " called Tag service (" +server_name +")")
                    logger.info('E_SERVERDOWN')

                    stp_all_rt.tagname = path
                    stp_all_rt.status ="E_SERVERDOWN"
                    rt_all.smuTags_all.append(stp_all_rt)
                    return
            
                tagnames = []
                for node in topology.NetworkNodes:
                    nodename = NormalizePath(node.Name)
                    for device in node.NetworkDevices:
                        
                        #if (device.Type == device_type and str(device.ID) == str(sector)):
                        #per deviceid and tag; only return the current server.
                        if (device.Type == device_type and nodename == server_name and str(device.ID) == str(sector)):
                            tagstring = ("%s/%s/%s/%s"%(nodename, device.Type, str(device.ID), taglist))
                            #print("tagstring")
                            #print(tagstring)
                            tagnames.append(tagstring)
                                           
                        if device.Type == device_type and str(sector) == '-1':
                            tagstring = ("%s/%s/%s/%s"%(nodename, device.Type, str(device.ID), taglist))
                            #print("tagstring")
                            #print(tagstring)
                            tagnames.append(tagstring)

                if not tagnames:
                    logger.info("User "+ 'kp20010503' + " called Tag service (" +server_name +")")
                    logger.info('E_TAG_CONFIGERROR: No devices found')

                    stp_all_rt.tagname = path
                    stp_all_rt.status ="E_TAG_CONFIGERROR"
                    rt_all.smuTags_all.append(stp_all_rt)
                    return

                transport = TSocket.TSocket(ipaddress, DefaultServicePorts.BINARY_TAG_SERVICE)
                transport = TagFramedTransport(transport)
                protocol = TBinaryProtocol.TBinaryProtocol(transport)
                client = UnsolTagServer.Client(protocol)
                transport.open()                
                authreq = generateAuthRequest()

                authresp = client.Authorize(authreq)
                clientid = authresp.clientid # client authorization id
                defaultTimeout = taglib.convertToTimeSpan(timedelta(seconds=15))

                readreq = ReadTagRequest()
                readreq.clientid = clientid
                readreq.reqtime = taglib.getDateTimeNow()
                readreq.timeout = defaultTimeout
                readreq.waitForSuccess = True
                readreq.tag = taglib.buildSimpleTagList( tagnames )

                readresp = client.ReadTags(readreq, defaultTimeout)

                try: 
                    #rtt = smuTags_path_message_all.returnTag()
                    for tag in readresp.tag:
                        stp_all_rt.tagname = tag.name
                        stp_all_rt.value = str(taglib.convertFromVariant(tag.value))
                        stp_all_rt.datetime = str(taglib.ticks_to_utc(tag.tstamp.value))
                        #rtt.ticks = tag.tstamp.value
                        stp_all_rt.status = taglib.getTagStatusString(tag.status)

                        rt_all.smuTags_all.append(stp_all_rt)
                except Exception as e:
                    logging.error("User "+ 'kp20010503' + " called Tag service (" +server_name +")")
                    logging.error('E_TAG_CONFIGERROR: No tags found.')
                    logging.error(str(e))


                    stp_all_rt.tagname = path
                    stp_all_rt.status="E_TAG_CONFIGERROR"

            except Thrift.TException as tx:
                logging.error(str(tx))
                #rtt.tagname=""
                #rt.result.append(rtt)
            finally:
                if transport: transport.close()

            #rt_all.smuTags_all.append(stp_all_rt)

        def grabTags_get(ipaddress,server_name, device_type, taglist,sector):
            transport = None
            try:
                stp_all_rt = smuTags_path_message_all.returnTag()

                try:
                    topology = tagGetSetService(ipaddress)
                except:
                    print("No server found.")
                    #rtt.tagname =""
                    #rt.result.append(rtt)
                    return
                if not topology: 
                    print("No Topology")
                    stp_all_rt.status ="E_SERVERDOWN: Computer " + server_name +": Server is down."
                    rt_all.smuTags_all.append(stp_all_rt)
                    return
            
                tagnames = []
                for node in topology.NetworkNodes:
                    nodename = NormalizePath(node.Name)
                    for device in node.NetworkDevices:

                        if (device.Type == device_type and str(device.ID) == str(sector)):
                            tagstring = ("%s/%s/%s/%s"%(nodename, device.Type, str(device.ID), taglist))
                            print(tagstring)
                            tagnames.append(tagstring)
                                           
                        if device.Type == device_type and str(sector) == '-1':
                            tagstring = ("%s/%s/%s/%s"%(nodename, device.Type, str(device.ID), taglist))
                            print(tagstring)
                            tagnames.append(tagstring)

                if not tagnames:
                    print("No devices found.")
                    stp_all_rt.status ="E_TAG_CONFIGERROR: Computer " + server_name +": No devices found."
                    rt_all.smuTags_all.append(stp_all_rt)
                    return

                transport = TSocket.TSocket(ipaddress, DefaultServicePorts.BINARY_TAG_SERVICE)
                transport = TagFramedTransport(transport)
                protocol = TBinaryProtocol.TBinaryProtocol(transport)
                client = TagGetSetService.Client(protocol)
 
                #client = UnsolTagServer.Client(protocol)
                transport.open()                
                authreq = generateAuthRequest()

                authresp = client.Authorize(authreq)
                clientid = authresp.clientid # client authorization id
                defaultTimeout = taglib.convertToTimeSpan(timedelta(seconds=15))

                readreq = ReadTagRequest()
                readreq.clientid = clientid
                readreq.reqtime = taglib.getDateTimeNow()
                readreq.timeout = defaultTimeout
                readreq.waitForSuccess = True
                readreq.tag = taglib.buildSimpleTagList( tagnames )

                readresp = client.ReadTags(readreq, defaultTimeout)
                print("readresp")
                print(readresp)

                try: 
                    #rtt = smuTags_path_message_all.returnTag()
                    for tag in readresp.tag:
                        stp_all_rt.tagname = tag.name
                        stp_all_rt.value = str(taglib.convertFromVariant(tag.value))
                        stp_all_rt.datetime = str(taglib.ticks_to_utc(tag.tstamp.value))
                        #rtt.ticks = tag.tstamp.value
                        stp_all_rt.status = taglib.getTagStatusString(tag.status)

                        rt_all.smuTags_all.append(stp_all_rt)
                except Exception as e:
                    print("No tags found. " + str(e))
                    stp_all_rt.status="E_TAG_CONFIGERROR: Computer " + server_name +": No tags found."

            except Thrift.TException as tx:
                print(('%s' % str(tx) + '!!!'))
                #rtt.tagname=""
                #rt.result.append(rtt)
            finally:
                if transport: transport.close()

            #rt_all.smuTags_all.append(stp_all_rt)


        def createErrormessage_all(server_name,device_type,position,path):
            rtt = smuTags_path_message_all.returnTag()
            rtt.tagname = path
            rtt.status = "E_TAG_CONFIGERROR"     
            rt_all.smuTags_all.append(rtt)      

        def createErrormessage_pathtag(server_name,device_type,position,path):
            rtt = smuTags_path_message_all.returnTag()
            rtt.tagname = path
            rtt.status = "E_TAG_CONFIGERROR"     
            rt_all.smuTags_all.append(rtt)     

        def queryIP(computername):
            ipaddress = '0.0.0.0'
            computernm = 'pending'
            ip_computer = []
            try:
                with conn.cursor() as cursor:
                    
                    sql = "SELECT DISTINCT a.computerName, b.ipaddress from besqlt_devices a LEFT JOIN besqlt_computers b "
                    sql = sql + " ON a.computerName = b.hostname WHERE substring(a.computerName,1,6) ='"+computername+"'"

                    #print(sql)
                    try:
                        cursor.execute(sql)
                        result_set = cursor.fetchall()
                    except Exception as e:
                        print(str(e))

                    for row in result_set:
                        ipaddress = str(row["ipaddress"])
                        computernm = str(row["computerName"])
                        ip_computer.append(ipaddress)
                        ip_computer.append(computernm)
                    return ip_computer
            except Exception as e:
                return ipaddress

        def queryPatterns(computer_,device_,sector_,tagpattern_):
            ipaddress = '0.0.0.0'
            computernm = 'pending'
            returnlist = []
            try:
                with conn.cursor() as cursor:
                    
                    sql = "SELECT DISTINCT d.computerName,b.ipaddress, d.deviceType, d.id AS device_id, t.id AS tag_id, CONCAT(d.path,t.name) AS tagname, "
                    sql = sql + "d.path,t.name, "
                    sql = sql + "REPLACE(SUBSTRING(SUBSTRING_INDEX(d.path, '/', 3), "
                    sql = sql + "    LENGTH(SUBSTRING_INDEX(d.path, '/', 3 -1)) + 1), "
                    sql = sql + "    '/', '') AS sector "
                    sql = sql + "FROM catalina_hmi.besqlt_devices d "
                    sql = sql + "INNER JOIN catalina_hmi.besqlt_tagdef t ON t.type= d.devicetype "
                    sql = sql + "LEFT JOIN besqlt_computers b "
                    sql = sql + "ON d.computerName = b.hostname "
                    sql = sql + "WHERE d.deleted_at IS NULL AND ( t.name LIKE '%mc%') "
                    sql = sql + " AND d.computerName like 'TST096%' "
                    sql = sql + " AND d.deviceType LIKE '%YPM%' "
                    #print(sql)
                    try:
                        #print("Inside query")
                        #print(computer_)
                        #print(device_)
                        #print(sector_)
                        #print(tagpattern_)

                        cursor.execute(sql)
                        result_set = cursor.fetchall()
                    except Exception as e:
                        print(str(e))

                    for row in result_set:
                        ipaddress = str(row["ipaddress"])
                        print("ipaddress" + ipaddress)
                        computernm = str(row["computerName"])
                        print("computernm " + computernm)
                        deviceType = row["deviceType"]
                        print("deviceType "+ deviceType)
                        tagname = row["name"]
                        print("tagname " + tagname)
                        sector = row["sector"]
                        print("sector " + sector)
                        ip_computer = []
                        ip_computer.append(ipaddress)
                        ip_computer.append(computernm)
                        ip_computer.append(deviceType)
                        ip_computer.append(tagname)
                        ip_computer.append(sector)
                        returnlist.append(ip_computer)
                    return returnlist
            except Exception as e:
                return returnlist

        def checkQueryLimitation():
            #open log.txt and calculate the query entries in the past hour
            logfile = open('log.txt', 'r')
            Lines = logfile.readlines()
            logfile.close()

            #print(len(Lines))
            x = Lines[len(Lines)-1].split(" ")
            #print(x[2])
            print("Delta")
            deltaseconds = (datetime.now() -parser.parse(x[5])).total_seconds()
            deltaminutes = deltaseconds/60
            hit = False
            if deltaminutes > 90:
                print("Limitation reset")
                return False
            else:
                limitation = int(x[2])
                print(limitation)
                if (limitation > 300000):
                    hit = True
                    print("Limitation hit! Wait for another hour.")
                    return True
                else:
                    i = 0

                    while hit != True and len(Lines)-1+i>0 :    
                        i = i -1
                        x = Lines[len(Lines)-1+i].split(" ")
                        deltaseconds = (datetime.now() -parser.parse(x[5])).total_seconds()
                        deltaminutes = deltaseconds/60
                        if deltaminutes <= 90:
                            limitation = limitation + int(x[2])
                            print(limitation)
                            if (limitation > 300000):
                                hit = True 
                    if hit == True:
                        print("Limitation hit! Wait for another hour..")
                        return True
                    else:
                        print("Limitation doesn't hit")
                        return False

        def checkPathTagMatch(path,tag):
            try:
                with conn.cursor() as cursor:
                    
                    sql = "SELECT d.path,t.name AS tag "
                    sql = sql + "FROM catalina_hmi.besqlt_devices d "
                    sql = sql + "INNER JOIN catalina_hmi.besqlt_tagdef t ON t.type= d.devicetype "
                    sql = sql + "WHERE d.deleted_at IS NULL AND t.name = '"+tag+"' "
                    sql = sql + "AND d.path = '"+ path + "' "

                    #print(sql)
                    try:
                        cursor.execute(sql)
                        result_set = cursor.fetchone()
                    except Exception as e:
                        print(str(e))

                    print(len(result_set))

                    return True
            except Exception as e:
                return False

        def writeLog():
            try:
                f = open("log.txt", "a")
                f.write('kp210503 queried '+str(len(rt_all.smuTags_all))+ ' entries at '  + str(datetime.today().isoformat())+'\n')
                f.close()
            except Exception as e:
                print(str(e))

        def checkUsernameToken(username,token):
            client = hvac.Client(url='https://10.192.63.129:443',verify = False)
            client.token = token
            #print(client.is_authenticated())
            return True
        
        def grabClientkey(username):
            client = hvac.Client(url='https://10.192.63.129:443',verify = False)
            read_response = client.secrets.kv.v1.read_secret('data/users/pd_software/'+username)
            print('Value under path "data/users/pd_software/" / key "clientid": {val}'.format(val=read_response['data']['clientid'],))
            print('Value under path "data/users/pd_software/" / key "token": {val}'.format(val=read_response['data']['token'],))

            return read_response['data']['clientid']

        def grabActions(Clientkey):
            try:
                rem_access = []
                with conn.cursor() as cursor:
                    sql = "SELECT a.clientkey, a.ipaddress,b.authorized_actions,b.filter_type,b.value FROM catalina_hmi.rem_access a JOIN catalina_hmi.rem_access_subset b ON a.id=b.id "
                    sql = sql + "WHERE a.clientkey= '"+Clientkey + "' "

                    try:
                        cursor.execute(sql)
                        result_set = cursor.fetchall()
                    except Exception as e:
                        print(str(e))

                    for row in result_set:
                        try:
                            rem_access.append(row["ipaddress"])
                            rem_access.append(row["authorized_actions"])
                            rem_access.append(row["value"])
                        except Exception as e:
                            print(str(e))

                    return rem_access
            except Exception as e:
                return rem_access
        
        def checkIP():
            return True

        def smuTags_path_all(paths):
            #check query limitation
            if (1 != 1):#checkQueryLimitation():
                rt_error = smuTags_path_message_all.returnTag()
                rt_error.status = "Query limitation hit! Wait for another hour.."
                rt_all.smuTags_all.append(rt_error)
            else:
                try:
                    #print(paths)   

                    position = 0    
                    username = ''
                    token = ''
                    clientkey = ''
                    actions = []
                    for path in paths:
                        #print("segments: " + str(len(path.split('/'))))
                        position = position + 1
                        #print("position:" + str(position))
                        if position == 1: #username
                            username = path
                        if position == 2: #token
                            token = path
                    if checkUsernameToken(username,token):
                        clientkey = grabClientkey(username)
                        actions = grabActions(clientkey)
                    if 'get' in actions[1]:
                        #print(actions[0])
                        print(actions[1])
                        print(actions[2])

                        position = 0
                        for path in paths:
                            position = position + 1
                            if (position >= 3):
                                if len(path.split('/')) == 4:
                                    #computer = path.split('/')[0][0:6]
                                    computer = path.split('/')[0]
                                    device = path.split('/')[1]
                                    sector = path.split('/')[2]
                                    tagpattern = path.split('/')[3]
                                    try:
                                        #ipaddress = queryIP(computer)[0]
                                        #computernm = queryIP(computer)[1]
                                        ipaddress = dict_PathIP[computer+'/'+device+'/'+sector+'/']

                                        #logger.info('ipaddress: {}'.format(ipaddress))
                                        #logger.info('tagpattern: {}'.format(tagpattern))

                                        if (checkPathTagMatch(computer+'/'+device+'/'+sector+'/',tagpattern)):
                                            grabTags(ipaddress,computer,device, tagpattern,sector,path)	
                                        else:
                                            computer = path.split('/')[0]
                                            device = path.split('/')[1]
                                            createErrormessage_pathtag(computer,device,position,path)
                                    except Exception as e:
                                        logger.info("User "+ 'kp20010503' + " called Tag service (" + computer +")")
                                        logger.info('E_TAG_CONFIGERROR: No IP found.')

                                        rt_error = smuTags_path_message_all.returnTag()
                                        rt_error.tagname = path
                                        rt_error.status = "E_TAG_CONFIGERROR"
                                        rt_all.smuTags_all.append(rt_error)

                                else:
                                    computer = path.split('/')[0]
                                    device = path.split('/')[1]
                                    createErrormessage_all(computer,device,position,path)
    
                except Exception as e:
                    logging.error(str(e))
            #print(rt)

        def smuTags_path_all_wildcard_backup(paths):
            try:
                print(paths)   
                position = 0    
                for path in paths:
                    print("segments: " + str(len(path.split('/'))))
                    position = position + 1
                    print("position:" + str(position))
                    
                    if len(path.split('/')) == 4:
                        computer_ = path.split('/')[0][0:6]
                        device_ = path.split('/')[1]
                        sector_ = path.split('/')[2]
                        tagpattern_ = path.split('/')[3]

                        print(computer_)
                        print(device_)
                        print(sector_)
                        print(tagpattern_)

                        try:
                            #print(queryPatterns(computer_,device_,sector_,tagpattern_))
                            for row in queryPatterns(computer_,device_,sector_,tagpattern_):
                                ipaddress = row[0]
                                computernm = row[1]
                                device = row[2]
                                tagpattern = row[3]
                                sector = row[4]

                                #print(ipaddress)
                                #print(computernm)
                                #print(device)
                                #print(sector)
                                #print(tagpattern)

                                grabTags(ipaddress,computernm,device, tagpattern,sector)	
                        except: 
                            print("Computer " + computer_ + ": No IP found")
                            rt_error = smuTags_path_message_all.returnTag()
                            rt_error.tagname = "Computer " + computer_ + ": No IP found"
                            rt_all.smuTags_all.append(rt_error)

                    else:
                        computer = path.split('/')[0]
                        device = path.split('/')[1]
                        createErrormessage_all(computer,device,position)
   
            except Exception as e:

                 print(str(e))
            #print(rt)

        def smuTags_path_all_wildcard(paths):
            try:
                print(paths)   
                position = 0    
                for path in paths:
                    print("segments: " + str(len(path.split('/'))))
                    position = position + 1
                    print("position:" + str(position))
                    
                    if len(path.split('/')) == 3:
                        #computer_ = path.split('/')[0][0:6]
                        device_ = path.split('/')[1]
                        #sector_ = path.split('/')[2]
                        #tagpattern_ = path.split('/')[3]

                        #print(computer_)
                        print(device_)
                        #print(sector_)
                        #print(tagpattern_)

                        try:
                            #print(len(tagMapping_PWM))
                            if (device_ == 'YPM'):
                                for row in tagMapping_YPM:
                                    ipaddress = str(row["ipaddress"])
                                    if (ipaddress != 'None'):
                                        computernm = str(row["computerName"])
                                        device = str(row["deviceType"])
                                        tagpattern = str(row["name"])
                                        sector = str(row["sector"])

                                        print(ipaddress)
                                        print(computernm)
                                        print(device)
                                        print(tagpattern)
                                        print(sector)
                                    #grabTags(ipaddress,computernm,device, tagpattern,sector)	
                                print(len(tagMapping_YPM))    
                            if (device_ == 'PWM'):
                                for row in tagMapping_PWM:
                                    ipaddress = str(row["ipaddress"])
                                    if (ipaddress != 'None'):
                                        computernm = str(row["computerName"])
                                        device = str(row["deviceType"])
                                        tagpattern = str(row["name"])
                                        sector = str(row["sector"])

                                        print(ipaddress)
                                        print(computernm)
                                        print(device)
                                        print(tagpattern)
                                        print(sector)
                                    #grabTags(ipaddress,computernm,device, tagpattern,sector)	    
                                print(len(tagMapping_PWM))     
                        except: 
                            print("Wildcard request has issues")
                            rt_error = smuTags_path_message_all.returnTag()
                            rt_error.tagname = "Wildcard request has issues"
                            rt_all.smuTags_all.append(rt_error)

                    else:
                        computer = path.split('/')[0]
                        device = path.split('/')[1]
                        createErrormessage_all(computer,device,position)
   
            except Exception as e:

                 print(str(e))
            #print(rt)

        #simpleClientTest(request.hostname,request.devicetype, request.taglist)	

        #smuTags_path_all_wildcard(request.paths)
        smuTags_path_all(request.paths)

        #writeLog()

        return rt_all  

class Tags_path_query(smuTags_path_query_service.smuTags_path_query_Service):
    
    def smuTags_path_query_rpc(self, request, context):
        rt_paths = smuTags_path_query_message.smuTagsResponse()

        def smuTags_path_query(path_string):
            try:
                with conn.cursor() as cursor:
                    
                    sql = "SELECT distinct d.path "
                    sql = sql + " FROM catalina_hmi.besqlt_devices d "
                    sql = sql + " WHERE d.deleted_at IS NULL "

                    path_clause = ""
                    #arry_device = device_string.split("/")
                                        
                    #if (len(arry_device) == 1): #has no /
                    #    device_clause = arry_device[0]
                    #else:
                    #    device_clause = arry_device[1]

                    if len(list(find_all(path_string,'*'))) == 0 : #has no *
                        sql = sql + " AND d.path = '"+path_string+"' "
                    else:
                        path_string = path_string.replace("*","%")
                        sql = sql + " AND d.path like '"+path_string+"' "
                    
                    print(sql)
                    try:
                        cursor.execute(sql)
                        result_set = cursor.fetchall()
                    except Exception as e:
                        print(str(e))
                    
                    for row in result_set:
                        try:
                            rt_paths.returnPath.append(row["path"])
                        except Exception as e:
                            print(str(e))

                    return rt_paths

                    if (len(arry_device) > 1): #has computer segment
                        cmptr = arry_device[0]
                        if cmptr == '*':
                            for row in result_set:
                                try:
                                    rt_paths.returnPath.append(row["path"])
                                except Exception as e:
                                    print(str(e))
                        else:
                            for row in result_set:
                                try:
                                    if (cmptr.find("*") == -1 and cmptr.find("?") == -1):
                                        if (row["path"].split('/')[0] == cmptr):
                                            rt_paths.returnPath.append(row["path"])
                                    elif (row["path"].split('/')[0].find(cmptr.replace("*","").replace("?","")) != -1):
                                        rt_paths.returnPath.append(row["path"])
                                except Exception as e:
                                    print(str(e))
                    else: #only device
                        for row in result_set:
                            try:
                                rt_paths.returnPath.append(row["path"])
                            except Exception as e:
                                print(str(e))

                    
            except Exception as e:
                return rt_paths

        smuTags_path_query(request.device_string)

        return rt_paths  

    def smuTags_tag_query_rpc(self, request, context):
        rt_tags = smuTags_tag_query_message.smuTagsResponse()

        def smuTags_tag_query(tag_string):
            try:
                with conn.cursor() as cursor:
                    sql = "SELECT distinct t.name AS tag FROM "
                    sql = sql + "catalina_hmi.besqlt_tagdef t "
                    #sql = sql + "WHERE t.name LIKE '%"+tag_string+"%' "
                    tag_clause = ""
                    arry_tag = tag_string.split("/")
                                        
                    if (len(arry_tag) == 1): #has no /
                        tag_clause = arry_tag[0]
                    else:
                        tag_clause = arry_tag[1]

                    if len(list(find_all(tag_clause,'*'))) == 0: #has no * 
                        sql = sql + "WHERE t.name = '"+tag_clause+"' "
                    else:
                        tag_clause2 = tag_clause.replace("*","%")
                        sql = sql + "WHERE t.name LIKE '"+tag_clause2+"' "
                    
                    print(sql)

                    try:
                        cursor.execute(sql)
                        result_set = cursor.fetchall()
                    except Exception as e:
                        print(str(e))

                    for row in result_set:
                        try:
                            rt_tags.returnTag.append(row["tag"])
                        except Exception as e:
                            print(str(e))

                    return rt_tags
            except Exception as e:
                return rt_tags

        smuTags_tag_query(request.tag_string)

        return rt_tags  


def bringupPatterns_YPM():
            ipaddress = '0.0.0.0'
            computernm = 'pending'
            ip_computer = []
            global tagMapping_YPM
            try:
                with conn.cursor() as cursor:
                    
                    sql = "SELECT DISTINCT d.computerName,b.ipaddress, d.deviceType, d.id AS device_id, t.id AS tag_id, CONCAT(d.path,t.name) AS tagname, "
                    sql = sql + "d.path,t.name, "
                    sql = sql + "REPLACE(SUBSTRING(SUBSTRING_INDEX(d.path, '/', 3), "
                    sql = sql + "LENGTH(SUBSTRING_INDEX(d.path, '/', 3 -1)) + 1), "
                    sql = sql + "'/', '') AS sector "
                    sql = sql + "FROM catalina_hmi.besqlt_devices d "
                    sql = sql + "INNER JOIN catalina_hmi.besqlt_tagdef t ON t.type= d.devicetype "
                    sql = sql + "LEFT JOIN besqlt_computers b "
                    sql = sql + "ON d.computerName = b.hostname "
                    sql = sql + "WHERE d.deleted_at IS NULL AND ( t.name LIKE '%MC_Watchdog%') "
                    sql = sql + "AND d.deviceType LIKE '%YPM%' "

                    #print(sql)
                    try:
                        cursor.execute(sql)
                        tagMapping_YPM = cursor.fetchall()
                        #print(len(tagMapping_PWM))
                    except Exception as e:
                        print(str(e))

            except Exception as e:
                return ipaddress

def bringupPatterns_PWM():
            ipaddress = '0.0.0.0'
            computernm = 'pending'
            ip_computer = []
            global tagMapping_PWM
            try:
                with conn.cursor() as cursor:
                    
                    sql = "SELECT DISTINCT d.computerName,b.ipaddress, d.deviceType, d.id AS device_id, t.id AS tag_id, CONCAT(d.path,t.name) AS tagname, "
                    sql = sql + "d.path,t.name, "
                    sql = sql + "REPLACE(SUBSTRING(SUBSTRING_INDEX(d.path, '/', 3), "
                    sql = sql + "LENGTH(SUBSTRING_INDEX(d.path, '/', 3 -1)) + 1), "
                    sql = sql + "'/', '') AS sector "
                    sql = sql + "FROM catalina_hmi.besqlt_devices d "
                    sql = sql + "INNER JOIN catalina_hmi.besqlt_tagdef t ON t.type= d.devicetype "
                    sql = sql + "LEFT JOIN besqlt_computers b "
                    sql = sql + "ON d.computerName = b.hostname "
                    sql = sql + "WHERE d.deleted_at IS NULL AND ( t.name LIKE '%MC_Watchdog%') "
                    sql = sql + "AND d.deviceType LIKE '%PWM%' "

                    #print(sql)
                    try:
                        cursor.execute(sql)
                        tagMapping_PWM = cursor.fetchall()
                        #print(len(tagMapping_PWM))
                    except Exception as e:
                        print(str(e))

            except Exception as e:
                return ipaddress

def bringupPatterns_PathIP():
            global tagMapping_PathIP
            global dict_PathIP
            #dict_PathIP = {"path":[],"ipaddress":[]}
            dict_PathIP = {}
            try:
                with conn.cursor() as cursor:
                    
                    sql = "SELECT DISTINCT d.path,b.ipaddress "
                    sql = sql + "FROM catalina_hmi.besqlt_devices d "
                    sql = sql + "JOIN besqlt_computers b "
                    sql = sql + "ON d.computerName = b.hostname "
                    sql = sql + "WHERE d.deleted_at IS NULL "

                    #print(sql)
                    try:
                        cursor.execute(sql)
                        tagMapping_PathIP = cursor.fetchall()
                        print(len(tagMapping_PathIP))
                        for row in tagMapping_PathIP:
                            dict_PathIP[row["path"]] = row["ipaddress"]
                    except Exception as e:
                        print(str(e))

            except Exception as e:
                return ipaddress

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    #tags_service.add_TagsServicer_to_server(TagService(), server)
    serverAvail_service.add_serverAvailServicer_to_server(ServerAvailService(), server)
    serverTopology_service.add_topologyServiceServicer_to_server(ServerTopologyService(), server)
    tagsList_service.add_tagsListserviceServicer_to_server(CreateTagListService(), server)
    authorize_service.add_authorizeServiceServicer_to_server(Authorization(),server)

    smuTags_service.add_smuTags_ServiceServicer_to_server(smuTagsClass(),server)
    smuTags_path_service.add_smuTags_path_ServiceServicer_to_server(smuTagsClass_path(),server)
    smuTags_path_service_all.add_smuTags_path_ServiceServicer_to_server(smuTagsClass_path_all(),server)
    smuTags_path_query_service.add_smuTags_path_query_ServiceServicer_to_server(Tags_path_query(),server)
    smuTags_tag_query_service.add_smuTags_tag_query_ServiceServicer_to_server(Tags_path_query(),server)

    server.add_insecure_port('127.0.0.1:50051')
    server.start()
    try:
        print("Server is up.. Computer IP mapping table is being created")
        bringupPatterns_PathIP()
        print("Computer IP mapping table has been created")
        

        #try:
        #    user = aduser.ADUser.from_cn(os.getlogin())
        #    print(user.get_attribute("displayName"))
        # except Exception as e:
        #    print(str(e)+"!!!")

        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print('Server Stop')
        server.stop(0)

if __name__ == '__main__':
    print('Server Start')
    serve()
    conn.close()