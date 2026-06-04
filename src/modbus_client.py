"""
Modbus TCP Client - Read data from NXMCD
"""

import logging
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from config import settings

logger = logging.getLogger(__name__)


class ModbusClient:
    """Modbus TCP client for reading from NXMCD."""

    def __init__(self, host=None, port=None, unit_id=None):
        self.host = host or settings.MODBUS_HOST
        self.port = port or settings.MODBUS_PORT
        self.unit_id = unit_id or settings.MODBUS_UNIT_ID
        self.client = None

    def connect(self):
        """Connect to Modbus TCP server."""
        try:
            self.client = ModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=settings.MODBUS_TIMEOUT,
            )
            connected = self.client.connect()
            if connected:
                logger.info(f"Connected to Modbus TCP at {self.host}:{self.port}")
            else:
                logger.error(f"Failed to connect to Modbus TCP at {self.host}:{self.port}")
            return connected
        except Exception as e:
            logger.error(f"Modbus connection error: {e}")
            return False

    def disconnect(self):
        """Disconnect from Modbus TCP server."""
        if self.client:
            self.client.close()
            logger.info("Disconnected from Modbus TCP server")

    def read_coils(self, address, count=1):
        """Read coils (function code 0x01)."""
        try:
            result = self.client.read_coils(
                address=address, count=count, slave=self.unit_id
            )
            if result.isError():
                logger.warning(f"Error reading coils at {address}: {result}")
                return None
            return result.bits[:count]
        except ModbusException as e:
            logger.error(f"Modbus exception reading coils: {e}")
            return None

    def read_discrete_inputs(self, address, count=1):
        """Read discrete inputs (function code 0x02)."""
        try:
            result = self.client.read_discrete_inputs(
                address=address, count=count, slave=self.unit_id
            )
            if result.isError():
                logger.warning(f"Error reading discrete inputs at {address}: {result}")
                return None
            return result.bits[:count]
        except ModbusException as e:
            logger.error(f"Modbus exception reading discrete inputs: {e}")
            return None

    def read_holding_registers(self, address, count=1):
        """Read holding registers (function code 0x03)."""
        try:
            result = self.client.read_holding_registers(
                address=address, count=count, slave=self.unit_id
            )
            if result.isError():
                logger.warning(f"Error reading holding registers at {address}: {result}")
                return None
            return result.registers
        except ModbusException as e:
            logger.error(f"Modbus exception reading holding registers: {e}")
            return None

    def read_input_registers(self, address, count=1):
        """Read input registers (function code 0x04)."""
        try:
            result = self.client.read_input_registers(
                address=address, count=count, slave=self.unit_id
            )
            if result.isError():
                logger.warning(f"Error reading input registers at {address}: {result}")
                return None
            return result.registers
        except ModbusException as e:
            logger.error(f"Modbus exception reading input registers: {e}")
            return None

    def is_connected(self):
        """Check if client is connected."""
        return self.client is not None and self.client.connected
