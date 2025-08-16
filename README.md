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
- status LEDs for VCP (Virtual COM Port), DAP status, and power.
- level shifted target interface (SWD, UART)
  - 1.2-5.5V target logic voltage

#### Layouts

There are various layouts and standalone boards available:

| ![Basic layout](./build/builds/rpdap/rpdap.pcba.png)  | ![Stick shaped layout](./build/builds/rpdap_stick/rpdap_stick.pcba.png)  |
|---------------------------------------|---------------------------------------|
| Basic layout without connectors (for inclusion in your own design/PCBA) | Standalone stick shaped layout with female USB Type-C, Cortex-M debug header and 4-pin JST-SH UART connector. All inside a PCB enclosure. |
|  ![RPDAP Compact board](./build/builds/rpdap_compact/rpdap_compact.pcba.png)  | ![JLink Base Compact compatible "footprint"](./build/builds/rpdap_compact_on_board/rpdap_compact_on_board.pcba.png) |
| Standalone RPDAP Compact board (JLink Base Compact compatible board shape) |  JLink Base Compact compatible "footprint" (for using as build-in debugger/programmer) |

### Firmware

The firmware for the debugger is available in the [free-dap](https://github.com/ruben-iteng/free-dap) repository.
Follow this standard RP2040 flashing procedure to flash the firmware.
