"""
 Created by ldh on 19-11-26
"""
__author__ = "刘大怪"

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3333, debug=app.config['DEBUG'], threaded=False)
