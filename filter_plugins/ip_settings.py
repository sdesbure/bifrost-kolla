import struct
import socket
import ipaddress


def ip2int(ipstr):
    return struct.unpack('!I', socket.inet_aton(ipstr))[0]


def int2ip(n):
    return socket.inet_ntoa(struct.pack('!I', n))


def ipadd(ip, add):
    return int2ip(int(ipaddress.ip_address(ip2int(ip))+add))


def node_ips(pod, netw, shift):
    nodes = {}
    index = 1
    for srv in sorted(pod['nodes']):
        nodes[srv] = {'ip': ipadd(netw, shift + index),
                      'shift': shift + index}
        index += 1
    return nodes


def job2nodes(pod):
    jobs = {'controller': [],
            'compute': [],
            'storage': [],
            'network': []}
    for srv in sorted(pod['nodes']):
        for job in pod['nodes'][srv]:
            jobs[job].append(srv)
    return jobs


class FilterModule(object):
    '''
    Functions linked to node network interfaces
    '''

    def filters(self):
        return {
            'ipadd': ipadd,
            'node_ips': node_ips,
            'job2nodes': job2nodes,
        }
