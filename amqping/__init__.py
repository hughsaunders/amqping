import argparse
import pika

"""
AMQP test script.
This script takes AMQP connection details and credentials and attempts to connect.
If an AMQP connection is established a success message is printed, otherwise an
eception is printed.
"""

class AMQPing:

    def __init__(self, opts):
        self.opts = opts

    def amqp_connect(self):
        credentials = pika.PlainCredentials(self.opts.user, self.opts.password)
        parameters = pika.ConnectionParameters(credentials=credentials,
                                               virtual_host="/%s"%self.opts.vhost,
                                               host=self.opts.host,
                                               port=self.opts.port)
        self.connection = pika.SelectConnection(parameters, self.on_connected)
        try:
            # Loop so we can communicate with RabbitMQ
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            # Gracefully close the connection
            self.connection.close()
            # Loop until we're fully closed, will stop on its own
            self.connection.ioloop.start()


    def on_connected(self, connection):
        """ Connection callback """
        print "Successfully opened AMQP connection."
        if self.opts.queue:
            channel = self.connection.channel(self.on_open)
        else:
            connection.close()

    def on_open(self, channel):
        print "Channel open"
        self.channel = channel
        self.channel.basic_get(self.on_recv, self.opts.queue)

    def on_recv(self, *args):
        print "Received Message: ",args[3]
        self.connection.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    parser.add_argument('-v', '--vhost', default='', help="Defaults to /")
    parser.add_argument('-H', '--host', default="localhost", help="Defaults to localhost")
    parser.add_argument('-P', '--port', default=5672, type=int, help="Defaults to 5672")
    parser.add_argument('-Q', '--queue', type=str, help="Get a sample message form this"
                "queue")
    options = parser.parse_args()
    amqping = AMQPing(options)
    amqping.amqp_connect()

if __name__ == "__main__":
    main()
