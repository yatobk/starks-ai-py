from api.routes import app
#import sys
#import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#from lib.utils.envSchema import EnvConfig
if __name__ == "__main__":
    #EnvConfig()
    app.run(debug=True)
