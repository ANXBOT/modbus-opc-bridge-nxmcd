"""
Modbus TCP to OPC UA Bridge - Main Entry Point

NXMCD Virtual Debugging Bridge
"""

import logging
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from src.bridge import DataBridge


def setup_logging():
    """Configure logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main():
    """Main entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("=" * 60)
    logger.info("Modbus TCP -> OPC UA Bridge for NXMCD Virtual Debugging")
    logger.info("=" * 60)
    logger.info(f"Modbus TCP: {settings.MODBUS_HOST}:{settings.MODBUS_PORT}")
    logger.info(f"OPC UA:     opc.tcp://{settings.OPC_HOST}:{settings.OPC_PORT}")
    logger.info(f"Poll interval: {settings.POLL_INTERVAL}s")
    logger.info("=" * 60)

    bridge = DataBridge(config_path=settings.MAPPING_CONFIG)

    try:
        bridge.setup()
        bridge.run()
    except Exception as e:
        logger.error(f"Bridge error: {e}", exc_info=True)
        bridge.stop()
        sys.exit(1)


if __name__ == "__main__":
    main()
