# ESP32-S3 Wireless AI Debugger - Schematic Example

Complete worked example: 28 components (after revision), 5 module boxes, 129-pin net fanout.

## Revision History

- v1: 30 components, 127-pin fanout (initial placement)
- v2: 28 components, 129-pin fanout (R6/R7/R8 removed, J3 2x4P header added,
  SW1/SW2 same-pole nets corrected)

## Module Layout (schematic units = 0.01 inch = 10mil)

Y-axis goes UP. topLeftY = top edge (large Y), height extends DOWN.

| Module | x | topY | w | h | color | Label |
|--------|---|------|---|---|-------|-------|
| USB & 电源 | 50 | 1450 | 620 | 500 | #0066CC | USB & 电源 |
| ESP32-S3 主控 | 750 | 1450 | 700 | 900 | #CC6600 | ESP32-S3 主控 |
| LCD 显示 | 1550 | 1450 | 520 | 700 | #008800 | LCD 显示 |
| 按键 & 接口 | 50 | 700 | 620 | 550 | #880088 | 按键 & 接口 |
| TF 卡存储 | 1550 | 700 | 520 | 550 | #008888 | TF 卡存储 |

```javascript
// Draw module box + label
await eda.sch_PrimitiveRectangle.create(x, topY, w, h, 10, 0, color, "none", 2, null, null);
await eda.sch_PrimitiveText.create(x + w/2, topY - 15, label, 0, color, null, 16, true, false, false, 4);
// NOTE: 4 = CENTER_TOP alignMode (numeric, NOT ESCH_PrimitiveTextAlignMode enum)
```

## Component Placement

28 components placed inside their module boxes (after revision: R6/R7/R8 removed,
J3 2x4P header added, SW1/SW2 same-pole nets corrected):

| Des | Device | Module | x | y |
|-----|--------|--------|---|---|
| J1 | USB-C 16P | USB&Power | 150 | 1250 |
| U3 | USBLC6-2SC6 | USB&Power | 150 | 1050 |
| D1 | SS34 | USB&Power | 350 | 1300 |
| U2 | AMS1117-3.3 | USB&Power | 550 | 1250 |
| R1 | 5.1k (CC1) | USB&Power | 350 | 1150 |
| R2 | 5.1k (CC2) | USB&Power | 450 | 1150 |
| C1 | 10uF (5V filter) | USB&Power | 550 | 1100 |
| C2 | 10uF (3V3 filter) | USB&Power | 550 | 1000 |
| C3 | 100nF (VBUS) | USB&Power | 350 | 1000 |
| C4 | 100nF (5V) | USB&Power | 450 | 1000 |
| U1 | ESP32-S3-WROOM-1 | ESP32 | 1100 | 1000 |
| C5 | 10uF (3V3) | ESP32 | 850 | 1350 |
| C6 | 10uF (3V3) | ESP32 | 950 | 1350 |
| C7 | 100nF (3V3) | ESP32 | 850 | 1250 |
| C8 | 100nF (3V3) | ESP32 | 950 | 1250 |
| R3 | 10k (EN pullup) | ESP32 | 850 | 700 |
| R4 | 10k (BOOT pullup) | ESP32 | 1350 | 700 |
| LCD1 | HS096T01H13 TFT | LCD | 1750 | 1150 |
| Q1 | S8050 (backlight) | LCD | 1950 | 1350 |
| R16 | 22R (LED limit) | LCD | 1950 | 1200 |
| R17 | 1k (base R) | LCD | 1950 | 1050 |
| SW1 | TS-1187A (BOOT) | Button | 200 | 550 |
| SW2 | TS-1187A (RESET) | Button | 450 | 550 |
| R5 | 10k (UART1_RX pullup) | Button | 200 | 350 |
| J3 | HDR2X4 2.54mm (interface) | Button | 550 | 400 |
| J2 | TF-01A | TF Card | 1750 | 450 |
| C9 | 100nF (3V3) | TF Card | 1950 | 600 |
| C10 | 100nF (3V3) | TF Card | 1950 | 500 |

## Net Assignment Table

129 non-NC pins assigned to 35 distinct nets.

### Power nets (31 pins -> createNetFlag "Power")

| Net | Pins |
|-----|------|
| 3V3 | U1:2, U2:2, U2:4, C2:1, C5:1, C6:1, C7:1, C8:1, R3:1, R4:1, LCD1:10, R16:1, J2:4, C9:1, C10:1, R5:1, J3:2, J3:6 |
| 5V | D1:1, U2:3, C1:1, C4:1, J3:1, J3:5 |
| VBUS | J1:A4B9, J1:B4A9, U3:5, D1:2, C3:1 |

### Ground net (37 pins -> createNetFlag "Ground")

All GND pins from: J1 (4 EP + 2 GND), U3:2, U2:1, R1:2, R2:2, C1:2, C2:2, C3:2, C4:2,
U1 (3 GND), C5-C8:2, LCD1:8, LCD1:13, Q1:2, SW1:3, SW1:4, SW2:3, SW2:4, J2 (5 GND), C9:2, C10:2

### Signal nets (61 pins -> createNetPort "BI")

