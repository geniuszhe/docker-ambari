#!/usr/bin/python

import psycopg2
import os
import socket
conn = psycopg2.connect(database="ambari", user="ambari", password="bigdata", host="localhost", port="5432")

print "Opened database successfully"

cur = conn.cursor()

cur.execute("select public_host_name,ipv4 from hosts")
rows = cur.fetchall()
host_file = "/etc/hosts"
data=""
'''
with open(host_file, 'rb') as f:
    data = f.read()
    array = data.split("\n")
    try:
        search_start=array.index("# hosts begin")
        search_end=array.index("# hosts end")
        for i in range(search_start,search_end+1):
            array.pop(search_start)
        data = "\n".join(array)
    except Exception as err:
       print err
'''
with open(host_file,"w") as f:
    f.write(data)
    f.write("127.0.0.1	localhost\n")
    f.write("::1	localhost ip6-localhost ip6-loopback\n")
    f.write("# hosts begin\n")
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    f.write( ip+ " " + hostname +"\n")
    for row in rows:
       f.write(row[1] + " " + row[0] + "\n")
    f.write("# hosts end\n")
conn.close

scp_put = '''
spawn scp %s %s@%s:%s
expect "(yes/no)?" {
send "yes\r"
expect "password:"
send "%s\r"
} "password:" {send "%s\r"}
expect eof
exit'''
for row in rows:
    local_path="/etc/hosts"
    user="root"
    host=row[1]
    remote_path="/etc"
    pwd="bigdata"
    os.system("echo '%s' > scp_put.cmd" % (scp_put % (os.path.expanduser(local_path), user, host, remote_path, pwd, pwd)))
    os.system('expect scp_put.cmd')
    os.system('rm scp_put.cmd')
