amqping
=======

Simple script for testing if an AMQP server is up and credentials are valid.

## Options
```bash
user@chefserver2:~# python amqping.py --help
usage: amqping.py [-h] [-u USER] [-p PASSWORD] [-v VHOST] [-H HOST] [-P PORT]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER
  -p PASSWORD, --password PASSWORD
  -v VHOST, --vhost VHOST
  -H HOST, --host HOST  Defaults to localhost
  -P PORT, --port PORT  Defaults to 5672
```

## Examples
```bash
user@chefserver2:~# python amqping.py -u chef -v chef -p $CHEF_RMQ_PW
Successfully opened AMQP connection.

user@chefserver2:~# python amqping.py -u chef -v chef -p incorrect_password
No handlers could be found for logger "pika.adapters.base_connection"
Traceback (most recent call last):
  File "amqping.py", line 44, in <module>
    main()
  File "amqping.py", line 19, in main
    amqp_connect(options.user, options.password, options.vhost, options.host, options.port)
  File "amqping.py", line 30, in amqp_connect
    connection.ioloop.start()
  File "/usr/local/lib/python2.7/dist-packages/pika/adapters/select_connection.py", line 136, in start
    self.poller.start()
  File "/usr/local/lib/python2.7/dist-packages/pika/adapters/select_connection.py", line 424, in start
    self.poll()
  File "/usr/local/lib/python2.7/dist-packages/pika/adapters/select_connection.py", line 479, in poll
    self._handler(fileno, event, write_only=write_only)
  File "/usr/local/lib/python2.7/dist-packages/pika/adapters/base_connection.py", line 302, in _handle_events
    self._handle_read()
  File "/usr/local/lib/python2.7/dist-packages/pika/adapters/base_connection.py", line 323, in _handle_read
    return self._handle_disconnect()
  File "/usr/local/lib/python2.7/dist-packages/pika/adapters/base_connection.py", line 231, in _handle_disconnect
    self._adapter_disconnect()
  File "/usr/local/lib/python2.7/dist-packages/pika/adapters/base_connection.py", line 122, in _adapter_disconnect
    self._check_state_on_disconnect()
  File "/usr/local/lib/python2.7/dist-packages/pika/adapters/base_connection.py", line 138, in _check_state_on_disconnect
    raise exceptions.ProbableAuthenticationError
pika.exceptions.ProbableAuthenticationError
```
