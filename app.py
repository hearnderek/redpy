import redis
import cherrypy
import uuid

r = redis.Redis(
        host='localhost',
        port=6379)

class HelloWorld(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def update(self):
        input_json = cherrypy.request.json

        if "key" in input_json:
            id = input_json["key"]
        else:
            id = uuid.uuid4().hex

        payload = input_json["payload"]
        r.set(id, payload)

        result = {"id": id, "payload": payload}
        return result

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def index(self, search): 

        value = r.get(search)
        if value is not None:
            value = value.decode()
        else:
            value = ''

        return {search: value}

    @cherrypy.expose
    def new(self): 
        return uuid.uuid4().hex

cherrypy.quickstart(HelloWorld())