| Net | Pins |
|-----|------|
| USB_DP | J1:A6, J1:B6, U3:3, U3:4, U1:14 (IO20) |
| USB_DM | J1:A7, J1:B7, U3:1, U3:6, U1:13 (IO19) |
| CC1 | J1:A5, R1:1 |
| CC2 | J1:B5, R2:1 |
| EN | U1:3, R3:2, SW2:1, SW2:2 |
| BOOT | U1:27 (IO0), R4:2, SW1:1, SW1:2 |
| UART0_RX | U1:36 |
| UART0_TX | U1:37 |
| UART1_TX | U1:10 (IO17), J3:3, J3:7 |
| UART1_RX | U1:11 (IO18), R5:2, J3:4, J3:8 |
| LCD_SDA | U1:19 (IO11), LCD1:3 |
| LCD_SCL | U1:20 (IO12), LCD1:4 |
| LCD_DC | U1:18 (IO10), LCD1:5 |
| LCD_RST | U1:21 (IO13), LCD1:6 |
| LCD_CS | U1:17 (IO9), LCD1:7 |
| LCD_BLK | U1:22 (IO14), R17:1 |
| LEDA | LCD1:12, R16:2 |
| LEDK | LCD1:11, Q1:3 |
| Q1B | Q1:1, R17:2 |
| TF_CS | U1:7 (IO7), J2:2 |
| TF_MOSI | U1:5 (IO5), J2:3 |
| TF_MISO | U1:6 (IO6), J2:7 |
| TF_CLK | U1:4 (IO4), J2:5 |
| TF_CD | J2:9 |
| GPIO1-GPIO3, GPIO8, GPIO15, GPIO16, GPIO21 | U1 spare IO pins |

### Button Same-Pole Wiring (CRITICAL)

TS-1187A 4-pin tactile buttons have internal symmetry:
- pin1 = pin2 (A = B, same pole)
- pin3 = pin4 (C = D, same pole)

Correct net assignment (same-pole pins share ONE net):

| Button | pin1 | pin2 | pin3 | pin4 |
|--------|------|------|------|------|
| SW1 (BOOT) | BOOT | BOOT | GND | GND |
| SW2 (RESET) | EN | EN | GND | GND |

WRONG (would short BOOT to GND internally): pin1=BOOT, pin2=GND, pin3=BOOT, pin4=GND

## J3 2x4P Header Pin Assignment

2.54mm pitch through-hole header (LCSC C9900013817, footprint CONN-TH_8P-P2.54-V-R2-C4-S2.54):

| Pin | Net | Direction |
|-----|-----|-----------|
| 1 | 5V | Power |
| 2 | 3V3 | Power |
| 3 | UART1_TX | Signal |
| 4 | UART1_RX | Signal |
| 5 | 5V | Power |
| 6 | 3V3 | Power |
| 7 | UART1_TX | Signal |
| 8 | UART1_RX | Signal |

Pins 1-4 and 5-8 mirror each other for flexible connection orientation.

## Pin Fanout Code Pattern

```python
# Flag offset: 10 units in direction of pin rotation
def compute_flag_pos(pinX, pinY, rot):
    rot = int(rot)
    if rot == 0:   return (pinX+10, pinY,   0,   pinX, pinY, pinX+10, pinY)
    if rot == 180: return (pinX-10, pinY,   180, pinX, pinY, pinX-10, pinY)
    if rot == 270: return (pinX,   pinY-10, 270, pinX, pinY, pinX,   pinY-10)
    if rot == 90:  return (pinX,   pinY+10, 90,  pinX, pinY, pinX,   pinY+10)
```

```javascript
// Batch create all flags + wires in one execute call (254 ops ~38s)
for (const e of entries) {
    if (e.flagType === "power")
        await eda.sch_PrimitiveComponent.createNetFlag("Power", e.net, e.fx, e.fy, e.flagRot, false);
    else if (e.flagType === "ground")
        await eda.sch_PrimitiveComponent.createNetFlag("Ground", e.net, e.fx, e.fy, e.flagRot, false);
    else
        await eda.sch_PrimitiveComponent.createNetPort("BI", e.net, e.fx, e.fy, e.flagRot, false);
    await eda.sch_PrimitiveWire.create([e.pinX, e.pinY, e.fx, e.fy], e.net);
}
```

## Modification Workflow (v1 -> v2)

When modifying an existing schematic:

1. **Delete components**: `sch_PrimitiveComponent.delete([pid1, pid2, ...])`
2. **Locate net flags/ports by position**: filter `getAll()` by X/Y proximity to
   deleted component pin locations (flags are 10 units from pin endpoints)
3. **Locate wires by position**: filter `getAll()` by `.line` coordinate proximity
4. **Delete orphaned flags + wires**: `sch_PrimitiveComponent.delete()` and
   `sch_PrimitiveWire.delete()`
5. **Place new components**: `sch_PrimitiveComponent.create()` + async designator
6. **Get new pin positions**: `getAllPinsByPrimitiveId()`
7. **Create new net flags + wires**: same batch pattern as initial fanout

Key: wire objects expose `.line` (array `[x1,y1,x2,y2]`) and `.net` directly.
`getState_Coordinates()` does NOT exist on wires - use `.line`.

## Verification Results (v2)

```
Total objects: 291
  Real components: 28
  Net flags + ports: 129 (31 power + 37 ground + 61 signal)
  Wires: 129
  Rectangles: 5 (module boxes)
  Texts: 5 (module labels)
Designators: C1-C10, D1, J1, J2, J3, LCD1, Q1, R1-R5, R16, R17, SW1, SW2, U1, U2, U3
```
