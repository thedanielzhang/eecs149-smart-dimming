#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include "light-sensor.h"
#include "app_error.h"
#include "nrf.h"
#include "nrf_delay.h"
#include "nrf_log.h"
#include "nrf_log_ctrl.h"
#include "nrf_log_default_backends.h"
#include "nrf_twi_mngr.h"
#include "nrf_serial.h"

#include "buckler.h"
#include "max44009.h"

static float saved_lux;
const uint8_t LIGHT_UP = 1;
const uint8_t LIGHT_DOWN = 2;
const float tol = 30;

NRF_TWI_MNGR_DEF(twi_mngr_instance, 5, 0);

void setup_light_sensor(void) {
  //I2C manager
  ret_code_t error_code = NRF_SUCCESS;

  // initialize i2c master (two wire interface)
  nrf_drv_twi_config_t i2c_config = NRF_DRV_TWI_DEFAULT_CONFIG;
  i2c_config.scl = BUCKLER_SENSORS_SCL;
  i2c_config.sda = BUCKLER_SENSORS_SDA;
  i2c_config.frequency = NRF_TWIM_FREQ_100K;
  error_code = nrf_twi_mngr_init(&twi_mngr_instance, &i2c_config);
  APP_ERROR_CHECK(error_code);

  // initialize MAX44009 driver
  max44009_init(&twi_mngr_instance, 0);
}

float poll_light_sensor(void){
  return max44009_read_lux();
}

void save_lux(void){
  //nrf_delay_ms(500); //if the switch is located close to the light sensor
  saved_lux = poll_light_sensor();
  printf("save_lux: %f \n",saved_lux);
}

uint8_t compare_light(void){
  float lux = poll_light_sensor();
  printf("polled_lux: %f \n",lux);
  if (lux < saved_lux - tol){
    return LIGHT_UP;
  } else if (lux > saved_lux + tol) {
    return LIGHT_DOWN;
  }
  return 0;
}
