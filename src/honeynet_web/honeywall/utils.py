import datetime
import time
import re
from honeywall.models import ARPRecord

PROTOCOLS = {
    0: 'HOPOPT',
    1: 'ICMP',
    2: 'IGMP',
    3: 'GGP',
    4: 'IP',
    5: 'ST',
    6: 'TCP',
    7: 'CBT',
    8: 'EGP',
    9: 'IGP',
    10: 'BBN-RCC-MON',
    11: 'NVP-II',
    12: 'PUP',
    13: 'ARGUS',
    14: 'EMCON',
    15: 'XNET',
    16: 'CHAOS',
    17: 'UDP',
    18: 'MUX',
    19: 'DCN-MEAS',
    20: 'HMP',
    21: 'PRM',
    22: 'XNS-IDP',
    23: 'TRUNK-1',
    24: 'TRUNK-2',
    25: 'LEAF-1',
    26: 'LEAF-2',
    27: 'RDP',
    28: 'IRTP',
    29: 'ISO-TP4',
    30: 'NETBLT',
    31: 'MFE-NSP',
    32: 'MERIT-INP',
    33: 'DCCP',
    34: '3PC',
    35: 'IDPR',
    36: 'XTP',
    37: 'DDP',
    38: 'IDPR-CMTP',
    39: 'TP++',
    40: 'IL',
    41: 'IPv6',
    42: 'SDRP',
    43: 'IPv6-Route',
    44: 'IPv6-Frag',
    45: 'IDRP',
    46: 'RSVP',
    47: 'GRE',
    48: 'MHRP',
    49: 'BNA',
    50: 'ESP',
    51: 'AH',
    52: 'I-NLSP',
    53: 'SWIPE',
    54: 'NARP',
    55: 'MOBILE',
    56: 'TLSP',
    57: 'SKIP',
    58: 'IPv6-ICMP',
    59: 'IPv6-NoNxt',
    60: 'IPv6-Opts',
    61: 'any host internal protocol',
    62: 'CFTP',
    63: 'any local network',
    64: 'SAT-EXPAK',
    65: 'KRYPTOLAN',
    66: 'RVD',
    67: 'IPPC',
    68: 'any distributed file system',
    69: 'SAT-MON',
    70: 'VISA',
    71: 'IPCV',
    72: 'CPNX',
    73: 'CPHB',
    74: 'WSN',
    75: 'PVP',
    76: 'BR-SAT-MON',
    77: 'SUN-ND',
    78: 'WB-MON',
    79: 'WB-EXPAK',
    80: 'ISO-IP',
    81: 'VMTP',
    82: 'SECURE-VMTP',
    83: 'VINES',
    84: 'TTP',
    85: 'NSFNET-IGP',
    86: 'DGP',
    87: 'TCF',
    88: 'EIGRP',
    89: 'OSPF',
    90: 'Sprite-RPC',
    91: 'LARP',
    92: 'MTP',
    93: 'AX.25',
    94: 'IPIP',
    95: 'MICP',
    96: 'SCC-SP',
    97: 'ETHERIP',
    98: 'ENCAP',
    99: 'any private encryption scheme',
    100: 'GMTP',
    101: 'IFMP',
    102: 'PNNI',
    103: 'PIM',
    104: 'ARIS',
    105: 'SCPS',
    106: 'QNX',
    107: 'A/N',
    108: 'IPComp',
    109: 'SNP',
    110: 'Compaq-Peer',
    111: 'IPX-in-IP',
    112: 'VRRP',
    113: 'PGM',
    114: 'any 0-hop protocol',
    115: 'L2TP',
    116: 'DDX',
    117: 'IATP',
    118: 'STP',
    119: 'SRP',
    120: 'UTI',
    121: 'SMP',
    122: 'SM',
    123: 'PTP',
    124: 'IS-IS over IPv4',
    125: 'FIRE',
    126: 'CRTP',
    127: 'CRUDP',
    128: 'SSCOPMCE',
    129: 'IPLT',
    130: 'SPS',
    131: 'PIPE',
    132: 'SCTP',
    133: 'FC',
    134: 'RSVP-E2E-IGNORE',
    135: 'Mobility Header',
    136: 'UDP Lite',
    137: 'MPLS-in-IP',
    138: 'manet',
    139: 'HIP',
    140: 'Shim6',
    141: 'UNASSIGNED',
    142: 'UNASSIGNED',
    143: 'UNASSIGNED',
    144: 'UNASSIGNED',
    145: 'UNASSIGNED',
    146: 'UNASSIGNED',
    147: 'UNASSIGNED',
    148: 'UNASSIGNED',
    149: 'UNASSIGNED',
    150: 'UNASSIGNED',
    151: 'UNASSIGNED',
    152: 'UNASSIGNED',
    153: 'UNASSIGNED',
    154: 'UNASSIGNED',
    155: 'UNASSIGNED',
    156: 'UNASSIGNED',
    157: 'UNASSIGNED',
    158: 'UNASSIGNED',
    159: 'UNASSIGNED',
    160: 'UNASSIGNED',
    161: 'UNASSIGNED',
    162: 'UNASSIGNED',
    163: 'UNASSIGNED',
    164: 'UNASSIGNED',
    165: 'UNASSIGNED',
    166: 'UNASSIGNED',
    167: 'UNASSIGNED',
    168: 'UNASSIGNED',
    169: 'UNASSIGNED',
    170: 'UNASSIGNED',
    171: 'UNASSIGNED',
    172: 'UNASSIGNED',
    173: 'UNASSIGNED',
    174: 'UNASSIGNED',
    175: 'UNASSIGNED',
    176: 'UNASSIGNED',
    177: 'UNASSIGNED',
    178: 'UNASSIGNED',
    179: 'UNASSIGNED',
    180: 'UNASSIGNED',
    181: 'UNASSIGNED',
    182: 'UNASSIGNED',
    183: 'UNASSIGNED',
    184: 'UNASSIGNED',
    185: 'UNASSIGNED',
    186: 'UNASSIGNED',
    187: 'UNASSIGNED',
    188: 'UNASSIGNED',
    189: 'UNASSIGNED',
    190: 'UNASSIGNED',
    191: 'UNASSIGNED',
    192: 'UNASSIGNED',
    193: 'UNASSIGNED',
    194: 'UNASSIGNED',
    195: 'UNASSIGNED',
    196: 'UNASSIGNED',
    197: 'UNASSIGNED',
    198: 'UNASSIGNED',
    199: 'UNASSIGNED',
    200: 'UNASSIGNED',
    201: 'UNASSIGNED',
    202: 'UNASSIGNED',
    203: 'UNASSIGNED',
    204: 'UNASSIGNED',
    205: 'UNASSIGNED',
    206: 'UNASSIGNED',
    207: 'UNASSIGNED',
    208: 'UNASSIGNED',
    209: 'UNASSIGNED',
    210: 'UNASSIGNED',
    211: 'UNASSIGNED',
    212: 'UNASSIGNED',
    213: 'UNASSIGNED',
    214: 'UNASSIGNED',
    215: 'UNASSIGNED',
    216: 'UNASSIGNED',
    217: 'UNASSIGNED',
    218: 'UNASSIGNED',
    219: 'UNASSIGNED',
    220: 'UNASSIGNED',
    221: 'UNASSIGNED',
    222: 'UNASSIGNED',
    223: 'UNASSIGNED',
    224: 'UNASSIGNED',
    225: 'UNASSIGNED',
    226: 'UNASSIGNED',
    227: 'UNASSIGNED',
    228: 'UNASSIGNED',
    229: 'UNASSIGNED',
    230: 'UNASSIGNED',
    231: 'UNASSIGNED',
    232: 'UNASSIGNED',
    233: 'UNASSIGNED',
    234: 'UNASSIGNED',
    235: 'UNASSIGNED',
    236: 'UNASSIGNED',
    237: 'UNASSIGNED',
    238: 'UNASSIGNED',
    239: 'UNASSIGNED',
    240: 'UNASSIGNED',
    241: 'UNASSIGNED',
    242: 'UNASSIGNED',
    243: 'UNASSIGNED',
    244: 'UNASSIGNED',
    245: 'UNASSIGNED',
    246: 'UNASSIGNED',
    247: 'UNASSIGNED',
    248: 'UNASSIGNED',
    249: 'UNASSIGNED',
    250: 'UNASSIGNED',
    251: 'UNASSIGNED',
    252: 'UNASSIGNED',
    253: 'experimentation and testing',
    254: 'experimentation and testing',
    255: 'Reserved',
    }

