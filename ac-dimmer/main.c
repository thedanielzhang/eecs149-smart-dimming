#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "nrf.h"
#include "nrf_delay.h"
#include "ac-dimmer.h"
#include "motion-detector.h"

int main() {
	//setup the dimmer
	setup_dimmer();
	//turn off the light
	set_dim_level(255);

	setup_motion_detector();
	
	while(1) {
		poll_motion_detector();
		nrf_delay_ms(1000);
	}
}

