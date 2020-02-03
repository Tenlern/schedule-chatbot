import chatbot
import cherrypy
import os
import logging


WEBHOOK_HOST = 'reptileserver.herokuapp.com'
WEBHOOK_PORT = int(os.environ.get("PORT", 5000)) # 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % "ff"#(API_TOKEN)


# WebhookServer, process webhook calls
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
           cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = chatbot.telebot.types.Update.de_json(json_string)
            chatbot.bot.process_new_updates([update])
            return 'Hi'
        else:
            raise cherrypy.HTTPError(403)

# Remove webhook, it fails sometimes the set if there is a previous webhook
chatbot.bot.remove_webhook()

# Set webhook
#chatbot.bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Disable CherryPy requests log
access_log = cherrypy.log.access_log
for handler in tuple(access_log.handlers):
    access_log.removeHandler(handler)

# Start cherrypy server
cherrypy.config.update({
    'server.socket_host'    : WEBHOOK_LISTEN,
    'server.socket_port'    : WEBHOOK_PORT,
    'server.ssl_module'     : 'builtin',
    #'server.ssl_certificate': WEBHOOK_SSL_CERT,
    #'server.ssl_private_key': WEBHOOK_SSL_PRIV
})
chatbot.bot.polling()
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})