#include "stdint.h"
#include "motion-detector.h"
#include "nrf.h"
#include "ac-dimmer.h"

static const uint32_t pir_pin = 4;
static uint8_t motion_detected;

// This is the interrupt handler that fires on a compare event
void TIMER2_IRQHandler(void) {
	NRF_TIMER2->EVENTS_COMPARE[0] = 0;
	set_dim_level(255, SOURCE_MOTION);
	NRF_TIMER2->TASKS_STOP = 1;
	NRF_TIMER2->TASKS_CLEAR = 1;
}

void setup_motion_detector(void) {
	motion_detected = 0;
	//set up pir pin for input
	NRF_GPIO->DIR &= ~(1 << pir_pin);
	NRF_GPIO->PIN_CNF[pir_pin] = 0;
	//set up timer2 to prescale of 9, compare of 18750000
	//that is 10 minutes
	NRF_TIMER2->MODE = 0;
	NRF_TIMER2->BITMODE = 3;
	NRF_TIMER2->PRESCALER = 9;
	NRF_TIMER2->CC[0] = 18750000;
	NRF_TIMER2->INTENSET = (1 << 16);
	NVIC_EnableIRQ(TIMER2_IRQn);
}

uint8_t get_motion_history(void) {
	return motion_detected;
}

uint8_t poll_motion_detector(void) {
	motion_detected = (motion_detected << 1) | ((NRF_GPIO->IN >> pir_pin) & 1);
	return motion_detected;
}

void restart_motion_timer(void) {
	//start timer to turn off lights in 10 minutes
	NRF_TIMER2->TASKS_CLEAR = 1;
	NRF_TIMER2->TASKS_START = 1;
}