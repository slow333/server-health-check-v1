# Execute multiple commands by chaining them with a semicolon.
# This ensures they run in the same shell session.

sv_info = [
    {'name': "echo hostname;", 'cmd': 'hostname;' },
    {'name': "echo ip_address;", 'cmd': 'hostname -I;' },
    {'name': "echo os_info;", 'cmd': 'uname -a;' },
    {'name': "echo uptime;", 'cmd': 'uptime;'},
    {'name': "echo checked_date;", 'cmd': 'date "+%Y-%m-%d %H:%M";'},
]

sv_resource = [
    {'name': "echo free_memory;", 'cmd': "free -m  | awk 'NR==2 {print (($6+$4+$5)/$2)*100 }';" },
    {'name': "echo cpu_cores;", 'cmd': 'grep -c processor /proc/cpuinfo;' },
    {'name': "echo cpu_usage;", 'cmd': "vmstat 1 1 | tail -n 1 | awk '{print $13}'" },
    {'name': "echo disk_usage;", 'cmd': 'df -h;' },
]

sv_sysctl = [
    {'name': "echo vm.swappiness;", 'cmd': 'sysctl vm.swappiness;' },
    {'name': "echo vm.dirty_ratio;", 'cmd': 'sysctl vm.dirty_ratio;' },
    {'name': "echo vm.dirty_background_ratio;", 'cmd': 'sysctl vm.dirty_background_ratio;' },
    {'name': "echo vm.overcommit_memory;", 'cmd': 'sysctl vm.overcommit_memory;' },
    {'name': "echo vm.overcommit_ratio;", 'cmd': 'sysctl vm.overcommit_ratio;' },
]

sv_conn = [
    {'server_name': 'rhel8', 'ip_addr': '192.168.219.111', 'username': 'root', 'password': '1', 'port': 22},
    {'server_name': 'rhel7','ip_addr': '192.168.219.7', 'username': 'root', 'password': '1', 'port': 22},
    {'server_name': 'rhel6','ip_addr': '192.168.253.6', 'username': 'root', 'password': '1', 'port': 22},
    {'server_name': 'rhel9','ip_addr': '192.168.2253.9', 'username': 'root', 'password': '1', 'port': 22},
]