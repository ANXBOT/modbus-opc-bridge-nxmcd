"""
OPC UA Server - Expose Modbus data as OPC UA nodes
"""

import logging
from opcua import Server

from config import settings

logger = logging.getLogger(__name__)


class OpcUaServer:
    """OPC UA server that exposes Modbus data as nodes."""

    def __init__(self, host=None, port=None):
        self.host = host or settings.OPC_HOST
        self.port = port or settings.OPC_PORT
        self.server = Server()
        self.node_map = {}  # opc_node -> modbus_tag
        self._idx = None

    def setup(self):
        """Initialize OPC UA server and namespace."""
        endpoint = f"opc.tcp://{self.host}:{self.port}/modbus-opc-bridge"
        self.server.set_endpoint(endpoint)
        self.server.set_server_name("NXMCD Modbus-OPC Bridge")

        # Register namespace
        uri = settings.OPC_NAMESPACE
        self._idx = self.server.register_namespace(uri)

        # Get objects node for adding variables
        objects = self.server.get_objects_node()
        self._parent = objects.add_object(self._idx, "ModbusData")

        logger.info(f"OPC UA server configured at {endpoint}")

    def add_node(self, tag, name, value=0, data_type="Int16"):
        """Add a variable node to the OPC UA server.

        Args:
            tag: Unique identifier for this node (used for mapping)
            name: Display name for the OPC UA node
            value: Initial value
            data_type: Data type (Bool, Int16, UInt16, Int32, Float, Double)
        """
        type_map = {
            "Bool": "set_bool",
            "Int16": "set_int16",
            "UInt16": "set_uint16",
            "Int32": "set_int32",
            "Float": "set_float",
            "Double": "set_double",
        }

        node = self._parent.add_variable(self._idx, name, value)

        # Make node writable by clients
        node.set_writable(False)

        self.node_map[tag] = node
        logger.debug(f"Added OPC UA node: {name} (tag={tag}, type={data_type})")
        return node

    def update_node(self, tag, value):
        """Update the value of an OPC UA node.

        Args:
            tag: Node tag identifier
            value: New value to set
        """
        if tag in self.node_map:
            try:
                self.node_map[tag].set_value(value)
            except Exception as e:
                logger.error(f"Error updating node {tag}: {e}")
        else:
            logger.warning(f"Node tag not found: {tag}")

    def start(self):
        """Start the OPC UA server."""
        try:
            self.server.start()
            logger.info(f"OPC UA server started on opc.tcp://{self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to start OPC UA server: {e}")
            raise

    def stop(self):
        """Stop the OPC UA server."""
        try:
            self.server.stop()
            logger.info("OPC UA server stopped")
        except Exception as e:
            logger.error(f"Error stopping OPC UA server: {e}")
