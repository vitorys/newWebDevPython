#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from threading import Thread
from Header import Header
from Responses import *

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
		print response
		self.client_connection.sendall(response.encode())

		self.client_connection.close()


	def parseHeader(self):
		header = self.client_request.split("\n")
		
		firstLineSplited = header[0].encode().split(" ")
		method = firstLineSplited[0]
		path = firstLineSplited[1]
		print firstLineSplited

		cookie = None

		for line in header:
			if("Host" in line):
				host = line.split(" ")[1]
			if("Cookie" in line):
				cookie = line.split(" ")[1]

		requestHeader = Header(method, path, host, cookie)

		return requestHeader

	def buildResponse(self, requestHeader):
		# Inicializa variáveis da resposta
		headerResponse = None
		contentOfPath = None

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

			

		else:
			# 404 NOT FOUND
			response = headerResponse
			return response

		#Build content of response


		return headerResponse

	def buildHeaderResponse(self, path):
		# Build Response Header
		if os.path.exists(path):
			response = response200
		else:
			response = response404
			# Retorna flag falando que arquivo não existe e erro 404
			return (False, response)

		# Retorna flag falando que arquivo existe e código 200
		return (True, response)


	# Thanks to @DanielVenturini
	def showFileContent(self, path):
		file = open(path, "rb")
        bytesSequence = file.read(size)        	# read only 512 bytes in each loop
        
        while(bytes.__len__(bytesSequence)):
            self.send(bytesSequence)	        # send the 512 bytes
            bytesSequence = file.read(size)    	# get nexts 512 bytes




	def showDirContent(self, path):
		pass

		
