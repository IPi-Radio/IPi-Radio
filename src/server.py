#! /usr/bin/env python3

import os
import sys
import json
import socket
import signal
import mimetypes
import urllib.parse as urlparse

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler

RADIOSTATIONS = "stations.json"
SETTINGS = "settings.json"

class Webserver(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            filepath = self.path[1:]
            # Reading the file

            # check for images
            if self.path.endswith("png"):
                resp: bytes = open(filepath, "rb").read()
            else:
                file_to_open: str = open(filepath).read()
                resp: bytes = file_to_open.encode("utf-8")

            self.send_response(200)
            #print(mimetypes.guess_type(filepath))
            self.send_header("Content-type", mimetypes.guess_type(filepath)[0])
        except:
            resp = b"File not found"
            self.send_response(404)
        
        self.end_headers()
        self.wfile.write(resp)


    def do_POST(self):

        if self.path == "/api/stations/all":
            resp: bytes = open(RADIOSTATIONS, "rb").read()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(resp)

        elif self.path == "/api/stations/clear":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            self._clearAllStations()

            self.wfile.write(b"OK")

        elif self.path.startswith("/api/stations/remove/"):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            data = urlparse.unquote_plus(os.path.basename(self.path))
            self._removeStation(data)

            self.wfile.write(b"OK")

        elif self.path == "/api/stations/add":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            data: dict = json.loads(urlparse.unquote(body.decode()))
            self._addStation(data)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            self.wfile.write(b"OK")

        elif self.path == "/api/stations/saveall":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            data: dict = json.loads(urlparse.unquote(body.decode()))

            self._updateAllStations(data)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            self.wfile.write(b"OK")

        else:
            self.send_error(404, "API Endpoint not found")

        #data = self.rfile.read( int(self.headers['Content-Length']) )
        #print(data)

        #self.wfile.write( json.dumps(resp).encode("utf-8") )

    def _addStation(self, newStation: dict):
        with open(RADIOSTATIONS, "r+") as f:
            stations: dict = json.load(f)

            entry = {
                "url": newStation.get("url"),
                "time": newStation.get("time"),
                "codec": newStation.get("codec"),
                "bitrate": newStation.get("bitrate"),
                "countrycode": newStation.get("countrycode"),
                "language": newStation.get("language")
            }

            stations[newStation["name"]] = entry

            # clear file
            f.seek(0)
            f.truncate()

            json.dump(stations, f, indent=4)

        return True

    def _removeStation(self, name: str):
        with open(RADIOSTATIONS, "r+") as f:
            stations: dict = json.load(f)
            stations.pop(name)
            # clear file
            f.seek(0)
            f.truncate()

            json.dump(stations, f, indent=4)
        return True

    def _updateAllStations(self, data: dict):
        stations = dict()

        for st in data:
            try:
                bitr = int(st.get("bitrate"))
            except:
                bitr = 0
            tmp = {
                "time": st.get("time"),
                "url": st.get("url"),
                "codec": st.get("codec"),
                "bitrate": bitr,
                "countrycode": st.get("countrycode"),
                "language": st.get("language"),
            }
            
            stations[st["name"]] = tmp

        with open(RADIOSTATIONS, "w") as f:
            json.dump(stations, f, indent=4)

        return True

    def _clearAllStations(self):
        with open(RADIOSTATIONS, "w") as f:
            f.write("{}")
        return True

    def _getAllStations(self) -> bytes:
        with open(RADIOSTATIONS, "r") as f:
            data = json.load(f)

        return data

def run(ip_port: tuple):

    httpServer = HTTPServer(ip_port, Webserver)

    try:
        signal.signal(signal.SIGTERM, httpServer.server_close)
        httpServer.serve_forever()
    except KeyboardInterrupt:
        httpServer.server_close()
        print("Webserver exited")

if __name__ == "__main__":
    #run()
    print("running directly is not supported")

    exit()

    print("loading settings...")
    # load settings
    with open(SETTINGS, "r") as f:
        settings: dict = json.load(f)

    print("checking network connection...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("1.1.1.1", 80))
        global CURRIP
        CURRIP = s.getsockname()[0]

    if settings.get("runWebserver"):
        print("starting HTTP server...")
        if settings.get("IP") not in ["DHCP, AUTO, auto"]:
            CURRIP = settings.get("IP")

        print(f"current IP is: {CURRIP}")