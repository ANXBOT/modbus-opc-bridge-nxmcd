"""
Data Bridge - Synchronize Modbus data to OPC UA
"""

import logging
import struct
import time

from src.modbus_client import ModbusClient
from src.opcua_server import OpcUaServer
from src.mapping import load_mapping, get_all_items

logger = logging.getLogger(__name__)


class DataBridge:
    """Bridge between Modbus TCP and OPC UA."""

    def __init__(self, config_path=None):
        self.modbus = ModbusClient()
        self.opcua = OpcUaServer()
        self.mapping = load_mapping(config_path)
        self.items = get_all_items(self.mapping)
        self._running = False

    def setup(self):
        """Set up Modbus client and OPC UA server with mapping."""
        # Setup OPC UA server
        self.opcua.setup()

        # Create OPC UA nodes from mapping
        for item in self.items:
            default_value = False if item["data_type"] == "Bool" else 0
            self.opcua.add_node(
                tag=item["tag"],
                name=item["name"],
                value=default_value,
                data_type=item["data_type"],
            )

        # Connect to Modbus
        self.modbus.connect()

        logger.info(f"Bridge setup complete with {len(self.items)} mapped items")

    def _read_modbus_value(self, item):
        """Read a single value from Modbus.

        Args:
            item: Mapping item dictionary.

        Returns:
            Read value, or None if read failed.
        """
        mb_type = item["modbus_type"]
        address = item["address"]
        count = item.get("count", 1)

        if mb_type == "coil":
            result = self.modbus.read_coils(address, count)
            if result is not None:
                return result[0] if count == 1 else result

        elif mb_type == "discrete_input":
            result = self.modbus.read_discrete_inputs(address, count)
            if result is not None:
                return result[0] if count == 1 else result

        elif mb_type == "holding":
            result = self.modbus.read_holding_registers(address, count)
            if result is not None:
                if count == 1:
                    return result[0]
                elif count == 2 and item["data_type"] == "Float":
                    return self._registers_to_float(result[0], result[1])
                elif count == 2 and item["data_type"] == "Int32":
                    return self._registers_to_int32(result[0], result[1])
                return result

        elif mb_type == "input_register":
            result = self.modbus.read_input_registers(address, count)
            if result is not None:
                if count == 1:
                    return result[0]
                elif count == 2 and item["data_type"] == "Float":
                    return self._registers_to_float(result[0], result[1])
                return result

        return None

    @staticmethod
    def _registers_to_float(reg_high, reg_low):
        """Convert two registers to IEEE 754 float (Big-Endian)."""
        try:
            packed = struct.pack(">HH", reg_high, reg_low)
            return struct.unpack(">f", packed)[0]
        except struct.error:
            return 0.0

    @staticmethod
    def _registers_to_int32(reg_high, reg_low):
        """Convert two registers to 32-bit integer (Big-Endian)."""
        try:
            packed = struct.pack(">HH", reg_high, reg_low)
            return struct.unpack(">i", packed)[0]
        except struct.error:
            return 0

    def sync_once(self):
        """Perform one sync cycle: read all Modbus values and update OPC UA."""
        if not self.modbus.is_connected():
            logger.warning("Modbus not connected, attempting reconnect...")
            if not self.modbus.connect():
                return

        for item in self.items:
            value = self._read_modbus_value(item)
            if value is not None:
                self.opcua.update_node(item["tag"], value)

    def run(self, poll_interval=None):
        """Run the bridge continuously.

        Args:
            poll_interval: Polling interval in seconds. Uses config default if None.
        """
        from config.settings import POLL_INTERVAL

        interval = poll_interval or POLL_INTERVAL
        self._running = True

        logger.info(f"Starting data bridge with {interval}s poll interval")

        try:
            while self._running:
                start = time.time()
                self.sync_once()
                elapsed = time.time() - start
                sleep_time = max(0, interval - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
        except KeyboardInterrupt:
            logger.info("Bridge stopped by user")
        finally:
            self.stop()

    def stop(self):
        """Stop the bridge and clean up."""
        self._running = False
        self.modbus.disconnect()
        self.opcua.stop()
        logger.info("Bridge stopped and resources cleaned up")
