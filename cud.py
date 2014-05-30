import os, os.path
import random
import string

import cherrypy
import telnetlib

class CudIndex(object):

    @cherrypy.expose
    def index(self):
        print 'returning index'
        return file('index.html')

class CudConnect(object):
    exposed = True

    def POST(self, server='hey', port='bub'):
        print 'connecting {0} {1}'.format(server,port)
        the_telnet = telnetlib.Telnet(server, int(port))
        cherrypy.session['server'] = the_telnet

class CudInput(object):
    exposed = True

    def PUT(self, input_string):
        print 'input >>{0}<<'.format(input_string)
        cherrypy.session['server'].write('{0}\n'.format(input_string))

class CudLog(object):
    exposed = True
    def GET(self):
        print 'getting...'
        val=''
        try:
            val=cherrypy.session['server'].read_very_eager()
            if val:
                val = val.replace('\n','<br>') + '\n'
        except EOFError:
            print 'CLOSED!'
            val = '%%%'
            cherrypy.session['server'].close()
        return val

class CudKill(object):
    exposed = True
    def PUT(self):
        print 'KILLED!'
        cherrypy.session['server'].close()

if __name__ == '__main__':

    cherrypy.tree.mount(
        CudIndex(), '/',
        {'/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
            },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
            }
        }
    )

    cherrypy.tree.mount(
        CudConnect(), '/connect',
        {'/': {
                'tools.sessions.on': True,
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
            }
        }
    )

    cherrypy.tree.mount(
        CudInput(), '/input',
        {'/': {
                'tools.sessions.on': True,        
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
                }
        }
    )

    cherrypy.tree.mount(
        CudLog(), '/log',
        {'/': {
                'tools.sessions.on': True,
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
                }
        }
    )

    cherrypy.tree.mount(
        CudKill(), '/kill',
        {'/': {
                'tools.sessions.on': True,
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
                }
        }
    )

    cherrypy.engine.start()
    cherrypy.engine.block()
    
if __name__ == '__mainXXXX__':
    conf = {
        '/': {
         'tools.sessions.on': True,
         'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/connect': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = Cud()
    webapp.generator = CudWebService()
    cherrypy.quickstart(webapp, '/', conf)
