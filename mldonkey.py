import telnetlib
class MLDonkey():
    """
        Utilitzada per interactuar amb el MLDonkey a traves de Telnet.
    """
    def __init__(host='localhost',port=4000):
        self._host=host
        self._port=port
        self.connected=False

    def connect():
        self._conn = telentlib.Telnet(self._host,self._port)
        self.connected=True

    def disconnect():
        self._conn.close()
        self.connected=False

#Aquestes dos funcions permeten utiltizar el patro with
    def __enter__():
        self.connect()
    def __exit__():
        self.disconnect()

    def new_user(self,username,email,password,max_descarregues=2):
        self._conn.write("useradd %s %s tw 0 %s %d" %
                            username,password,email,max_descarregues)
    def change_pass(self,username,password):
        self._conn.write("useradd %s %s " %
                            username,password)
