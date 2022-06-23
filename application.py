from App import app
import os

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    # os.environ['FLASK_ENV'] = 'production'
    app.run(host='0.0.0.0',port=8000)
