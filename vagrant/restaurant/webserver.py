from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind = engine)
                session = DBSession()
                restaurant_names = session.query(Restaurant).all()
                session.close()
                output = ""
                output += "<html><body>"
                for restaurant_name in restaurant_names:
                    output += "<h1>{0}</h1>".format(restaurant_name.name)
                    output += "<div><a href='/edit'>Edit</a></div>"
                    output += "<div><a href='/delete'>Delete</a></div>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add a new Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action=''><h2>What is the restaurant name?</h2><input name="name" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: {0}'.format(self.path))

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                try:
                    messagecontent = fields.get('message')
                    output = ""
                    output += "<html><body>"
                    output += " <h2> Okay, how about this: </h2>"
                    output += "<h1> {0} </h1>".format(messagecontent[0])
                    output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                except:
                    messagecontent = fields.get('name')
                    output = ""
                    output += " <h2> {0} added </h2>".format(messagecontent[0])
                    output += "</body></html>"
                    self.wfile.write(output)
                    engine = create_engine('sqlite:///restaurantmenu.db')
                    Base.metadata.bind = engine
                    DBSession = sessionmaker(bind=engine)
                    session = DBSession()
                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                    session.close()
                    print output

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port {0}".format(port)
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()