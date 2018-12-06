#ifndef TASKS_H
#define TASKS_H

extern volatile bool should_check_motion;
extern volatile bool should_check_manual;
extern volatile bool should_check_light;
extern volatile bool light_level_changed;

void create_timers(void);
void start_repeating_timers(void);
void start_light_changed_timer(void);

#endif
