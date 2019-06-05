#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import views



URLS = {
    '/':'../index.html',
    '/auth':'../authorization.html',
    '/reg':'../registration.html',
}

def parseRequest(req):
    parse = req.split(' ')
    return (parse[0], parse[1])

def genHeaders(method, url):
    if not (url in URLS):
        try:
            with open('..'+url, 'r') as file:
                file.close()
            return ('HTTP/1.1 200 OK\n\n', '..'+url)
        except FileNotFoundError:
            print('файл не найден')
            return ('HTTP/1.1 404 Not found\n\n', 0)
    else:
        return ('HTTP/1.1 200 OK\n\n', URLS[url])

def genResponce(req):
    method, url = parseRequest(req)
    headers, filename = genHeaders(method, url)
    if filename != 0:
        if 'img' in filename:
            with open(filename, 'rb') as file:
                return (file.read(), 'img')
        else:
            with open(filename, 'r', encoding='utf-8') as file:
                return (headers + file.read(), 'txt')
    else: 
        return (headers, 'txt')

def run():
    serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    serverSock.bind(('localhost', 5000))
    serverSock.listen()
    print('----------server is working------------')

    while True:
        try:
            clientSock, addr = serverSock.accept()#кортеж
            request = clientSock.recv(1024)

            print(request)
            print()
            print(addr)
            
            response, file = genResponce(request.decode())
            if file == 'img':
                clientSock.send(response)
                clientSock.close()     
            else:
                clientSock.sendall(response.encode())
                clientSock.close()     
        except IndexError:
            pass     

if __name__ == "__main__":
    run()