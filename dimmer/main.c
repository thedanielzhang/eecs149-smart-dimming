#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "nrf.h"

const uint8_t out_pin = 3;
const uint32_t zc_int_pin = 2;

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
		NRF_GPIO->OUTCLR = 1 << out_pin;
		NRF_TIMER4->TASKS_STOP = 1;
		NRF_TIMER4->TASKS_CLEAR = 1;
	//compare event 1 fires when we should turn the triac on
	} else if (NRF_TIMER4->EVENTS_COMPARE[1]) {
		NRF_TIMER4->EVENTS_COMPARE[1] = 0;
		NRF_GPIO->OUTSET = 1 << out_pin;

	}
}

int main() {
	//setup the pwm pin for output
	NRF_GPIO->DIR |= 1 << out_pin;
	//turn it on for now
	NRF_GPIO->OUT |= 1 << out_pin;

	//set up a rising edge interrupt on zc_int_pin
	NRF_GPIOTE->CONFIG[0] = (1 << 16) | (zc_int_pin << 8) | (1);
	NRF_GPIOTE->INTENSET |= 1;
	NVIC_EnableIRQ(GPIOTE_IRQn);

	//set up timer to run with prescale of 512, 8 bits, and a compare when
	//it reaches 255, just before the next zero crossing
	NRF_TIMER4->MODE = 0;
	NRF_TIMER4->BITMODE = 1;
	NRF_TIMER4->PRESCALER = 9;
	NRF_TIMER4->CC[0] = 255;
	NRF_TIMER4->CC[1] = 250;
	NRF_TIMER4->INTENSET = (1 << 16) | (1 << 17);
	NVIC_EnableIRQ(TIMER4_IRQn);

	__WFI();
}

//set a new dim level
//dim_level is an 8-bit value, with 0 representing full brightness,
//and 255 representing full darkness
void set_dim_level(uint8_t dim_level) {
	//if full darkness or full brightness,
	//just turn on or off the LED and disable all
	//interrupts
	if (dim_level == 0 || dim_level == 255) {
		NVIC_DisableIRQ(TIMER4_IRQn);
		NVIC_DisableIRQ(GPIOTE_IRQn);
		NRF_TIMER4->TASKS_STOP = 1;
		NRF_TIMER4->TASKS_CLEAR = 1;
		if (dim_level == 0) {
			NRF_GPIO->OUTSET = 1 << out_pin;
		} else {
			NRF_GPIO->OUTCLR = 1 << out_pin;
		}
	//otherwise, set the second compare register to the dim level and enable interrupts
	} else {
		NRF_TIMER4->CC[1] = dim_level;
		NVIC_EnableIRQ(TIMER4_IRQn);
		NVIC_EnableIRQ(GPIOTE_IRQn);
	}
}