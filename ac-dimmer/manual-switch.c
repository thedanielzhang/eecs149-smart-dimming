#include "manual-switch.h"
#include <stdint.h>
#include "nrf.h"
#include "ac-dimmer.h"

static const uint32_t switch_up_pin = 31;
static const uint32_t switch_down_pin = 30;

const uint8_t DIR_UP = 1;
const uint8_t DIR_DOWN = 2;

static uint8_t last_direction;


void setup_manual_switch(void) {
	//set up switch pins for input with internal pullup

	NRF_GPIO->DIR &= ~(1 << switch_up_pin);
	NRF_GPIO->PIN_CNF[switch_up_pin] = 3 << 2;

	NRF_GPIO->DIR &= ~(1 << switch_down_pin);
	NRF_GPIO->PIN_CNF[switch_down_pin] = 3 << 2;

}

uint8_t get_last_switch_state(void) {
	return last_direction;
}

uint8_t poll_manual_switch(void) {
	last_direction = 0;
	if (((NRF_GPIO->IN >> switch_down_pin) & 1) == 0) {
		last_direction = DIR_DOWN;
	} else if (((NRF_GPIO->IN >> switch_up_pin) & 1) == 0) {
		last_direction = DIR_UP;
	}
	return last_direction;
}
