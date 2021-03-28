from flask import Flask, render_template_string, request
import logging

import firebase_admin
from firebase_admin import db

cred_object = firebase_admin.credentials.Certificate('androjerry-36582-firebase-adminsdk-355ix-a3d830de02.json')
default_app = firebase_admin.initialize_app(cred_object, {
	"databaseURL":'https://androjerry-36582-default-rtdb.firebaseio.com/'
	})

ref = db.reference("/")


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)


TPL = '''
<html>
    <body>
        <button id="connectbtn" onclick="requestPermission()">Connect</button>
        <button id="calibratebtn" onclick="calibrate()">Calibrate</button>
        <div id="outputdiv"></div>
    </body>
    <script>
    var output = document.getElementById("outputdiv");
    
    var initPos_h = 0;
    var initPos_v = 0;
    
    var socket = false;
    var leftright = 0;
    var updown = 0;
    
    function sendToFlask()
    {
        const xhr = new XMLHttpRequest();
        const data = new FormData();
        data.append("leftright", leftright);
        data.append("updown", updown);
        xhr.open("POST", "movepointer");
        xhr.send(data);
    }
    function requestPermission()
    {
        output.innerHTML = "Android device";
        if(window.DeviceOrientationEvent) {
            window.addEventListener('deviceorientation', function(event) {
                updown = event.beta - initPos_v; 
                leftright = event.alpha - initPos_h;
                });
        }
        finishRequest();
    }
    function calibrate()
    {
        initPos_h = leftright;
        initPos_v = updown;
    }
    function finishRequest()
    {
        setInterval(sendToFlask, 100);
    }
    </script>
</html>
'''

@app.route("/")
def serveRoot():
    return render_template_string(TPL)

data = {
    "h_val":0,
    "v_val":0
}

@app.route("/movepointer", methods=["POST"])
def movepointer():
    global data
    h_val = float(request.form["leftright"])
    v_val = float(request.form["updown"])
    print('Horizontal: '+str(h_val)+'          Vertical: '+str(v_val))

    data['h_val'] = h_val
    data['v_val'] = v_val    

    ref.set(data)

    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0")