#include "sdk_config.h"

#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include "nrf_log.h"
#include "nrf_log_ctrl.h"
#include "nrf_log_default_backends.h"

#include "ac-dimmer.h"
#include "motion-detector.h"
#include "manual-switch.h"
#include "tasks.h"
#include "light-sensor.h"
#include "custom-ble.h"
#include "configuration.h"

static uint8_t motion_set_point = 0;

static void log_init(void)
{
    ret_code_t err_code = NRF_LOG_INIT(NULL);
    APP_ERROR_CHECK(err_code);

    NRF_LOG_DEFAULT_BACKENDS_INIT();
}

int main(void)
{
    create_timers();

    setup_dimmer();
    //set_dim_level(100);
    setup_motion_detector();
    setup_manual_switch();
    setup_light_sensor();

    bool erase_bonds = false;

    // Initialize.
    log_init();
    //buttons_leds_init(&erase_bonds);
    //power_management_init();
    ble_stack_init();
    gap_params_init();
    gatt_init();

	services_init();
	advertising_init();

    conn_params_init();
    peer_manager_init();

    start_repeating_timers();

    advertising_start(erase_bonds);

    // Enter main loop.
    while (1) {
        if (light_level_changed) {
            light_level_changed = false;
            uint8_t source = get_current_source();
            if (source != SOURCE_LIGHT_SENSOR) {
                save_lux();
                if (source != SOURCE_MOTION) {
                  motion_set_point = get_dim_level();
                }
            }
            //if it was not changed over bluetooth
            if (source != SOURCE_APP_SLIDER && source != SOURCE_SCHEDULE) {
                update_ble_characteristic();
            }
        }

        uint8_t motion_history = 0;
        if (should_check_motion) {
            should_check_motion = false;
            motion_history = poll_motion_detector();
        }

        uint8_t switch_state = 0;
        if (should_check_manual) {
            should_check_manual = false;
            switch_state = poll_manual_switch();
        }

        uint8_t light_state = 0;
        if (should_check_light) {
            should_check_light = false;
            light_state = compare_light();
        }

        if (switch_state) {
            if (switch_state == DIR_UP) {
                less_dim(SOURCE_MANUAL);
            } else {
                more_dim(SOURCE_MANUAL);
            }
        } else if (motion_tracking_enabled && get_dim_level() == 0xFF && !get_last_switch_state() && (motion_history) == 0xFF) {
            //turn on
            set_dim_level(motion_set_point, SOURCE_MOTION);
            restart_motion_timer();
        } else if (light_tracking_enabled && light_state) {
            if (light_state == LIGHT_UP) {
                less_dim(SOURCE_LIGHT_SENSOR);
            } else if (light_state == LIGHT_DOWN) {
                more_dim(SOURCE_LIGHT_SENSOR);
            }
        }
    }
}
