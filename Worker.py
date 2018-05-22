#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from threading import Thread
from Header import Header
from Constant import *
import os

class Worker(Thread):
    """docstring for Worker"""

    def __init__(self, client_connection, client_address):
        Thread.__init__(self)

        self.client_connection = client_connection
        self.client_address = client_address
        self.client_request = client_connection.recv(1024).decode()

    def run(self):
        requestHeader = self.parseHeader()

        response = self.buildResponse(requestHeader)
        self.client_connection.sendall(response.encode())

        self.client_connection.close()

    def parseHeader(self):
        header = self.client_request.split("\n")

        firstLineSplited = header[0].split(" ")
        method = firstLineSplited[0]
        path = firstLineSplited[1]

        cookie = None

        for line in header:
            if ("Host" in line):
                host = line.split(" ")[1]
            if ("Cookie" in line):
                cookie = line.split(" ")[1]

        requestHeader = Header(method, path, host, cookie)

        return requestHeader

    def buildResponse(self, requestHeader):

        # Buid response header
        pathExist, headerResponse = self.buildHeaderResponse(requestHeader.path)

        if pathExist:
            # Deve verificar se o caminho é diretório ou arquivo
            if os.path.isfile(requestHeader.path):
                # Se for arquivo
                contentOfPath = self.showFileContent(requestHeader.path)
            else:
                # Se for diretório
                contentOfPath = self.showDirContent(requestHeader.path)
                print(contentOfPath)



        else:
            # 404 NOT FOUND
            response = headerResponse
            return response

        # Build content of response

        return headerResponse + contentOfPath

    def buildHeaderResponse(self, path):
        # Build Response Header
        if os.path.exists(path):
            response = response200
        else:
            response = response404
            # Retorna flag falando que arquivo não existe e erro 404
            return False, response

        # Retorna flag falando que arquivo existe e código 200
        return True, response

    def showFileContent(self, path):
        # file = open(path, "rb")
        # bytesSequence = file.read(size)        	# read only 512 bytes in each loop

        # while(bytes.__len__(bytesSequence)):
        #    self.send(bytesSequence)	        # send the 512 bytes
        #    bytesSequence = file.read(size)    	# get nexts 512 bytes
        pass

    def showDirContent(self, path):
        files = os.listdir(path)
        response = "\r\n\r\n" + tableHeader
        for file in files:
            response += "\n<tr>"
            response += "<th>"+ file +"<\th>"
            response += "<th>to be done<\th>"
            response += "<th>To be done<\th>"
