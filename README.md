## Changelog

### [2026-04-01] – Initial Assembly and Hardware Testing
- Assembled the Freenove 4WD smart car chassis and installed all four wheels.
- Set up and successfully tested the Raspberry Pi camera module.
- Installed and configured the Discord application for communication and testing.

### [2026-04-01] – Motor Testing Blocked by Hardware Fault
- Attempted to run motor and servo tests using the Freenove test scripts.
- Encountered consistent I²C timeout errors during motor and servo initialization.
- Performed extensive diagnostics and troubleshooting.
- Determined that the issue is **not related to software or code**.
- Identified a hardware fault on the Raspberry Pi: **GPIO3 (I²C SCL) is broken and stuck LOW**, preventing I²C communication with the motor/servo controller.
- Motor and servo testing cannot proceed until a functioning Raspberry Pi is used.


### [2026-04-01] – Networking
- Raspberry Pi IP address (current network): **192.168.162.246**

#### [2026-04-08] - Error
error code [ WARN:0@1.471] global cap_gstreamer.cpp:1777 open OpenCV | GStreamer warning: Cannot query video position: status=0, value=-1, duration=-1


