import logging
logging.basicConfig(level=logging.DEBUG)
from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode, Float
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server


class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(self, name, times):
        for i in range(times):
            yield 'Hello, %s' % name
   
    @rpc(Unicode, Integer, _returns=Unicode)
    def say_hello2(self, name, times):
        return ("yes")

    @rpc(Float, Float, _returns=Float)
    def livraison(self, poids, distance):
        return poids * (distance * (1/4) )



application = Application([HelloWorldService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

app = WsgiApplication(application)
