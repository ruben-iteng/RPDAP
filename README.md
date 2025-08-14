<div align="center">

# RPDAP

<img height=300 title="3D render" src="./"/>
<br/>

CMSIS-DAP debugger hardware based on a Raspberry Pi RP2040 microcontroller.

[![Version](https://img.shields.io/github/v/tag/ruben-iteng/RPDAP)](https://github.com/ruben-iteng/RPDAP/releases) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ruben-iteng/RPDAP/blob/main/LICENSE) [![Pull requests open](https://img.shields.io/github/issues-pr/ruben-iteng/RPDAP)](https://github.com/ruben-iteng/RPDAP/pulls) [![Issues open](https://img.shields.io/github/issues/ruben-iteng/RPDAP)](https://github.com/ruben-iteng/RPDAP/issues)

</div>

## About

This project contains the hardware designs for a RP2040 based CMSIS-DAP debugger running the [free-dap](https://github.com/ruben-iteng/free-dap) firmware.

This project is build with [atopile](https://atopile.io).

### Features

- USB interface (data and power)
- status LEDs for VCP (Virtual COM Port), DAP, and power.
- level shifted target interface (SWD, UART)
  - 1.2-5.5V target voltage

#### Layouts

There are various layouts available:

| ![No layout](./mock/no_layout.png)  | ![Basic layout](./mock/basic_layout.png)  |
|---------------------------------------|---------------------------------------|
| No layout (for doing you own layout)                   | Basic layout without connectors (for inclusion in your own design/PCBA) |
| ![Stick shaped layout](./mock/stick_shaped_layout.png)  | ![JLink Base Compact compatible layout](./mock/jlink_base_compact_compatible_layout.png)  |
| Stick shaped layout with female USB Type-C connector | JLink Base Compact compatible layout (for use with JLink Base Compact) |

### Firmware

The firmware for the debugger is available in the [free-dap](https://github.com/ruben-iteng/free-dap) repository.
