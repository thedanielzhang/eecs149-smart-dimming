# nRF application makefile
PROJECT_NAME = $(shell basename "$(realpath ./)")

# Bluetooth device name
BT_DEVICE_NAME = Buckler

# Configurations
NRF_IC = nrf52832
SDK_VERSION = 15
SOFTDEVICE_MODEL = s132

# Path to base of nRF52-base repo
NRF_BASE_DIR = ../../nrf5x-base/

# Source and header files
APP_HEADER_PATHS += .
APP_SOURCE_PATHS += .
APP_SOURCES = $(notdir $(wildcard ./*.c))

CFLAGS += -DDEVICE_NAME=$(DEVICE_NAME)

# Include board Makefile (if any)
include ./Board.mk
#include ../../boards/buckler_revB/Board.mk

# Include main Makefile
include $(NRF_BASE_DIR)make/AppMakefile.mk
