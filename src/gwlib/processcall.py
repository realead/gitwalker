import subprocess

class ProcessCallError(Exception):
      def __init__(self, message, returncode):
        Exception.__init__(self, message)
        self.returncode=returncode
        


class CallResult:
    def __init__(self, out, err, returncode):
        self.stdout=out
        self.stderr=err
        self.returncode=returncode
        

def execute_process(command, ok_code=[0]): 
    df = subprocess.Popen(command, stdout=subprocess.PIPE,  stderr=subprocess.PIPE)        
    output, err = df.communicate()
    code=df.returncode
    if code not in ok_code:
        raise ProcessCallError("Process returned unexpected code {0}".format(code), code)
    return CallResult(output, err, code)
    
    
