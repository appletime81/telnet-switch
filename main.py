import telnetlib
import time

# 你的設備 IP，這裡為localhost
HOST = "localhost"
PORT = 8000  # 填入你的服務器端口

username = input("Enter your username: ")
password = input("Enter your password: ")
# set 的ip 跟name OSPF 跟port
set_ip = input("Enter your set ip: ")
set_name = input("Enter your set name: ")
set_ospf = input("Enter your set OSPF: ")
set_port1 = input("Enter your set port1: ")
set_port2 = input("Enter your set port2: ")

# Telnet 連線設定
tn = telnetlib.Telnet(HOST, PORT)

# Login
response = tn.read_until(b"User: ")
print(response.decode("ascii"))  # 將響應從二進位轉換為字符串並列印
tn.write(username.encode("ascii") + b"\n")

response = tn.read_until(b"Password: ")
print(response.decode("ascii"))  # 將響應從二進位轉換為字符串並列印
tn.write(password.encode("ascii") + b"\n")

# 確認登入成功
response = tn.read_until(b"Welcome!")
print(response.decode("ascii"))  # 將響應從二進位轉換為字符串並列印
assert b"Welcome!" in response

# 執行你的命令
commands = [
    "CO",
    "set / desc HUB01",
    f"set / id {set_ip}",
    f"set / dataid {set_ip}",
    f"set protocols/ospf rt_id_area {set_ospf}",
    f"cr protocols/ospf area.{set_ospf}",
    f"cr protocols/ospf/area.{set_ospf} type stub",
    f"set protocols/ospf/area.{set_ospf}/type defmetric 1",
    f"set protocols/ospf/area.{set_ospf}/type nosummaries true",
    f"set interfaces/eth/xg.{set_port1} admin up",
    f"set interfaces/eth/xg.{set_port1} role nni",
    f"set interfaces/eth/xe.{set_port1} permon true",
    f"set interfaces/eth/xg.{set_port1} framelen 9600",
    f"set interfaces/eth/xg.{set_port1} als false",
    f"set interfaces/eth/xg.{set_port2} admin up",
    f"set interfaces/eth/xg.{set_port2} role nni",
    f"set interfaces/eth/xe.{set_port2} permon true",
    f"set interfaces/eth/xg.{set_port2} framelen 9600",
    f"set interfaces/eth/xg.{set_port2} als false",
    "CO"
]

for command in commands:
    tn.write(command.encode("ascii") + b"\n")
    time.sleep(1)  # 等待一段時間以確保命令已經執行完成
    output = tn.read_very_eager().decode("ascii")  # 讀取執行結果
    print(f"{command}:\n{output}")  # 顯示執行結果

output = tn.read_very_eager().decode("ascii")  # 讀取執行結果
print(f"\n{output}")

tn.close()  # 關閉連線
