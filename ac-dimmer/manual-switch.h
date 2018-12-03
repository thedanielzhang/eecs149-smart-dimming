#ifndef MANUAL_SWITCH_H
#define MANUAL_SWITCH_H

#include <stdint.h>

extern const uint8_t DIR_UP;
extern const uint8_t DIR_DOWN;

void setup_manual_switch(void);
uint8_t poll_manual_switch(void);
uint8_t get_last_switch_state(void);

#endif