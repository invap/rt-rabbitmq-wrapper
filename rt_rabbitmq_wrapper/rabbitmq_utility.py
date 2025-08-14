# Copyright (c) 2025 Carlos Gustavo Lopez Pombo, clpombo@gmail.com
# Copyright (c) 2025 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Lopez-Pombo-Commercial

from abc import ABC, abstractmethod
import logging
# Create a logger for the RabbitMQ utility component
logger = logging.getLogger(__name__)

import pika
from pika.exceptions import (
    AMQPConnectionError,
    ProbableAuthenticationError,
    ProbableAccessDeniedError,
    IncompatibleProtocolError,
    ChannelClosed,
    ConnectionClosed,
    ChannelWrongStateError,
    AMQPChannelError,
)


class RabbitMQError(Exception):
    def __init__(self):
        super().__init__("RabbitMQ error.")


class RabbitMQ_server_info:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password


class RabbitMQ_server_connection(ABC):
    def __init__(self, server_info, connection_attempts, retry_delay, exchange, exchange_type):
        self.server_info = server_info
        self.connection = None
        self.connection_attempts = connection_attempts
        self.retry_delay = retry_delay
        self.channel = None
        self.exchange = exchange
        self.exchange_type = exchange_type

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    def close(self):
        if self.connection and self.connection.is_open:
            try:
                self.connection.close()
                logger.info(
                    f"Connection to the RabbitMQ server at {self.server_info.host}:{self.server_info.port} closed.")
            except Exception as e:
                logger.error(
                    f"Error closing connection to RabbitMQ server at {self.server_info.host}:{self.server_info.port}: {e}.")

    def _connect_to_server(self):
        # Connection parameters with CLI arguments
        credentials = pika.PlainCredentials(
            self.server_info.user, self.server_info.password
        )
        parameters = pika.ConnectionParameters(
            host=self.server_info.host,
            port=self.server_info.port,
            credentials=credentials,
            connection_attempts=self.connection_attempts,
            retry_delay=self.retry_delay,
            heartbeat=0  # DANGER: no heartbeat because connections might be blocked for unlimited timestamp
        )
        # Setting up the RabbitMQ connection
        try:
            self.connection = pika.BlockingConnection(parameters)
        except IncompatibleProtocolError:
            logger.error(
                f"Protocol version at RabbitMQ server at {self.server_info.host}:{self.server_info.port} error.")
            raise RabbitMQError()
        except ProbableAuthenticationError:
            logger.error(
                f"Authentication to RabbitMQ server at {self.server_info.host}:{self.server_info.port} failed with user {self.server_info.user} and password {self.server_info.password}.")
            raise RabbitMQError()
        except ProbableAccessDeniedError:
            logger.error(
                f"User {self.server_info.user} lacks access permissions to RabbitMQ server at {self.server_info.host}:{self.server_info.port}.")
            raise RabbitMQError()
        except AMQPConnectionError:
            logger.error(
                f"Connection to RabbitMQ server at {self.server_info.host}:{self.server_info.port} failed.")
            raise RabbitMQError()
        except TypeError:
            logger.error(f"Invalid argument types.")
            raise RabbitMQError()
        else:
            logger.info(
                f"Connection to RabbitMQ server at {self.server_info.host}:{self.server_info.port} established.")

    def _connect_to_channel_exchange(self):
        try:
            # Declare RabbitMQ connection channel
            self.channel = self.connection.channel()
            # Declare exchange for the RabbitMQ connection channel
            self.channel.exchange_declare(
                exchange=self.exchange,
                exchange_type=self.exchange_type,
                auto_delete=True,
                durable=False,
            )
        except ChannelClosed:
            logger.error(f"Channel closed.")
            raise RabbitMQError()
        except ConnectionClosed:
            logger.error(f"Unexpected connection loss during operation.")
            raise RabbitMQError()
        except TypeError:
            logger.error(f"Invalid argument types.")
            raise RabbitMQError()
        else:
            logger.info(
                f"Channel and exchange {self.exchange} created at RabbitMQ server at {self.server_info.host}:{self.server_info.port}.")


class RabbitMQ_server_outgoing_connection(RabbitMQ_server_connection):
    def __init__(self, server_info, connection_attempts, retry_delay, exchange, exchange_type):
        super().__init__(server_info, connection_attempts, retry_delay, exchange, exchange_type)

    def connect(self):
        try:
            self._connect_to_server()
        except RabbitMQError:
            logger.error(f"RabbitMQ server connection setup error.")
            raise RabbitMQError()
        try:
            self._connect_to_channel_exchange()
        except RabbitMQError:
            logger.error(f"RabbitMQ exchange setup error.")
            raise RabbitMQError()

    def publish_message(self, body='', properties=None):
        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key='',
                body=body,
                properties=properties,
            )
        except AMQPConnectionError:  # Raised if the connection is closed or lost during the operation.
            logger.error(f"Connection closed or lost during message publishing.")
            raise RabbitMQError()
        except ChannelClosed:  # Subclass of AMQPChannelError: Triggered if RabbitMQ closes the channel mid - operation(e.g., due to an error).
            logger.error(f"Channel closed during message publishing.")
            raise RabbitMQError()
        except AMQPChannelError:  # Raised if the channel is closed or invalid when calling basic_publish.
            logger.error(f"Channel is closed or invalid when calling basic_publish.")
            raise RabbitMQError()
        except TypeError:  # Raised for invalid arguments(e.g., non - string queue name, empty queue name).
            logger.error(f"Invalid argument type.")
            raise RabbitMQError()
        except ValueError:
            logger.error(f"Invalid argument value.")
            raise RabbitMQError()


