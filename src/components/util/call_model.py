import subprocess


# Calling our model via a .bat script and the python subprocess module
def call_model():
    print('Calling our model')
    return \
        subprocess.Popen("/var/www/FlaskApp/FlaskApp/model_call.bat", shell=False)
