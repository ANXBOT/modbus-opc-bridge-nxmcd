"""
Modbus TCP to OPC UA Bridge - Configuration
"""

import os

# Modbus TCP Settings (NXMCD)
MODBUS_HOST = os.getenv("MODBUS_HOST", "127.0.0.1")
MODBUS_PORT = int(os.getenv("MODBUS_PORT", "502"))
MODBUS_UNIT_ID = int(os.getenv("MODBUS_UNIT_ID", "1"))
MODBUS_TIMEOUT = int(os.getenv("MODBUS_TIMEOUT", "5"))
MODBUS_RECONNECT_DELAY = int(os.getenv("MODBUS_RECONNECT_DELAY", "3"))

# OPC UA Server Settings
OPC_HOST = os.getenv("OPC_HOST", "0.0.0.0")
OPC_PORT = int(os.getenv("OPC_PORT", "4840"))
OPC_NAMESPACE = os.getenv("OPC_NAMESPACE", "http://nxmcd.modbus.opc.bridge")

# Data Sync Settings
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "0.5"))

# Mapping config file
MAPPING_CONFIG = os.getenv("MAPPING_CONFIG", "config/mapping.yaml")
