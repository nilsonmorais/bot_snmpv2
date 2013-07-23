bot_snmpv2
========


Python bot for snmpv2.

It queries a SNMP server v2 and writes the result in a rrd file. For better use, put this script in cron to constants updates in rrd file.

Features
--------
- Simple bot to get snmp values.
- Very lightweight.

Usage
-----

    $ ./bot_snmpv2.py host=<host> port=<port> oid=<oid> community=<community> rrd_file=<rrd_file>

Example
-------

    $ ./bot_snmpv2.py host=localhost port=161 oid=1.3.6.1.4.1.2620.1.6.7.2.4.0 community=public rrd_file=rrd.rrd

About
----

Nilson Morais - @nilsonmorais

Distributed under the MIT license. See ``LICENSE.txt`` for more information.

https://github.com/nilsonmorais/bot_snmpv2
