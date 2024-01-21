from GStore.API import app  #keep it here so that the paths are imported properly
from GStore.CeleryTasks import celery
#import cryptography #Necessary for adhoc method of creating SSL certificates



if __name__ == '__main__':
  app.run(debug=True, host='127.0.0.1', port=8100, ssl_context=('./SSL/server.crt', './SSL/server.key'))#"adhoc")

