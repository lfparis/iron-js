import os
import subprocess

cwd = os.path.dirname(__file__)
parent = os.path.dirname


def subprocess_wrapper(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    proc_stdout, errmsg = process.communicate()
    return process, proc_stdout, errmsg


def run(app=None, port=None, endpoint=''):
    # start local server
    local_server = subprocess.Popen(['python', '-m', 'http.server', str(port)], shell=True, cwd=app)

    # locate python 35
    python_path = os.path.join(parent(parent(parent(cwd))), "Lib", "Python35", "python.exe")

    # launch app with python subprocess at http://localhost:port/#/endpoint
    script_path = os.path.join(cwd, 'launch_browser.py')
    process, out, error = subprocess_wrapper('{python} {script} {port} {endpoint}'.format(python=python_path, script=script_path, port=str(port), endpoint=endpoint))

    # after app close, kill local server
    # TODO this is not actually closing the local server
    local_server.terminate()
    
    # app was exited and will return results from sub process
    return process, out, error