#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "nrf.h"
#include "nrf_delay.h"
#include "app_timer.h"
#include "nrf_drv_clock.h"
#include "nrf_log.h"
#include "nrf_log_ctrl.h"
#include "nrf_log_default_backends.h"

#include "ac-dimmer.h"
#include "motion-detector.h"
#include "manual-switch.h"
#include "tasks.h"
#include "light-sensor.h"

int main() {

	// initialize RTT library
  ret_code_t error_code = NRF_LOG_INIT(NULL);
  APP_ERROR_CHECK(error_code);
  NRF_LOG_DEFAULT_BACKENDS_INIT();

	create_timers();
	start_timers();

	//setup the dimmer
  setup_light_sensor();
	setup_dimmer();
	setup_motion_detector();
	setup_manual_switch();

	//__WFI();
	while(1) {

		uint8_t motion_history = 0;
		uint8_t motion_dim_set = 180; // READ FROM BLE
		if (should_check_motion) {
			should_check_motion = false;
			motion_history = poll_motion_detector();
			printf("motion_history: %X \n", motion_history);
		}

		uint8_t switch_state = 0;
		if (should_check_manual) {
			should_check_manual = false;
			switch_state = poll_manual_switch();
		}

		uint8_t light_state = 0;
		bool config_light = true; // READ FROM BLE
		if (config_light && should_check_light) {
			should_check_light = false;
			light_state = compare_light();
		}

		if (switch_state) {
			if (switch_state == DIR_UP) {
				less_dim(SOURCE_MANUAL);
			} else {
				more_dim(SOURCE_MANUAL);
			}
		} else if (light_state) {
			if (light_state == LIGHT_UP) {
				less_dim(SOURCE_LIGHT_SENSOR);
			} else if (light_state == LIGHT_DOWN) {
				more_dim(SOURCE_LIGHT_SENSOR);
			}
		} else if (!get_last_switch_state() && (motion_history) == 0xFF) {
			//turn on
			set_dim_level(motion_dim_set, SOURCE_MOTION);
			restart_motion_timer();
		}
		nrf_delay_ms(10);
	}
}
