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

    bool erase_bonds;

    // Initialize.
    log_init();
    buttons_leds_init(&erase_bonds);
    power_management_init();
    ble_stack_init();
    gap_params_init();
    gatt_init();

	services_init();
	advertising_init();

    conn_params_init();
    peer_manager_init();

    // Start execution.
    NRF_LOG_INFO("Buckler started.");

    start_timers();

    advertising_start(erase_bonds);

    // Enter main loop.
    for (;;)
    {
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
        bool config_light = true;
        if (config_light && should_check_light) {
            should_check_light = false;
            light_state = compare_light();
        }

        if (switch_state) {
            if (switch_state == DIR_UP) {
                less_dim(SOURCE_MANUAL);
            } else {
                more_dim(SOURCE_MANUAL);
            }
        } else if (light_state) {
            if (light_state == LIGHT_UP) {
                less_dim(SOURCE_LIGHT_SENSOR);
            } else if (light_state == LIGHT_DOWN) {
                more_dim(SOURCE_LIGHT_SENSOR);
            }
        } else if (!get_last_switch_state() && (motion_history & 0x7) == 0x7) {
            //turn on
            set_dim_level(0, SOURCE_MOTION);
            restart_motion_timer();
        }
    }
}