class RabbitMQ_server_incoming_connection(RabbitMQ_server_connection):
    def __init__(self, server_info, connection_attempts, retry_delay, exchange, exchange_type):
        super().__init__(server_info, connection_attempts, retry_delay, exchange, exchange_type)
        self.queue_name = None

    def connect(self):
        try:
            self._connect_to_server()
        except RabbitMQError:
            logger.error(f"RabbitMQ server connection setup error.")
            raise RabbitMQError()
        try:
            self._connect_to_channel_exchange()
        except RabbitMQError:
            logger.error(f"RabbitMQ exchange setup error.")
            raise RabbitMQError()
        try:
            self._declare_queue()
        except RabbitMQError:
            logger.error(f"RabbitMQ queue setup error.")
            raise RabbitMQError()

    def get_message(self):
        try:
            method, properties, body = self.channel.basic_get(
                queue=self.queue_name, auto_ack=False
            )
        except AMQPConnectionError:  # Raised if the connection is closed or lost during the operation.
            logger.error(f"Connection closed or lost during message reception.")
            raise RabbitMQError()
        except ChannelClosed:  # Subclass of AMQPChannelError: Triggered if RabbitMQ closes the channel mid - operation(e.g., due to an error).
            logger.error(f"Channel closed during message reception.")
            raise RabbitMQError()
        except ChannelWrongStateError:  # Occurs if the channel is in an unusable state(e.g., recovering).
            logger.error(f"Channel is in an unusable state.")
            raise RabbitMQError()
        except AMQPChannelError:  # Raised if the channel is closed or invalid when calling basic_get.
            logger.error(f"Channel is closed or invalid when calling basic_get.")
            raise RabbitMQError()
        except TypeError:  # Raised for invalid arguments(e.g., non - string queue name, empty queue name).
            logger.error(f"Invalid argument type.")
            raise RabbitMQError()
        except ValueError:
            logger.error(f"Invalid argument value.")
            raise RabbitMQError()
        else:
            return method, properties, body

    def ack_message(self, delivery_tag):
        try:
            self.channel.basic_ack(delivery_tag)
        except AMQPConnectionError:  # Raised if the connection is closed or lost during acknowledgement.
            logger.error(f"Connection closed or lost during acknowledgement.")
            raise RabbitMQError()
        except ChannelClosed:  # Raised if: The channel is closed or invalid, RabbitMQ closes the channel due to an error(e.g., invalid delivery_tag)
            logger.error(f"Channel closed during acknowledgement.")
            raise RabbitMQError()
        except AMQPChannelError:
            logger.error(f"Channel is closed or invalid when calling basic_ack.")
            raise RabbitMQError()
        except TypeError:  # Raised if arguments have invalid types(e.g., delivery_tag is a string).
            logger.error(f"Invalid argument type.")
            raise RabbitMQError()
        except ValueError:  # Raised if the delivery_tag is: Negative, Zero, A non-integer value
            logger.error(f"Invalid argument value.")
            raise RabbitMQError()

    def _declare_queue(self):
        # Declare queue
        try:
            result = self.channel.queue_declare(
                queue="", exclusive=True, durable=False  # Let RabbitMQ generate unique name
            )
            self.queue_name = result.method.queue
        except ChannelClosed:
            logger.error(f"Channel closed.")
            raise RabbitMQError()
        except ConnectionClosed:
            logger.error(f"Unexpected connection loss during operation.")
            raise RabbitMQError()
        except TypeError:
            logger.error(f"Invalid argument types.")
            raise RabbitMQError()
        # Bind queue
        try:
            self.channel.queue_bind(
                exchange=self.exchange,
                queue=self.queue_name,
                routing_key='',
            )
        except ChannelClosed:
            logger.error(f"Binding violates server rules.")
            raise RabbitMQError()
        except ConnectionClosed:
            logger.error(f"Connection lost during binding operation.")
            raise RabbitMQError()
        except ValueError:
            logger.error(f"Missing required arguments.")
            raise RabbitMQError()
        except TypeError:
            logger.error(f"Invalid argument types.")
            raise RabbitMQError()
        logger.info(
            f"Queue {self.queue_name} created and bound to exchange {self.exchange} at RabbitMQ server at {self.server_info.host}:{self.server_info.port}."
        )
