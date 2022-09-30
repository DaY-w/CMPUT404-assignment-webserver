#  coding: utf-8
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        reqPage = self.data.decode('utf-8').split(" ")[1]
        reqPageSplit = self.data.decode('utf-8').split(" ")[1].split("/")
        reqPageSplit = list(filter(None, reqPageSplit))

        mainDir = os.listdir("./www/")
        nestDir = [x for x in mainDir if "." not in x]

        if ("../" in reqPage):
            self.request.sendall(
                'HTTP/1.1 404 Not Found\r\n'.encode('utf-8'))
            return

        if (self.data.decode('utf-8').split(" ")[0] != "GET"):
            self.request.sendall(
                'HTTP/1.1 405 Not Found\r\n'.encode('utf-8'))
            return

        if (".ico" in reqPage):
            return

        myFile = "./www/{}".format("/".join(reqPageSplit))

        if (reqPage[-1] != "/" and "." not in myFile[1:] and reqPage != "/"):
            self.request.sendall(
                ('HTTP/1.1 301 Moved Permanently\r\nLocation: {}/'.format(reqPageSplit[0])).encode('utf-8'))
            return

        if (myFile[-1] == "/"):
            myFile += "index.html"

        if ("." not in myFile[1:]):
            myFile += "/index.html"

        try:
            file = open(myFile, 'rb')
            response = file.read()
            file.close()

            header = "HTTP/1.1 200 OK\n"
            if (myFile.endswith(".jpg")):
                mimetype = 'image/jpg'
            elif (myFile.endswith(".css")):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'

            header += 'Content-Type: '+str(mimetype)+'\n\n'
        except Exception as e:
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = ''.encode('utf-8')

        final_response = header.encode('utf-8')
        final_response += response

        self.request.sendall(final_response)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    server.serve_forever()
