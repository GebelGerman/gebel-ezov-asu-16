#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sqlite3 
import json
import hashlib

def hash(string:str):
    s = hashlib.sha256()
    s.update(string.encode('utf-8'))
    news=s.hexdigest()
    return news

conn = sqlite3.connect('web.db')
cur = conn.cursor()

# def parseJsonAuth(jsonn):
#     jsonn = json.loads(jsonn)
#     return (jsonn['email'], jsonn['password'])
# def parseJsonReg(jsonn):
#     jsonn = json.loads(jsonn)
#     return (jsonn['nickname'],jsonn['email'], jsonn['password'])


def addUser(jsonn):
    jsonn = json.loads(jsonn)
    string = jsonn['password']+jsonn['nickname']
    password = hash(string)
    cur.execute("INSERT INTO users (nickname, email, password) VALUES(?,?,?)", (str(jsonn['nickname']),str(jsonn['email']),password))
    conn.commit()

def searchUser(jsonn):
    jsonn = json.loads(jsonn)
    cur.execute("SELECT nickname, password FROM users WHERE email=?", (str(jsonn['email']),))
    try:
        result = cur.fetchone()
        password = hash(jsonn['password']+str(result[0]))
        return password == result[1]
    except Exception:
        return False

URLS = {
    '/':'../index.html',
    '/auth':'../authorization.html',
    '/reg':'../registration.html',
    '/user':'../user.html'
}

def parseRequest(req):
    parse = req.split(' ')
    return (parse[0], parse[1])

def parsePOST(req):
    parse = req.split('no-cache\r\n\r\n')
    return parse[1]


def genHeaders(method, url):
    if method=='POST':
        if url=='/reg':
            return ('HTTP/1.1 200 OK\n\n', 'reg')
        if url=='/auth':
            return ('HTTP/1.1 200 OK\n\n', 'auth')
    if not (url in URLS):
        try:
            with open('..'+url, 'r') as file:
                file.close()
            return ('HTTP/1.1 200 OK\n\n', '..'+url)
        except FileNotFoundError:
            return ('HTTP/1.1 404 Not found\n\n', '')
    else:
        return ('HTTP/1.1 200 OK\n\n', URLS[url])

def genResponce(req):
    method, url = parseRequest(req)
    headers, filename = genHeaders(method, url)
    if filename != '':
        if filename == 'reg':
            addUser(parsePOST(req))           
            return (headers, 'txt')
        if filename == 'auth':
            if searchUser(parsePOST(req)): 
                with open('../user.html','w') as file:
                    file.write("<h1>IT IS YOUR PAGE!!!</h1>")
                    file.close()
                return (headers, 'txt')
            else: 
                with open('../user.html','w') as file:
                    file.write("<h1>ERROR 404</h1><p>Not Found</p>")
                    file.close()
                return (headers, 'txt')
        if 'img' in filename:
            with open(filename, 'rb') as file:
                return (file.read(), 'img')
        else:
            with open(filename, 'r', encoding='utf-8') as file:
                return (headers + file.read(), 'txt')
    else: 
        return (headers+'<h1>ERROR 404</h1><p>Not Found</p>', 'txt')

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
            
            response, filename = genResponce(request.decode())
            if filename == 'img':
                clientSock.send(response)
                clientSock.close()     
            else:
                clientSock.sendall(response.encode())
                clientSock.close()     
        except IndexError:
            pass     

if __name__ == "__main__":
    run()