import json
from os.path import join, dirname
from watson_developer_cloud import PersonalityInsightsV3
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi


personality_insights = PersonalityInsightsV3(
version='2016-10-20',
username="YOUR-USERNAME",
password="YOUR-PASSWORD")

def getValue(i,decoded,start_char,end_char1,end_char2):
    i += 1
    while decoded[i]!=start_char:
        i+=1
    i+=1
    temp = ''
    while decoded[i]!=end_char1 and decoded[i]!=end_char2:
        temp += decoded[i]
        i += 1
    return temp

def parseJSON(decoded):
    temp = ''
    send_back = []
    f = False
    adder = []
    open_brace = []
    close_brace = []
    for i in range(len(decoded)):
        if decoded[i] == '[':
            open_brace += [len(send_back)]
        elif decoded[i] == ']':
            close_brace += [len(send_back)]
        elif decoded[i] == '"':
            if f:
                if temp == 'name':
                    send_back += [getValue(i,decoded,'"','"','"')]
                elif temp == 'score' or temp == 'raw_score':
                    send_back += [getValue(i,decoded,' ','\n',',')]
                temp = ''
            f = not f
        elif f:
            temp += decoded[i]
    return [send_back,open_brace,close_brace]

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        self._set_headers()

        the_text = str(self.rfile.read(int(self.headers['content-length'])))[7:]
        profile = personality_insights.profile(
        the_text, content_type='text/plain',
        raw_scores=True, consumption_preferences=True)

        out = list(json.dumps(profile, indent=2))

        resp = str(parseJSON(out))

        self.wfile.write(resp.encode())
        
def run():
    httpd = HTTPServer(('localhost', 8888), S)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
    
##    profile = personality_insights.profile(
##    request, content_type='text/plain',
##    raw_scores=True, consumption_preferences=True)
##
##    out = (json.dumps(profile, indent=2))
##    


##
##with open('op_file.json','w') as file:
##    file.write(out)
##    file.close()
