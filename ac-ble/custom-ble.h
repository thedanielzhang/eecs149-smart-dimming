#ifndef CUSTOM_BLE_H
#define CUSTOM_BLE_H
#include <stdlib.h>
#include <stdbool.h>
void timers_init(void);
void buttons_leds_init(bool *erase_bonds);
void power_management_init(void);
void ble_stack_init(void);
void gap_params_init(void);
void gatt_init(void);

void services_init(void);
void advertising_init(void);

void conn_params_init(void);
void peer_manager_init(void);

void application_timers_start(void);

void advertising_start(bool erase_bonds);

void idle_state_handle(void);

void update_ble_characteristic(void);

#endif