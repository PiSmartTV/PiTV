from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import UnixAuthorizer
from pyftpdlib.filesystems import UnixFilesystem
from threading import Thread


class FTPThread(Thread):
    def __init__(self):
        super().__init__(target=self.serve_forever)

        self.setDaemon(True)
        self.setName("FTP Daemon")

        self.authorizer = UnixAuthorizer(
            rejected_users=["root"], require_valid_shell=True)
        self.handler = FTPHandler
        self.handler.authorizer = self.authorizer
        self.handler.abstracted_fs = UnixFilesystem
        self.server = FTPServer(('127.0.0.1', 21), self.handler)

    def serve_forever(self):
        self.server.serve_forever()

        
