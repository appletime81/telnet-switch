import asyncio


class SimpleTelnetProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.command_list = [
            b"CO",
            b"set / desc HUB01",
            b"set / id 192.168.1.1",
            b"set / dataid 192.168.1.1",
            b"set protocols/ospf rt_id_area 30",
            b"cr protocols/ospf area.30",
            b"cr protocols/ospf/area.30 type stub",
            b"set protocols/ospf/area.30/type defmetric 1",
            b"set protocols/ospf/area.30/type nosummaries true",
            b"set interfaces/eth/xg.1.1 admin up",
            b"set interfaces/eth/xg.1.1 role nni",
            b"set interfaces/eth/xe.1.1 permon true",
            b"set interfaces/eth/xg.1.1 framelen 9600",
            b"set interfaces/eth/xg.1.1 als false",
            b"set interfaces/eth/xg.1.2 admin up",
            b"set interfaces/eth/xg.1.2 role nni",
            b"set interfaces/eth/xe.1.2 permon true",
            b"set interfaces/eth/xg.1.2 framelen 9600",
            b"set interfaces/eth/xg.1.2 als false",
            b"CO"
        ]
        self.login = False
        self.transport.write(b"User: ")

    def data_received(self, data):
        print(self.login, data, data.strip())
        if not self.login:
            if data.strip() == b"ems":
                self.transport.write(b"Password: ")
                self.login = True
        elif self.login and data.strip() == b"ems":
            print(self.login)
            self.transport.write(b"Welcome!\n#")
        elif self.login:
            if data.strip() == self.command_list[0]:
                """
                如果讀取到"CO"，回傳以下
                ```
                SUCCESS, Entering configuration
                0s, 8803.59375k
                [edit ne]
                CFG#
                ```
                """
                if self.command_list[0] == b"CO":
                    self.transport.write(b"SUCCESS, Entering configuration\n")
                    self.transport.write(b"0s, 8803.59375k\n")
                    self.transport.write(b"[edit ne]\n")
                    self.transport.write(b"CFG#\n")

                self.command_list.pop(0)
                self.transport.write(b"SUCCESS\n")

    def connection_lost(self, exc):
        self.transport.close()


loop = asyncio.get_event_loop()
coro = loop.create_server(SimpleTelnetProtocol, "localhost", 8000)
server = loop.run_until_complete(coro)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
