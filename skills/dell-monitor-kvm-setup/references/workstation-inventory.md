# Arthur's published workstation inventory

Last consolidated: 10 September 2026.

This reference documents one real multi-computer workstation as a reusable troubleshooting example. It is the authoritative factual copy inside the `dell-monitor-kvm-setup` package. Treat the labels below as part of every fact: a reported or proposed connection is not equivalent to a verified one.

## Topology at a glance

**Arthur-reported topology:** the workstation combines a permanently connected Dell Windows desktop tower with two interchangeable laptop docking positions. A personal MacBook Air, a work-owned MacBook Pro, or a work-owned Lenovo ThinkPad may occupy either laptop position after travel or desk changes. The exact ThinkPad model is unknown.

Do not model this as a fixed cable per laptop or as four simultaneous host connections:

1. **Fixed desktop path — Arthur-reported:** Dell desktop video reaches the Dell U3225QE over DisplayPort. Its USB host path reaches a separate Ugreen USB sharing switch.
2. **Direct laptop path — Arthur-reported:** USB-C connects a laptop directly to the U3225QE Thunderbolt 4 upstream port marked for up to 140 W. Arthur reports video, USB data, and charging. The cable's certification has not been inspected.
3. **Adapter laptop path — Arthur-reported:** A laptop connects through a Ugreen USB-C adapter. The adapter side supplies U3225QE video over HDMI and joins the separate Ugreen USB sharing switch for shared peripheral data. An additional USB-C cable runs from a U3225QE downstream port to this adapter; its exact power/data role remains unverified.

**Arthur-reported topology:** the U3225QE has two host-side USB paths: the direct Thunderbolt laptop and the monitor's USB-C KVM upstream through the Ugreen switch. The Ugreen switch selects either the desktop or the adapter-based laptop path. This explains how the monitor's built-in KVM and the separate USB switch participate without treating every laptop as a dedicated switch input. Actual switching and port mapping have not been independently tested.

## Computers, displays, and adapters

### Installed or available hardware

