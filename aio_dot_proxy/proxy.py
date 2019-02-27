import asyncio
import logging
import socket
import ssl

logger = logging.getLogger(__name__)


class DOTProxy:
    """A proxy between a DNS client and a DNS-over-TLS backend server"""

    def __init__(self, server_hostname, server_port):

        self.server_hostname = server_hostname
        self.server_port = server_port

        self._ssl_context = ssl.create_default_context()
        self._ssl_context.verify_mode = ssl.CERT_REQUIRED
        self._ssl_context.check_hostname = True
        self._test_connection()

    def _test_connection(self):
        """Connect to the server and show TLS version and server certificate."""
        with socket.create_connection((self.server_hostname, self.server_port)) as sock:
            with self._ssl_context.wrap_socket(
                    sock, server_hostname=self.server_hostname) as ssock:
                logger.info("Transport version: %s", ssock.version())
                logger.info("Server cert: %s", ssock.getpeercert())

    async def query_backend_server(self, raw_data):
        """Query a DNS-over-TLS backend server with the given data."""
        # open_connection will create a SSL socket and perform the handshake with the
        # backend server.
        reader, writer = await asyncio.open_connection(
            self.server_hostname, self.server_port, ssl=self._ssl_context)
        logger.debug("Quering backend server with %r", raw_data)

        writer.write(raw_data)

        result = await reader.read(1024)
        logger.debug("Received response from backend (%s:%s): %r",
                     self.server_hostname, self.server_port, result)

        logger.debug('Close the connection with backend')
        writer.close()
        await writer.wait_closed()
        return result

    async def handle_dns_query(self, reader, writer):
        """Handle the client requests."""
        data = await reader.read(1024)
        addr = writer.get_extra_info('peername')
        logger.info("New query from %s", addr)
        logger.debug("Query data: %r", data)

        result = await self.query_backend_server(data)

        writer.write(result)
        await writer.drain()

        logger.info("Close the connection with %s", addr)
        writer.close()
