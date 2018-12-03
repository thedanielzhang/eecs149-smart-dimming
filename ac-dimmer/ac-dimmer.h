#ifndef AC_DIMMER_H
#define AC_DIMMER_H

#include <stdint.h>

/*
 * set_dim_level controls how dim the light is
 * a dim_level of 255 represents complete darkness,
 * and a dim level of 0 represents full brightness.
*/
void set_dim_level(uint8_t dim_level);

/*
 * setup_dimmer sets up an interrupt on GPIO pin 0.5,
 * a PWM output on GPIO pin 0.2, configures TIMER4
 * to control the PWM, and sets the output to full brightness
*/
void setup_dimmer(void);

#endif
