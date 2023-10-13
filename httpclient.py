#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
from urllib.parse import urlparse, urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        # return code
        data_list = data.split('\r\n')
        code = int(data_list[0].split()[1])
        return code

    def get_headers(self, data):
        # rerurn headers
        data_list = data.split('\r\n\r\n')
        headers = data_list[0]
        return headers

    def get_body(self, data):
        # return body
        data_list = data.split('\r\n\r\n')
        body = data_list[1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        
        # getting host, path and port from url
        url_data = urlparse(url)
        host = url_data.hostname
        path = url_data.path
        port = url_data.port
        
        # if path is empty or none
        if path == '':
            path = '/'
        if port == None:
            port = 80
        
        self.connect(host, port)
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nAccept: */*\r\nConnection: close\r\n\r\n"

        # send request and recive data
        self.sendall(request)
        reciv_data = self.recvall(self.socket)
        code = self.get_code(reciv_data)
        headers = self.get_headers(reciv_data)
        body = self.get_body(reciv_data)

        # print result to stdout
        print("Headers:\n"+headers)
        print("Code:", code)
        print("Body:\n"+body)
        
        # closing the socket.
        self.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):

        url_data = urlparse(url)
        host = url_data.hostname
        path = url_data.path
        port = url_data.port

        # if path is empty or none
        if path == '':
            path = '/'
        if port == None:
            port = 80

        # connecting to the host with the port.
        self.connect(host, port)
        if not args:
            args = ''
        else:
            args = urlencode(args)
        
        # reference: TA help session
        request = f"POST {path} HTTP/1.1\r\nHost: {host}\r\nAccept: */*\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(args)}\r\nConnection: close\r\n\r\n{args}"
        # send request and recive data
        self.sendall(request)
        reciv_data = self.recvall(self.socket)
        code = self.get_code(reciv_data)
        headers = self.get_headers(reciv_data)
        body = self.get_body(reciv_data)

        # print result to stdout
        print("Headers:\n"+headers)
        print("Code:", code)
        print("Body:\n"+body)
 
        self.close()    
        return HTTPResponse(code, body)


    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))