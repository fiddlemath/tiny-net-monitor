from speedtest import Speedtest
from plumbum.cmd import ping
import yaml
# import schema
import re

testing = True

def check_speed():
    s = Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    return {
        'down': s.results.download, #units: bits per second
        'up': s.results.upload, #units: bits per second
        'ping': s.results.ping #units: milliseconds
    }

def check_ping(address='8.8.8.8'):
    if testing:
        num_pings, delay = 5, 0.2
    else:
        num_pings, delay = 100, 5
    
    p = ping['-c'][num_pings]['-i'][delay]
    output = p(address)
    return parse_ping(output)

def parse_ping(stdout):
    lines = stdout.splitlines()

    times = {}
    timeouts = []
    packet_data = None
    stats = None
    unparsed_lines = []
    
    # Geh. This feels derpy. Suggestions?
    for line in lines:
        match = re.match(r'[0-9]+ bytes from [0-9.]+: icmp_seq=([0-9]+) ttl=[0-9]+ time=([0-9.]+) ms', line)
        if match:
            seq_s, time_s = match.group(1,2)
            seq, time = int(seq_s), float(time_s)
            times[seq] = time
            continue

        match = re.match(r'Request timeout for icmp_seq ([0-9]+)', line)
        if match:
            seq = int(match.group(1))
            timeouts.append(seq)
            continue

        match = re.match(r'([0-9]+) packets transmitted, ([0-9]+)( packets)? received, ([0-9.]+)% packet loss.*', line)
        if match:
            total, got, loss = match.group(1,2,4)
            packet_data = {
                'total': int(total),
                'completed': int(got),
                'loss': float(loss),
                }
            continue
        
        match = re.match(r'.* min/avg/max/.*dev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms', line)
        if match:
            min_t, avg_t, max_t, dev = match.group(1,2,3,4)
            stats = {
                'min': float(min_t),
                'avg': float(avg_t),
                'max': float(max_t),
                'stddev': float(dev)
                }
            continue

        if line.strip() == '' or \
            re.match(r'PING \d+\.\d+\.\d+\.\d+.*', line) or \
            re.match(r'--- [0-9.]+ ping statistics ---', line):
            continue

        # Line has unknown meaning. Leave it in this data.
        unparsed_lines.append(line)

    return {
        'stats': stats,
        'packets': packet_data,
        'times': times,
        'timeouts': timeouts,
        'unparsed_lines': unparsed_lines
    }
        

#  if __name__ == "__main__":
#    print check_speed()
#    print check_ping()

