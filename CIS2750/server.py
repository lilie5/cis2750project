import os
import math
import Physics
import sys;
import cgi;
import json
import math;
import random;

import Physics;
from Physics import Table 

from http.server import HTTPServer, BaseHTTPRequestHandler; 
from urllib.parse import urlparse, parse_qsl, parse_qs; 

svgBallStart = """<li><svg width = "30" height = "30"><circle cx="14.25" cy="14.25" r="14.25" fill="""
svgBallEnd = """></svg>"""
BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];
sunk = """<p> - UNSUNK</p>"""


#our global table and game
table = Table(setup=True)
game_instance = Physics.Game(gameID = 1)


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    game = None
    #global initial_svg
    
    def sendError(self):
        self.send_error(404, 'File Not Found: %s' % self.path)


    def do_GET(self):
        #global initial_svg
        parsed = urlparse(self.path)

        if parsed.path in [ '/index.html' ]:
            try:
                with open("."+self.path) as svgFile:
                    svg = svgFile.read()
            except:
                self.sendError()
            self.send_response( 200 )
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len(svg))
            self.end_headers()
            self.wfile.write(bytes(svg, "utf-8"))
            


        elif parsed.path.startswith("/table-") and parsed.path.endswith(".svg"):
            try:
                with open("."+self.path) as svgFile:
                    tableSvg  = svgFile.read()
            except:
                self.sendError()
            
            self.send_response( 200 )
            self.send_header( "Content-type", "image/svg+xml" )
            self.send_header( "Content-length", len(tableSvg))
            self.end_headers()
            self.wfile.write(bytes(tableSvg, "utf-8"))

        elif parsed.path.endswith(".css"):
            try:
                with open('.' + self.path) as file:
                    css = file.read()
            except:
                self.sendError()
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.send_header("Content-length", len(css))
            self.end_headers()
            self.wfile.write(bytes(css, "utf-8"))

        elif parsed.path.endswith(".html"):
            html = None
            try:
                with open('.' + self.path) as htmlFile:
                    html = htmlFile.read()
            except:
                self.sendError()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(html))
            self.end_headers()
            self.wfile.write(bytes(html, "utf-8"))

        elif parsed.path.endswith(".js"):
            try:
                with open('.' + self.path) as jsFile:
                    js = jsFile.read()
            except:
                self.sendError()
            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.send_header("Content-length", len(js))
            self.end_headers()
            self.wfile.write(bytes(js, "utf-8"))
                
        else:
            # generate error
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );
    
    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path in ['/submit']:
            global table 
            #get length and post data
            contLength = int(self.headers['Content-Length'])
            postData = self.rfile.read(contLength)
            data = json.loads(postData.decode('utf-8'))
            
            # get dx, dy, vx, vy
            dx = data['mouseX'] - data['ballCenterX']
            dy = data['mouseY'] - data['ballCenterY']

            vx = (-1) * 10 * dx
            vy = (-1) * 10 * dy

            #set up our html
            html = "<html><head><title>Pool Game</title><link rel='stylesheet' href='style.css'>"
            html += "<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script><script src='script.js'></script></head><body>"
            
            print("Reaching out to shoot")
            segTable, svgArr = game_instance.shoot( "GameName", "Player1", table, vx, vy ); #we will get our table and our svg array from here
            print("Shoot has returned")
            table = segTable

            html += """<div id="svgContainer" style="position: relative;">"""

            # Iterate over svg_list and position each SVG absolutely
            for svg in svgArr:
                html += f"""<div style="position: absolute; top: 0; left: 0;">{svg}</div>"""
            svgArr = [] #clean, it it has a bunch of unecessary information in it
            html += "</div></body></html>"

            with open('animate.html', 'w') as file:
                file.write(html)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header('Location', '/animate.html')
            self.end_headers()
            self.wfile.write(json.dumps(html).encode('utf-8'))


        if parsed.path in ['/second']:
            #clean our display file; it has junk in it we no longer want
            os.remove('animate.html') #prevents our crashes
            if (table.cueBall() is None): #update cueball (if it doesn't exist)
                cueball = Physics.StillBall(0, Physics.Coordinate(675, 2025))
                table += cueball

            html = "<html><head><title>A4</title><link rel='stylesheet' href='style.css'>"
            html += "<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script><script src='script.js'></script></head><body>"
            html += f"""<div id="svgContainer2" style="position: relative;">{table.svg()}</div><ol>"""
            for item in table:
                if item.__class__ == Physics.StillBall or item.__class__ == Physics.RollingBall:
                    if item.__class__ == Physics.StillBall:
                        if item.obj.still_ball.number != 0 and item.obj.still_ball.number != 8:
                            html += svgBallStart + f"""'{BALL_COLOURS[item.obj.still_ball.number]}'"""
                            html += svgBallEnd + f"<p> - {item.obj.still_ball.number}</p></li>"
                    else:
                        if item.obj.rolling_ball.number != 0 and item.obj.rolling_ball.number != 8:
                            html += svgBallStart + f"""'{BALL_COLOURS[item.obj.rolling_ball.number]}'"""
                            html += svgBallEnd + f"<p> - {item.obj.rolling_ball.number}</p></li>"
            html += '</ol></body></html>' 
            os.remove("second.html")
            with open('second.html', 'w') as file:
                file.write(html)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "hello!"}).encode('utf-8'))

if __name__ == "__main__":
    #create HTTP server and instance
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHTTPRequestHandler)
    print( "Server listing in port:  ", int(sys.argv[1]) )
    httpd.serve_forever()