#ifndef TASKS_H
#define TASKS_H

extern volatile bool should_check_motion;
extern volatile bool should_check_manual;
extern volatile bool should_check_light;

void create_timers(void);
void start_timers(void);

#endif
