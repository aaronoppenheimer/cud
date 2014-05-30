import os, os.path
import random
import string

import cherrypy

class CudIndex(object):

    @cherrypy.expose
    def index(self):
        print 'returning index'
        return file('index.html')

class CudConnect(object):
    exposed = True

    def POST(self, server='hey', port='bub'):
        print 'connecting {0} {1}'.format(server,port)
        cherrypy.session['input_string'] = ''

class CudInput(object):
    exposed = True

    def PUT(self, input_string):
        print 'input {0}'.format(input_string)
        if cherrypy.session['input_string']:
            cherrypy.session['input_string'] = cherrypy.session['input_string']+'<br>'+input_string
        else:
            cherrypy.session['input_string'] = input_string

class CudLog(object):
    exposed = True
    def GET(self):
        print 'getting...'
        val=cherrypy.session['input_string']
        cherrypy.session['input_string'] = ''
        return val

class CudKill(object):
    exposed = True
    def PUT(self):
        print 'KILLED!'

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
