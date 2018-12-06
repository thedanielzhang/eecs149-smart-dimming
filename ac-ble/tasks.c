#include <stdbool.h>
#include "nrf.h"
#include "app_timer.h"
#include "nrf_drv_clock.h"

volatile bool should_check_motion;
volatile bool should_check_manual;
volatile bool should_check_light;
volatile bool light_level_changed;

APP_TIMER_DEF(m_motion_checking_id);
APP_TIMER_DEF(m_manual_checking_id);
APP_TIMER_DEF(m_light_checking_id);
APP_TIMER_DEF(m_light_changed_id);

static void lfclk_request(void) {
	uint32_t err_code = nrf_drv_clock_init();
	APP_ERROR_CHECK(err_code);
	nrf_drv_clock_lfclk_request(NULL);
}

static void motion_checking_handler(void *p_context) {
	should_check_motion = true;
}

static void manual_checking_handler(void *p_context) {
	should_check_manual = true;
}

static void light_checking_handler(void *p_context) {
	should_check_light = true;
}

static void light_changed_handler(void *p_context) {
	light_level_changed = true;
}

void create_timers() {
	lfclk_request();
	app_timer_init();

	uint32_t err_code;
	err_code = app_timer_create(&m_motion_checking_id, APP_TIMER_MODE_REPEATED, motion_checking_handler);
	APP_ERROR_CHECK(err_code);
	err_code = app_timer_create(&m_manual_checking_id, APP_TIMER_MODE_REPEATED, manual_checking_handler);
	APP_ERROR_CHECK(err_code);
	err_code = app_timer_create(&m_light_checking_id, APP_TIMER_MODE_REPEATED, light_checking_handler);
	APP_ERROR_CHECK(err_code);
	err_code = app_timer_create(&m_light_changed_id, APP_TIMER_MODE_SINGLE_SHOT, light_changed_handler);
	APP_ERROR_CHECK(err_code);
}

void start_repeating_timers() {
	uint32_t err_code;
	err_code = app_timer_start(m_motion_checking_id, APP_TIMER_TICKS(1000), NULL);
	APP_ERROR_CHECK(err_code);
	err_code = app_timer_start(m_manual_checking_id, APP_TIMER_TICKS(20), NULL);
	APP_ERROR_CHECK(err_code);
	err_code = app_timer_start(m_light_checking_id, APP_TIMER_TICKS(200), NULL);
	APP_ERROR_CHECK(err_code);
}

void start_light_changed_timer() {
	uint32_t err_code;
	err_code = app_timer_stop(m_light_changed_id);
	APP_ERROR_CHECK(err_code);
	err_code = app_timer_start(m_light_changed_id, APP_TIMER_TICKS(5000), NULL);
	APP_ERROR_CHECK(err_code);
}