import os
from route_config import *


app.debug = True
host = os.environ.get('IP', '0.0.0.0')
port = int(os.environ.get('PORT', 55677))
if __name__ == '__main__':
    app.run(host=host, port=port)


