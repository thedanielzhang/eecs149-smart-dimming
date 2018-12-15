AC Dimmer Code
===================

This code is to be flashed to the Buckler NRF52 Dev Board. It performs sensor polling and local decisions. It also implements BLE on the NRF52 (advertisments), and implements the two smart features: motion detection and light tracking. It is modular, with the main file calling many other child files. For instance, the timers and polling are established in the tasks.c file. Each sensor has its own drivers, as well. The BLE code, based on Staff Code, also has its own dedicated files. 
