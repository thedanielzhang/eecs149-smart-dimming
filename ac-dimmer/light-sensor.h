#ifndef LIGHT_SENSOR_H
#define LIGHT_SENSOR_H
#include <stdlib.h>
#include <stdint.h>

void setup_light_sensor(void);
void save_lux(void);
float poll_light_sensor(void);
uint8_t compare_light(void);

extern const uint8_t LIGHT_UP;
extern const uint8_t LIGHT_DOWN;

#endif