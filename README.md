# AMQPing
Amqping is a simple utility for testing AMQP functions.
it can connect to an amqp instance, post and consume test messages,
count & purge queues.


Ping and cleanup example:
```
   $ amqping myuser mypass myhost ping cleanup
   Succesfully connected to broker at amqp://myhost:5672/
   Created exchange:testexchange and queue:testqueue
   Succesfully posted and consumed a test message
   Removed queue:testqueue and exchange:testexchange
```


 Command chaining example:
```
   $ amqping usr pass host ping mcount post --messages 10000 mcount purge mcount cleanup
   HEAD is now at 27edfa3 Restructured around click
   Succesfully connected to broker at amqp://host:5672/
   Created exchange:testexchange and queue:testqueue
   Succesfully posted and consumed a test message
   There are 0 messages in queue:testqueue
   Posted 10000 messages to exchange:testexchange with routing key:testkey
   There are 10000 messages in queue:testqueue
   Purged messages from queue:testqueue
   There are 0 messages in queue:testqueue
   Removed queue:testqueue and exchange:testexchange
```

Note that general options must be placed at the beginning of the command line
For example:
```
   amqping --vhost /foo user pass host ping
```

Usage:
```
root@rpc-partition:~/amqping# amqping
Usage: amqping [OPTIONS] USER PASSWORD HOST COMMAND1 [ARGS]... [COMMAND2
               [ARGS]...]...

Options:
  --port INTEGER
  --vhost TEXT
  --queue TEXT
  --exchange TEXT
  --routingkey TEXT
  --help             Show this message and exit.

Commands:
  cleanup  Remove test exchange and queue
  mcount   Print message count for specified queue
  ping     Connect to broker, create and delete test...
  post     Post a series of test messgaes
  purge    Purge a queue (remove all messages)
```