| Component | Evidence and role |
| --- | --- |
| Dell U3225QE | **Verified model.** Primary 32-inch 4K Thunderbolt hub monitor and central video/USB connection point. Port capabilities were checked against [Dell's U3225QE specification](https://www.dell.com/en-us/shop/dell-ultrasharp-32-4k-thunderbolt-hub-monitor-u3225qe/apd/210-bqhs/monitors-monitor-accessories). |
| Dell P2725DE | **Verified model; Arthur-reported topology.** Portrait secondary display driven through the Wavlink DisplayLink path. |
| Dell P22 display | **Arthur-reported.** Third display on the other Wavlink HDMI output; exact model is unknown. |
| Dell Tower ECT1250 running Windows 11 | **Arthur-reported model.** Permanently connected desktop host. |
| MacBook Air M4 running macOS | **Arthur-reported model.** May use either laptop docking path. |
| Work-owned MacBook Pro | **Arthur-reported.** May use either laptop docking path. Exact generation is not established here. |
| Work-owned Lenovo ThinkPad | **Arthur-reported.** Available for either laptop docking path; exact model and compatibility per path remain unverified. |
| Wavlink DisplayLink adapter | **Detected on Windows; cabling Arthur-reported.** USB-A connects to the U3225QE hub and two HDMI outputs feed the P22 and P2725DE. Exact adapter model is unknown. |
| Ugreen two-computer/four-port USB sharing switch | **Arthur-reported.** Switches shared USB data between the desktop and adapter-based laptop path. Exact model is unknown. |
| Ugreen laptop adapter | **Arthur-reported.** Provides the adapter docking path. Arthur recalls an “8K 30 Hz” product label, but the exact model and actual capabilities are unverified. |

### U3225QE port occupancy

This table combines Dell's published port inventory with Arthur's reported occupancy on 10 September 2026.

| U3225QE connection | Role and dated occupancy |
| --- | --- |
| Four rear USB-A 10 Gbps downstream ports | **Arthur-reported:** all occupied by a Logitech receiver, a backup touchpad receiver of unknown model, the Wavlink DisplayLink adapter, and one unidentified device. The webcam is only a possibility for the unidentified socket, not a confirmed mapping. |
| Front USB-A 10 Gbps downstream port | **Verified capability; unpublished occupancy:** the connected device and its placement are intentionally omitted from the public inventory. |
| Two front USB-C 10 Gbps downstream ports | **Arthur-reported:** one carries a phone/charging cable; the other appeared free by elimination but was not visually verified. |
| Rear USB-C 10 Gbps KVM upstream | **Arthur-reported:** USB-C at the monitor to USB-A at the Ugreen sharing switch. |
| Rear Thunderbolt 4 upstream, up to 140 W | **Arthur-reported:** direct interchangeable laptop docking path for video, data, and charging. |
| Rear Thunderbolt 4 downstream, 15 W | **Arthur-reported:** USB-C cable to the Ugreen laptop adapter; exact use remains unverified. |
| DisplayPort 1.4 input | **Arthur-reported:** video from the Dell desktop. |
| DisplayPort 1.4 output | **Unknown occupancy:** no connected device was reported. |
| HDMI input | **Arthur-reported:** main-display video from the Ugreen adapter docking path; the adapter's exact physical source connector was not inspected. |
| RJ45 2.5 GbE | **Unknown occupancy.** |
| 3.5 mm analog line out | **Unknown occupancy.** |
| AC power inlet | **Arthur-reported:** connected to desk power. Physical power-strip placement is outside this skill. |

The separate Ugreen switch was described as USB-A on its switch-side host connections. The desktop-side cable was finally reported as USB-C at the desktop and USB-A at the switch. A USB-A cable links the Ugreen laptop adapter to the switch. These connector descriptions have not been independently inspected.

## Shared peripherals and switching

- **Arthur-reported:** switching the active host transfers the webcam, Logitech keyboard, and Logitech mouse to that computer.
- Logitech HD Pro Webcam C920 is the identified webcam. The keyboard and mouse models and Logitech receiver type are unknown.
- A rarely used backup touchpad receiver occupies a rear hub port and may be unplugged when another USB-A port is needed. Its exact product name is unknown.
- Laptop placement is changeable; an open raised stand and a closed vertical stand do not imply personal-versus-work ownership or a fixed cable path.
- The workstation also has work-loaned compact Apple keyboard and mouse peripherals available when needed; they are not necessarily connected.
- A Samsung Galaxy S25 FE is available for USB-C charging and Windows Phone Link. A Google Pixel Watch 3 was reported but is not connected to the computer.
- Connectivity uses a TP-Link Wi-Fi router and fiber internet. The exact router model, provider, fiber equipment, and all network identifiers are intentionally absent because they were not established or are not needed for this skill.

The physical location and port mapping of security devices are deliberately excluded from this public inventory.

## Display settings and observations

**Verified on Windows on 10 September 2026:** the portrait P2725DE ran at its observed native 1440 × 2560 resolution and 60 Hz. Scaling changed from 100% to 200%. The U3225QE was observed at 175% scaling.

These are dated settings, not universal recommendations. Preserve native resolution when sharp text is the priority, then adjust scaling and verify the result visually.

## Audio and microphone workflow

### Installed and used

- Sony WH-CH720N headphones are used most often.
- A90 Pro in-ear headphones and LC-dolida sleep/sport headphones were reported; exact models or manufacturers are not fully confirmed.
- Headphone pairs are rotated when one needs charging.
- The Dell desktop relies on headphones in this setup; no usable speaker path was reported.

### Verified Windows state on 10 September 2026

- The C920 microphone was set as the default Windows input for console, multimedia, and communications roles.
- The C920 was assigned as application input for Chrome and the desktop AI chat application used during inspection.
- The Sony capture endpoint was disabled while Sony playback remained enabled and selected as default output.
- Post-change inspection showed the desktop AI application recording through the C920 and playing through the Sony headphones.

This state is not guaranteed after device removal, reinstallation, or application-specific changes. Other headphone microphones were not exhaustively inspected. Preserve the playback route when changing input devices.

### USB audio handover experiment

A Creative BT-W5 had been ordered but was **not installed or tested as of 10 September 2026**. Delivery was expected on 12 September, but arrival was not confirmed in the source record. Connector fit, USB/KVM handover, reconnect time, multipoint behavior, and operating-system output selection therefore remained unverified.

The proposed topology is:

```text
active computer -> shared USB/KVM path -> dedicated USB audio transmitter -> headphones
```

The intended benefit is that one transmitter retains headphone pairing while the KVM changes the active computer. This is a proposal, not a compatibility claim. A general-purpose Bluetooth adapter should not be assumed to provide the same self-contained pairing behavior as a dedicated USB audio transmitter.

A Creative BT-W3X was discussed historically but was not the ordered device. [Creative's BT-W3X product page](https://de.creative.com/p/accessories/creative-bt-w3x) describes it as USB-C and says its USB-C-to-USB-A converter is not included. Do not transfer BT-W3X connector or compatibility assumptions to the BT-W5.

## Troubleshooting evidence and lessons

### Start with the occupied path

Ask which physical path is active: desktop, direct-monitor laptop, or adapter-based laptop. Do not ask only for the laptop name because the laptops move between positions.

Trace each layer separately:

1. main-display video input;
2. USB upstream path and KVM selection;
3. DisplayLink USB path and its two HDMI outputs;
4. power delivery or charging;
5. audio input and output endpoints.

This prevents a working video link from being mistaken for working USB data, or a charging cable from being treated as proven Thunderbolt.

### Preserve uncertainty

- USB-C connector shape does not prove Thunderbolt certification, power direction, data speed, or DisplayPort Alt Mode.
- A monitor port's published capability does not prove that the connected cable or adapter supports it.
- Detection of DisplayLink on one Windows session supports presence, not permanent cross-platform compatibility.
- A switch that transfers keyboard and mouse successfully does not by itself prove seamless Bluetooth-audio handover.

### Historical USB receiver observation

In an earlier desktop configuration, a Logitech receiver behind the tower produced lag and repeated characters; moving it to a front USB port improved behavior. Treat this as historical evidence for interference or placement testing, not proof of the receiver's current socket or of a universal fix.

### Validate changes observably

After rewiring or changing settings, test the actual outcome on every affected host and path. Useful checks include display detection and native resolution, keyboard/mouse/webcam transfer, microphone capture, headphone playback, charging state, and reconnect behavior after a full switch away and back.

## Known gaps

- Exact Wavlink DisplayLink adapter, Ugreen sharing-switch, and Ugreen laptop-adapter models.
- Exact Dell P22, Lenovo ThinkPad, backup touchpad, keyboard, mouse, and receiver models.
- Identity of the fourth rear USB-A device.
- RJ45 and analog line-out occupancy.
- Exact cable certification and the downstream USB-C link's power/data behavior.
- Physical HDMI connector on the adapter docking side.
- BT-W5 installation and KVM handover results.

Resolve gaps through direct inspection, manufacturer documentation for the exact model, and repeatable tests. Record the date and whether each new fact was verified, reported, historical, ordered/untested, or proposed.
