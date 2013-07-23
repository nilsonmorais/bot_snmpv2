#!/usr/bin/python
# -*- coding: utf-8 -*-

#recebe os dados do SNMP e grava num RRD 
#
#bot_snmpv2.py <host> <port> <oid> <community> <rrd_file>


from pysnmp.entity.rfc3413.oneliner import cmdgen
import sys
import rrdtool
import datetime

def oid2tuple(str):
    return tuple(int(v) for v in str.split("."))

def write_rrd(rrd,value):
    try:
        rrdtool.update(rrd, 'N:'+str(value))
        print(datetime.datetime.now().isoformat()+" Update: "+rrd+' N:'+str(value))
    except:
        erro_custom("Problema ao inserir dados no arquivo rrd.")

def create_rrd_realtime(rrd):
    try:
        rrdtool.create(rrd,
            '--step', '2', #Using 2 seconds interval, see http://oss.oetiker.ch/rrdtool/doc/rrdcreate.en.html for help to create your own rrd.
            'DS:tuneis:GAUGE:4:0:U',
            'RRA:AVERAGE:0.5:1:1200',
            'RRA:MIN:0.5:10:1200',
            'RRA:MAX:0.5:10:1200',
            'RRA:AVERAGE:0.5:10:1200',
            'RRA:LAST:0.5:1:10')
        print(datetime.datetime.now().isoformat()+" Created: "+rrd)
    except:
        erro_custom("Problema ao criar o arquivo rrd.")

def main(argv):
    argx = ('host','port','oid','community', 'rrd_file')
    if len(argv) < 4:
        erro(argv[0])
        return 1

    try:
        args = dict([arg.split('=') for arg in argv[1:]])
        for argm in argx:
            if not str(argm) in args:
                erro(argv[0])
                return 1
    except:
        erro(argv[0])
        return 1

    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(str(args['community']), str(args['community'])),
         cmdgen.UdpTransportTarget((str(args['host']), int(args['port']))),
         oid2tuple(str(args['oid'])),
    )

    try:
       with open(args['rrd_file']): pass
    except IOError:
       create_rrd_realtime(args['rrd_file'])

    write_rrd(args['rrd_file'],varBinds[0][1])
    return 0

def erro(arg):
    sys.stderr.write("Usage: %s host=<host> port=<port> oid=<oid> community=<community> key=<key> rrd_file=<rrd_file>\n" % arg)

def erro_custom(msg):
    sys.stderr.write("Erro: %s" % msg)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

