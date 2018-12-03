#ifndef MOTION_DETECTOR_H
#define MOTION_DETECTOR_H

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
void poll_motion_detector(void);

#endif