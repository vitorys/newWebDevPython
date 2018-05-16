from threading import Thread
from Header import Header

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
			if("Host" in line):
				host = line.split(" ")[1]
			if("Cookie" in line):
				cookie = line.split(" ")[1]

		requestHeader = Header(method, path, host, cookie)

		return requestHeader

	def buildResponse(self, requestHeader):
		return "HTTP/1.0 200 OK\r\n\r\nHello World"



		
