# nRF application makefile
PROJECT_NAME = $(shell basename "$(realpath ./)")

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
APP_SOURCES += $(NRF_BASE_DIR)sdk/nrf5_sdk_15.0.0/integration/nrfx/legacy/nrf_drv_clock.c
APP_SOURCES += $(NRF_BASE_DIR)sdk/nrf5_sdk_15.0.0/modules/nrfx/drivers/src/nrfx_timer.c
APP_SOURCES += $(NRF_BASE_DIR)sdk/nrf5_sdk_15.0.0/modules/nrfx/drivers/src/nrfx_clock.c
APP_SOURCES += $(NRF_BASE_DIR)sdk/nrf5_sdk_15.0.0/components/libraries/timer/app_timer.c
APP_SOURCES += $(NRF_BASE_DIR)sdk/nrf5_sdk_15.0.0/components/libraries/util/app_util_platform.c

# Include board Makefile (if any)
include ./Board.mk

# Include main Makefile
include $(NRF_BASE_DIR)make/AppMakefile.mk
