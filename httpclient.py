#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust, Carson McLean
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
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
    # def __str__(self):
    #     return self.code + "\r\n" + self.body

class HTTPClient(object):
    #def get_host_port(self,url):

    clientSocket = None

    def connect(self, host, port):
        # use sockets!
        if port is None:
            port = 80

        # Joshua Campbell
        # CMPUT 404 Lab 2
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((str(host), int(port)))

        return None

    def get_code(self, data):
        try:
            code = int(data.split(" ")[1])
        except:
            code = 400

        return code

    def get_headers(self,data):
        try:
            headers = data.split("\r\n\r\n")[0]
        except:
            headers = ""
        return headers

    def get_body(self, data):
        try:
            body = data.split("\r\n\r\n")[1]
        except:
            body = ""
        return body

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
        return str(buffer)

    def GET(self, url, args=None):
        # TODO: Fix this. Had trouble with Python "if not" concept
        if  (url.startswith("http://") or url.startswith("https://")):
            parsed_url = urlparse(url)
        else:
             url = "http://" + url
             parsed_url = urlparse(url)

        self.connect(parsed_url.hostname, parsed_url.port)

        file = parsed_url.path
        if file=="":
            file = "/"

        HTTP_request = "GET " + file + " HTTP/1.1\r\nHost: " + parsed_url.hostname + "\r\nAccept: */*\r\nConnection: Close\r\n\r\n"

        self.clientSocket.send(HTTP_request)

        received = self.recvall(self.clientSocket)

        code = self.get_code(received)
        body = self.get_body(received)

        return HTTPResponse(code,body)

    def POST(self, url, args=None):
        # TODO: Fix this. Had trouble with Python "if not" concept
        if  (url.startswith("http://") or url.startswith("https://")):
            parsed_url = urlparse(url)
        else:
             url = "http://" + url
             parsed_url = urlparse(url)
        self.connect(parsed_url.hostname, parsed_url.port)

        file = parsed_url.path
        if file=="":
            file = "/"

        if args:
            encoded_args = urllib.urlencode(args)
            length = len(encoded_args)
        else:
            encoded_args = ""
            length = 0

        content_type = "application/x-www-form-urlencoded"

        HTTP_request = ("POST " + file + " HTTP/1.1\r\n"
                        "Host: " + parsed_url.hostname + "\r\n"
                        "Accept: */*\r\n"
                        "Content-Length: " + str(length) + "\r\n"
                        "Content-Type: " + content_type + "\r\n"
                        "Connection: Close\r\n\r\n")
        HTTP_request += encoded_args
        print(HTTP_request)

        self.clientSocket.send(HTTP_request)

        received = self.recvall(self.clientSocket)

        code = self.get_code(received)
        body = self.get_body(received)

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
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )
