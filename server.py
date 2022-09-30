#  coding: utf-8
import socketserver
from urllib import response
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

        if(self.data.decode('utf-8').split(" ")[0] != "GET"):
            self.request.sendall(
                'HTTP/1.1 405 Not Found\r\n'.encode('utf-8'))
            return

        if (".ico" in reqPage):
            return

        # print(reqPage)

        myFile = "./www/{}".format("/".join(reqPageSplit))

        if (myFile[-1] == "/" and "." not in myFile[1:]):
            print("CHANGED")
            self.request.sendall(
                ('HTTP/1.1 301 Moved Permanently\r\nLocation: {}/index.html'.format(reqPageSplit[0])).encode('utf-8'))
            return
        # print(myFile)
        if (myFile[-1] == "/"):
            myFile += "index.html"
        if ("." not in myFile[1:]):
            # print("change")
            myFile += "/index.html"

        # print(myFile)
        # print("./www/{}".format("/".join(reqPageSplit)))
        # if (len(reqPageSplit) == 0):
        #     print("./www/index.html")
        # else:
        #     print("./www/{}".format("".join(reqPageSplit)))

        # if (len(reqPageSplit) == 0 or 'index.html' in reqPageSplit[0]):
        #     myFile = "./www/index.html"
        # else:
        #     if (".css" in reqPageSplit[0]):
        #         # print(reqPage)
        #         myFile = "./www/base.css"
        #     elif ("deep" in reqPageSplit[0]):
        #         if (len(reqPageSplit) > 1 and ".css" in reqPageSplit[1]):
        #             myFile = "./www/deep/deep.css"
        #         else:
        #             myFile = "./www/deep/index.html"

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

        # print("header", header, type(header))
        final_response = header.encode('utf-8')
        # print("final", final_response, type(final_response))
        # if (type(response) == "str"):
        # print("Not bytes", response)
        # print("response", response, type(response))
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
