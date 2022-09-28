#  coding: utf-8
import socketserver
from urllib import response

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
        print("Got a request of: %s\n" % self.data)
        # print(self.data.decode('utf-8').split(" ")[1])
        reqPage = self.data.decode('utf-8').split(" ")[1].split("/")
        reqPage = list(filter(None, reqPage))
        # print(reqPage)
        if (len(reqPage) == 0 or 'index.html' in reqPage[0]):
            myFile = "./www/index.html"
        else:
            if (".css" in reqPage[0]):
                myFile = "./www/base.css"
            elif ("deep" in reqPage[0]):
                if (".css" in reqPage[1]):
                    myFile = "./www/deep/deep.css"
                else:
                    myFile = "./www/deep/index.html"

        # if (self.data.decode('utf-8').split(" ")[1] == "/"):
        #     myFile = "./www/index.html"
        #     print("MAINNNN")
        # elif (self.data.decode('utf-8').split(" ")[1].strip() == "/deep/index.html"):
        #     print("DEEEEEEEEEEEEEEEEEEEEEEEEp")
        #     myFile = "./www/deep/index.html"
        # else:
        #     myFile = "./www/base.css"
        #     print("fail")

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
            response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'

        final_response = header.encode('utf-8')
        final_response += response

        self.request.sendall(final_response)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
