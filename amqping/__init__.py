#!/usr/bin/env python

# Copyright 2015 Hugh Saunders <hugh@wherenow.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# stdlib
import random
import sys

# 3rd party
import click
import pika


def setup_broker_resources(ctx):
    # connect to broker
    try:
        credentials = pika.PlainCredentials(ctx.obj['user'],
                                            ctx.obj['password'])
        parameters = pika.ConnectionParameters(ctx.obj['host'],
                                               ctx.obj['port'],
                                               ctx.obj['vhost'],
                                               credentials)
        connection = pika.BlockingConnection(parameters=parameters)
        channel = connection.channel()
        print ("Succesfully connected to broker at"
               " amqp://%(host)s:%(port)s%(vhost)s"
               % dict(host=ctx.obj['host'],
                      port=ctx.obj['port'],
                      vhost=ctx.obj['vhost']))

        # create resources
        channel.exchange_declare(exchange=ctx.obj['exchange'],
                                 exchange_type=ctx.obj['exchange_type'])
        channel.queue_declare(queue=ctx.obj['queue'])
        channel.queue_bind(queue=ctx.obj['queue'],
                           exchange=ctx.obj['exchange'],
                           routing_key=ctx.obj['routing_key'])
        print ("Created exchange:%(exchange)s and queue:%(q)s"
               % dict(exchange=ctx.obj['exchange'], q=ctx.obj['queue']))
        return channel
    except pika.exceptions.ConnectionClosed:
        print("Cant connect to broker at %(host)s:%(port)s, "
              " are the host and port correct?"
              " Is broker running? Are there any firewalls in the way?"
              % dict(host=ctx.obj['host'], port=ctx.obj['port']))
    except pika.exceptions.ProbableAccessDeniedError:
        print("Got access denied, did you specify the right vhost?")
    except pika.exceptions.ProbableAuthenticationError:
        print("Got Authentication Error, check your username and password")
    except pika.exceptions.ChannelClosed as e:
        print("Exchange type mismatch - exchange already exists but its type"
              " does not match '%(etype)s'. Try specifying --exchangetype."
              " Error details: %(e)s"
              % dict(etype=ctx.obj['exchange_type'], e=e))
    sys.exit(1)


# Cli group stores options and args common to all commands.
@click.group(chain=True)
@click.argument('user')
@click.argument('password')
@click.argument('host')
@click.option('--port', default=5672)
@click.option('--vhost', default='/')
@click.option('--queue', default='testqueue')
@click.option('--exchange', default='testexchange')
@click.option('--routingkey', default='testkey')
@click.option('--exchangetype', default='topic')
@click.pass_context
def cli(ctx,
        user,
        password,
        host,
        port,
        vhost,
        queue,
        exchange,
        routingkey,
        exchangetype):
    ctx.obj['user'] = user
    ctx.obj['password'] = password
    ctx.obj['host'] = host
    ctx.obj['port'] = port
    ctx.obj['vhost'] = vhost
    ctx.obj['queue'] = queue
    ctx.obj['exchange'] = exchange
    ctx.obj['routing_key'] = routingkey
    ctx.obj['exchange_type'] = exchangetype
    ctx.obj['channel'] = setup_broker_resources(ctx)


@cli.command()
@click.option('--messages', help='number of messages to post', default=150)
@click.pass_context
def post(ctx, messages):
    """Post a series of test messgaes"""
    for i in range(messages):
        ctx.obj['channel'].basic_publish(
            exchange=ctx.obj['exchange'],
            routing_key=ctx.obj['routing_key'],
            body='Test Message %s' % i)
    print ("Posted %(messages)s messages to exchange:%(e)s"
           " with routing key:%(key)s"
           % dict(messages=messages,
                  e=ctx.obj['exchange'],
                  key=ctx.obj['routing_key']))


@cli.command()
@click.pass_context
def purge(ctx):
    """Purge a queue (remove all messages)"""
    ctx.obj['channel'].queue_purge(queue=ctx.obj['queue'])
    print("Purged messages from queue:%(q)s" % dict(q=ctx.obj['queue']))


@cli.command()
@click.pass_context
def mcount(ctx):
    """Print message count for specified queue"""
    q = ctx.obj['channel'].queue_declare(ctx.obj['queue'])
    num_messages = q.method.message_count
    print("There are %(messages)s messages in queue:%(q)s"
          % dict(messages=num_messages, q=ctx.obj['queue']))


@cli.command()
@click.pass_context
def ping(ctx):
    """Connect to broker, create and delete test exchange and queue"""

    ping_message = "amqping id %s" % random.randint(0, 10000000)
    channel = ctx.obj['channel']

    # post ping message
    channel.basic_publish(
        exchange=ctx.obj['exchange'],
        routing_key=ctx.obj['routing_key'],
        body=ping_message)

    # consume ping messages
    method_frame, header_frame, body = channel.basic_get(
        queue=ctx.obj['queue'])

    # verify recieved message
    if body == ping_message:
        # ack if we got the message we were expecting
        channel.basic_ack(method_frame.delivery_tag)
        print ("Succesfully posted and consumed a test message")
    else:
        # nack if we got an unexpected message
        channel.basic_nack(method_frame.delivery_tag)
        print ("Posted message '%(sent)s' but received '%(recv)s'"
               % dict(sent=ping_message, recv=body))


@cli.command()
@click.pass_context
def cleanup(ctx):
    """Remove test exchange and queue"""
    channel = ctx.obj['channel']
    channel.queue_delete(queue=ctx.obj['queue'])
    channel.exchange_delete(exchange=ctx.obj['exchange'])
    print("Removed queue:%(q)s and exchange:%(e)s" % dict(q=ctx.obj['queue'],
          e=ctx.obj['exchange']))



cli(obj={})
