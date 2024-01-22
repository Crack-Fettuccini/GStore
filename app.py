import multiprocessing
from GStore.API import app  #keep it here so that the paths are imported properly
from GStore.CeleryTasks import celery
from gunicorn_config import gunicorn_options
from gunicorn.app.base import BaseApplication
#import cryptography #Necessary for adhoc method of creating SSL certificates

def number_of_workers():
  return (multiprocessing.cpu_count() * 2) + 1


def handler_app(environ, start_response):
  response_body = b'Works fine'
  status = '200 OK'

  response_headers = [
      ('Content-Type', 'text/plain'),
  ]

  start_response(status, response_headers)

  return [response_body]


class StandaloneApplication(BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == '__main__':
  StandaloneApplication(app, gunicorn_options).run()
  #app.run(debug=True, host='127.0.0.1', port=8100, ssl_context=('./SSL/server.crt', './SSL/server.key'))#"adhoc")

