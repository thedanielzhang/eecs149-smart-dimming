#ifndef MOTION_DETECTOR_H
#define MOTION_DETECTOR_H
#include <stdlib.h>
#include "stdint.h"
#include "inttypes.h"
/*
 * setup_motion_detector sets up GPIO
 * pin 0.4 for input, and configures TIMER2
 * for a 10-minute timer
*/
void setup_motion_detector(void);

/*
 * poll_motion_detector checks the motion detector's
 * status, and sets the dim level accordingly
*/
uint8_t poll_motion_detector(void);

void restart_motion_timer(void);

extern uint8_t motion_set_point;

#endif
