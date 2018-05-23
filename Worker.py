#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Utils import *
from threading import Thread
from Header import Header
from Constant import *
import os
import os.path, time
from mimetypes import MimeTypes
import urllib

class Worker(Thread):
    """docstring for Worker"""

    def __init__(self, client_connection, client_address):
        Thread.__init__(self)

        self.client_connection = client_connection
        self.client_address = client_address
        self.client_request = client_connection.recv(1024).decode()

    def run(self):
        requestHeader = self.parseHeader()

        # Build response header
        pathExist, headerResponse = self.buildHeaderResponse(requestHeader.path)
        self.client_connection.sendall(headerResponse.encode())

        # Build file content
        self.buildResponse(pathExist, requestHeader)

        self.client_connection.close()

    def parseHeader(self):
        header = self.client_request.split("\n")

        firstLineSplited = header[0].split(" ")
        method = firstLineSplited[0]
        path = firstLineSplited[1]

        cookie = None

        for line in header:
            if "Host" in line:
                host = line.split(" ")[1]
            if "Cookie" in line:
                cookie = line.split(" ")[1]

        requestHeader = Header(method, path, host, cookie)

        return requestHeader

    def buildResponse(self, pathExists, requestHeader):

        if pathExists:
            # Deve verificar se o caminho é diretório ou arquivo
            if os.path.isfile(requestHeader.path):
                # Se for arquivo
                self.showFileContent(requestHeader.path)
            else:
                # Se for diretório
                self.showDirContent(requestHeader.path)

        else:
            return None

    def buildHeaderResponse(self, path):
        # Build Response Header
        if os.path.exists(path):
            response = response200
        else:
            response = response404
            # Retorna flag falando que arquivo não existe e erro 404
            self.client_connection.sendall(response.encode())
            return False, response

        self.client_connection.sendall(response.encode())
        # Retorna flag falando que arquivo existe e código 200
        return True, response

    def showFileContent(self, path, size=512):
        mime = MimeTypes()
        mime_type = mime.guess_type(path)
        contentType = 'Content-Type: ' + mime_type[0] + '\r\n\r\n'
        self.client_connection.sendall(contentType.encode())

        file = open(path, "rb")
        bytesSequence = file.read()  # read only 512 bytes in each loop

        while bytes.__len__(bytesSequence):
            self.client_connection.sendall(bytesSequence)  # send the 512 bytes
            bytesSequence = file.read(size)  # get nexts 512 bytes

    def showDirContent(self, path):
        if  path[-1:] != '/':
            path += '/'

        files = os.listdir(path)
        response = "\r\n\r\n" + tableHeader

        for file in files:
            response += "\n<tr>"

            response += "<th><a href=\"" + path + file + "\">" + file + "</th>\n"
            response += "<th>" + time.ctime(os.path.getmtime(path + file)) + "</th>\n"
            response += "<th>" + convertBytes(os.stat(path + file).st_mode) + "</th>"
            response += "</tr>"

        response = response + tableTail

        self.client_connection.sendall(response.encode())
