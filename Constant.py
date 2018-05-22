#!/usr/bin/env python
# -*- coding: utf-8 -*-

response404 = "HTTP/1.1 404 Not Found\r\n\r\n";
response200 = "HTTP/1.1 200 OK\r\n"
response401 = "\"HTTP/1.1 401 Unauthorized\r\nDate: Wed, 21 Oct 2015 07:28:00 GMT" + "\r\nWWW-Authenticate: Basic realm=\\\"Access to staging site\\\"\r\n\r\n";

tableHeader = "<head><meta charset=\"UTF-8\"></head>" + "\n<h1>Index of </h1>" + "<table><tbody>"+ "<tr>"+ "<th> Nome </th>"+ "<th> Data de Motificação</th>"+ "<th> Tamanho</th>"+ "</tr>"+ "<th colspan=\"5\"><hr></th>"
tableTail = "<th colspan=\"5\"><hr></th>" + "</table></tbody>"
