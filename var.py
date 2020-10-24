from json import load
db_user = ""
db_pass = ""
db_ip = ""
db_port = int()
db_name = "stream"
proxy_user = ""
proxy_pass = ""
proxy_port = int()
time_duration = int()
site = ""
stop = False
stop_all = False
stop_list = list()
main_table_row_count = 0
try:
    with open('config.json') as json_file:
        data = load(json_file)
    config = data['config']
    db_user = config['db_user']
    db_pass = config['db_pass']
    db_ip = config['ip']
    db_port = config['port']
    db_name = config['db_name']
    proxy_user = config['proxy_user']
    proxy_pass = config['proxy_pass']
    proxy_port = config['proxy_port']
    time_duration = config['time_duration']
except Exception as e:
    print("Exeception occured at config loading:{}".format(e))

# "ip": "127.0.0.1", 
# "port": 3306, 
# "db_user": "test", 
# "db_pass": "1234",
# "db_name": "stream", 
# "proxy_user": "lum-customer-hl_fec22e79-zone-zone3",
# "proxy_pass": "hmaltqa5k06o",
# "proxy_port": 45785,
# "time_duration": 39
