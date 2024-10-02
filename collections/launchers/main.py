from bottle import route, run

@route('/launch')
def launch():
    return "Hello World!"

@route('/simulate')
def simulate():
    return "Simulation of a real Hello World"

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080)