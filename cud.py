import os, os.path
import random
import string

import cherrypy
import telnetlib

import threading

fetch_lock = threading.Lock()

class CudIndex(object):

    @cherrypy.expose
    def index(self):
#         print 'returning index'
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
#         print 'input >>{0}<<'.format(input_string)
        cherrypy.session['server'].write('{0}\n'.format(input_string))

class CudFetchVerb(object):
    exposed = True

    def POST(self, verb_text):
        global fetch_lock
        fetch_lock.acquire()
#        print 'fetching verb {0}'.format(verb_text)
        cherrypy.session['server'].write('@list {0}\n\n;"%%%"\n'.format(verb_text))
        val=''
        val=cherrypy.session['server'].expect(['=> "%%%"'])[2]

        fetch_lock.release()
        
        code = process_verb_code(val)
#        print '\n\n{0}\n\n'.format(code)
        return code
        
class CudProgram(object):
    exposed = True

    def PUT(self, input_verb, input_program):
#         print 'programming...'
        cherrypy.session['server'].write('@program {0}\n'.format(input_verb))
        cherrypy.session['server'].write('{0}\n.\n'.format(input_program))

class CudLog(object):
    exposed = True
    def GET(self):
        if not 'server' in cherrypy.session:
            return ''
            
        global fetch_lock
        fetch_lock.acquire()
        val=''
#         print 'getting...'
        try:
            val=cherrypy.session['server'].read_very_eager()
#             if val:
#                 val = val.replace('\n','<br>') + '\n'
        except EOFError:
#             print 'CLOSED!'
            val = '%%%'
            cherrypy.session['server'].close()
        fetch_lock.release()
        return val

class CudKill(object):
    exposed = True
    def PUT(self):
#         print 'KILLED!'
        cherrypy.session['server'].close()

def process_verb_code(the_code):
    # drop the first line
    lines = the_code.split('\n')
    while len(lines)>1 and lines[0].strip()[0] != '1':
        lines = lines[1:]
    
    newlines=[]
    for line in lines:
        tmp=line.split(':',1)
        if len(tmp) > 1:
            newlines.append(tmp[1])

    new_code = '\n'.join(newlines)
#     print '\n\n'+new_code+'\n\n'
    return new_code

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
        CudFetchVerb(), '/fetchverb',
        {'/': {
                'tools.sessions.on': True,        
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
                }
        }
    )

    cherrypy.tree.mount(
        CudProgram(), '/program',
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

    cherrypy.log.screen = False

    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080
                        })

    cherrypy.engine.start()
    cherrypy.engine.block()
    

