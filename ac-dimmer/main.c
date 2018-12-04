#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "nrf.h"
#include "nrf_delay.h"
#include "app_timer.h"
#include "nrf_drv_clock.h"

#include "ac-dimmer.h"
#include "motion-detector.h"
#include "manual-switch.h"
#include "tasks.h"
#include "light-sensor.h"

int main() {
	create_timers();
	start_timers();

	//setup the dimmer
	setup_dimmer();
	//set_dim_level(100);
	setup_motion_detector();
	setup_manual_switch();
	setup_light_sensor();

	//__WFI();
	while(1) {

		uint8_t motion_history = 0;
		if (should_check_motion) {
			should_check_motion = false;
			motion_history = poll_motion_detector();
		}

		uint8_t switch_state = 0;
		if (should_check_manual) {
			should_check_manual = false;
			switch_state = poll_manual_switch();
		}

		uint8_t light_state = 0;
		bool config_light = true;
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
		} else if (!get_last_switch_state() && (motion_history & 0x7) == 0x7) {
			//turn on
			set_dim_level(0, SOURCE_MOTION);
			restart_motion_timer();
		}

	}
}
