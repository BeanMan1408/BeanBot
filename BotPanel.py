# -----------------------------------------------------
# NOTE: Currently Scraped
# -----------------------------------------------------


from http.server import BaseHTTPRequestHandler, HTTPServer
import paho.mqtt
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import SECRET

hostname = SECRET.HOSTNAME
serverport = SECRET.SERVERPORT
Broker = SECRET.BROKER
Port = SECRET.PORT
Topic = SECRET.TOPIC


def pub(message):
    client = mqtt.Client(client_id=SECRET.CLIENTUSER, transport="tcp",
                         clean_session=False, userdata=None)
    client.connect(Broker, port=Port, keepalive=60)
    client.publish(topic=Topic, payload=message,
                   qos=1, retain=False)
    client.disconnect()
    pass


def close():
    webServer.server_close()


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        file = open("BeanBotPanel.html", "r")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(str(file.read()), "utf-8"))

    def do_POST(self):
        length = int(self.headers.get('Content-length', 0))
        data = self.rfile.read(length).decode()
        print(data)
        pub(data)
        close()
        pass


webServer = HTTPServer((hostname, serverport), MyServer)


if __name__ == "__main__":
    webServer = HTTPServer((hostname, serverport), MyServer)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