def protocol_lookup(protocol_id):
    return PROTOCOLS[protocol_id]

def packet_to_dict(packet):
    d = {}
    d['id'] = packet.id
    d['source_ip'] = packet.source_ip
    d['destination_ip'] = packet.destination_ip
    d['source_port'] = packet.source_port
    d['dest_port'] = packet.dest_port
    d['source_mac'] = packet.source_mac
    d['destination_mac'] = packet.destination_mac
    d['packet_id'] = packet.packet_id
    d['time'] = datetime_to_milliseconds(packet.time)
    d['protocol_id'] = packet.protocol
    d['protocol'] = protocol_lookup(packet.protocol)
    d['payload'] = packet.payload
    d['classification_time'] = datetime_to_milliseconds(packet.classification_time)
    d['attack_id'] = packet.attack.id

    return d

def attack_to_dict(attack):
    d = {}
    d['id'] = attack.id
    d['classification_time'] = datetime_to_milliseconds(attack.classification_time)
    d['source_ip'] = attack.source_ip
    d['destination_ip'] = attack.destination_ip
    d['start_time'] = datetime_to_milliseconds(attack.start_time)
    d['end_time'] = datetime_to_milliseconds(attack.end_time)
    d['score'] = attack.score

    return d

# from <http://djangosnippets.org/snippets/1997/>
def datetime_to_milliseconds(dt=None):
    # Ensure the type matches
    if not dt:
        dt = datetime.datetime.now()

    elif type(dt) == type(datetime.datetime.now()):
        return time.mktime(dt.timetuple())+float("0.%s"%dt.microsecond) * 1000

    elif type(dt) == type(datetime.date.today()):
        return time.mktime(dt.timetuple()) * 1000

    else:
        raise ValueError, "You may only use a datetime.datetime or datetime.date instance with datetime_to_milliseconds"

def parse_arp_records(f):
    for record in f:
        # regular expressions from <http://stackoverflow.com/a/5287465/609144>
        ip = re.search(r'((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9])', record, re.I)
        mac = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', record, re.I)

        if ip and mac:
            ip = ip.group()
            mac = mac.group()


            a, created = ARPRecord.objects.get_or_create(ip=ip, mac=mac)
            print a
            a.save()
