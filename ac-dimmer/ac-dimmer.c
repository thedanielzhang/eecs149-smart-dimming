#include "ac-dimmer.h"
#include <stdlib.h>
#include "nrf.h"
#include "light-sensor.h"

static const uint32_t ac_out_pin = 2;
static const uint32_t zc_int_pin = 5;

static uint8_t current_dim_level;
static uint8_t current_source;

const uint8_t SOURCE_MANUAL = 0x1;
const uint8_t SOURCE_LIGHT_SENSOR = 0x2;
const uint8_t SOURCE_MOTION = 0x4;

static const uint8_t dim_increment = 5;
static const uint8_t dim_increment_light = 20;

static void dim_level_changed(uint8_t source) {
	if (source != SOURCE_LIGHT_SENSOR) {
		save_lux();
	}
	//update bluetooth with new data
}

//set a new dim level
//dim_level is an 8-bit value, with 0 representing full brightness,
//and 255 representing full darkness
void set_dim_level(uint8_t dim_level, uint8_t source) {
	printf("source: %d \n", source);
	//if full darkness or full brightness,
	//just turn on or off the LED and disable all
	//interrupts
	if (dim_level == 0 || dim_level == 255) {
		NVIC_DisableIRQ(TIMER4_IRQn);
		NVIC_DisableIRQ(GPIOTE_IRQn);
		NRF_TIMER4->TASKS_STOP = 1;
		NRF_TIMER4->TASKS_CLEAR = 1;
		if (dim_level == 0) {
			NRF_GPIO->OUTSET = 1 << ac_out_pin;
		} else {
			NRF_GPIO->OUTCLR = 1 << ac_out_pin;
		}
	//otherwise, set the second compare register to the dim level and enable interrupts
	} else {
		NRF_TIMER4->CC[1] = dim_level;
		NVIC_EnableIRQ(TIMER4_IRQn);
		NVIC_EnableIRQ(GPIOTE_IRQn);
	}

	current_dim_level = dim_level;
	printf("current_dim_level: %d \n", current_dim_level);
	current_source = source;
	dim_level_changed(source);
	//start/restart timer to send new dim level
}

uint8_t get_dim_level(void) {
	return current_dim_level;
}

void more_dim(uint8_t source) {
	//printf("more_dim: %d \n", source);
	if (0xFF - current_dim_level < dim_increment) {
		//printf("minned out \n");
		set_dim_level(0xFF, source);
	} else {
			if (source == SOURCE_LIGHT_SENSOR) {
				set_dim_level(current_dim_level + dim_increment_light, source);
			} else {
				set_dim_level(current_dim_level + dim_increment, source);
			}
		}
	}

void less_dim(uint8_t source) {
	//printf("less_dim: %d \n", source);
	if (current_dim_level < dim_increment) {
		//printf("maxxed out \n");
		set_dim_level(0, source);
	} else {
		if (source == SOURCE_LIGHT_SENSOR) {
			set_dim_level(current_dim_level - dim_increment_light, source);
		} else {
			set_dim_level(current_dim_level - dim_increment, source);
		}
	}
}

void setup_dimmer(void) {
	//setup the pwm pin for output
	NRF_GPIO->DIR |= 1 << ac_out_pin;
	//turn it on for now
	NRF_GPIO->OUT |= 1 << ac_out_pin;

	//set up a rising edge interrupt on zc_int_pin
	NRF_GPIOTE->CONFIG[0] = (1 << 16) | (zc_int_pin << 8) | (1);
	NRF_GPIOTE->INTENSET |= 1;

	//set up timer to run with prescale of 512, 8 bits, and a compare when
	//it reaches 255, just before the next zero crossing
	NRF_TIMER4->MODE = 0;
	NRF_TIMER4->BITMODE = 1;
	NRF_TIMER4->PRESCALER = 9;
	NRF_TIMER4->CC[0] = 255;
	NRF_TIMER4->CC[1] = 250;
	NRF_TIMER4->INTENSET = (1 << 16) | (1 << 17);
	set_dim_level(0, SOURCE_MANUAL);
}

// this is the interrupt handler that fires on an interrupt
void GPIOTE_IRQHandler(void) {
    NRF_GPIOTE->EVENTS_IN[0] = 0;
    NRF_TIMER4->TASKS_START = 1;
}

// This is the interrupt handler that fires on a compare event
void TIMER4_IRQHandler(void) {
	//compare event 0 fires just before the next zero crossing
	//we want to ensure the triac is off
	if (NRF_TIMER4->EVENTS_COMPARE[0]) {
		NRF_TIMER4->EVENTS_COMPARE[0] = 0;
		NRF_GPIO->OUTCLR = 1 << ac_out_pin;
		NRF_TIMER4->TASKS_STOP = 1;
		NRF_TIMER4->TASKS_CLEAR = 1;
	//compare event 1 fires when we should turn the triac on
	} else if (NRF_TIMER4->EVENTS_COMPARE[1]) {
		NRF_TIMER4->EVENTS_COMPARE[1] = 0;
		NRF_GPIO->OUTSET = 1 << ac_out_pin;

	}
}
