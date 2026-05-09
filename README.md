# TEASR

Repository for the paper "Do You 'Relay' Want to Give Me Away? – Forensic Cues of Smart Relays and Their IoT Companion Apps" with the source code for the *Tool for Evidence Acquisition from Smart Relays* (TEASR). The paper is available at https://doi.org/10.1016/j.fsidi.2024.301810. TEASR is designed to support forensic data acquisition from smart relays by enabling automated and repeatable extraction of forensic artifacts from firmware dumps, companion app data, network traffic captures, and vendor cloud APIs.

## Repo Structure

The folder `teasr` contains the source code for TEASR. The main script `teasr.py` provides four commands corresponding to the four data sources analyzed in the paper: `firmware`, `app`, `remote`, and `network`. The library modules in `teasrlib` implement the analysis logic for each data source, including vendor-specific cloud connectors for eWeLink, meross, Shelly, and Tuya.

```
teasr
├─ teasr.py
└─ teasrlib
   ├─ cloud_ewelink.py
   ├─ cloud_meross.py
   ├─ cloud_shelly.py
   ├─ cloud_tuya.py
   ├─ functions_db.py
   ├─ functions_external.py
   ├─ functions_helper.py
   ├─ functions_os.py
   ├─ relay_companion_app.py
   ├─ relay_firmware.py
   ├─ relay_network.py
   └─ relay_remote.py
```

## Usage

TEASR is executed via the `teasr.py` script and provides four subcommands. Each subcommand produces a `summary.json` output file containing the identified forensic artifacts.

### firmware

Analyzes a firmware dump or a directory of firmware dumps and extracts forensic artifacts such as strings, JSON fragments, and files.

```
python3 teasr.py firmware (-f fw_file | -d fw_dir) [-p prefix] [-t table_file]
```

| Argument | Description |
|----------|-------------|
| `-f fw_file` | Absolute path of the firmware dump file |
| `-d fw_dir` | Absolute path of a directory containing multiple firmware dumps |
| `-p prefix` | Prefix for output files (optional) |
| `-t table_file` | Absolute path of an optional partition table in CSV format (optional) |

### app

Performs a forensic examination of the persistent data of a companion app.

```
python3 teasr.py app -a dir -o path [-i id]
```

| Argument | Description |
|----------|-------------|
| `-a dir` | Path of the app data directory |
| `-o path` | Output path for the log and output files |
| `-i id` | App ID, if the directory has been renamed (optional) |

### remote

Calls the device list from the vendor cloud API for the given user credentials and extracts remote artifacts.

```
python3 teasr.py remote -v vendor -c mail pw -o path
```

| Argument | Description |
|----------|-------------|
| `-v vendor` | Vendor cloud to query (possible values: `shelly`, `ewelink`, `meross`, `tuya`) |
| `-c mail pw` | Cloud credentials (mail and password; for Tuya: ID and key) |
| `-o path` | Output path for the log and output files |

### network

Analyzes a network traffic capture file in PCAP format for forensically relevant traces.

```
python3 teasr.py network -f file -o path [-k keyfile] [--ip ip_filter]
```

| Argument | Description |
|----------|-------------|
| `-f file` | Absolute path of the network traffic PCAP file |
| `-o path` | Output path for the log and output files |
| `-k keyfile` | Absolute path of an SSL key log file for TLS decryption (optional) |
| `--ip ip_filter` | IP address of the device to filter for (optional) |

## Paper Tables

### Table 1: Overview of Analyzed Smart Relays

Overview of the 16 smart relay models analyzed with details regarding their SoCs, UART accessibility, the tool used for firmware extraction, and whether a firmware dump was obtained and whether it was encrypted.

| R | Model | Vendor | SoC | Chip Type | UART | Tool | FW Dump | FW Enc. |
|---|-------|--------|-----|-----------|------|------|:-------:|:-------:|
| R₁ | Shelly 1 | Shelly | ESP8266EX | RISC | ● | esptool | ● | ○ |
| R₂ | Shelly Plus 1 | Shelly | ESP32 U4WD | RISC | ● | esptool | ● | ○ |
| R₃ | Shelly Plus 1PM | Shelly | ESP32 U4WD | RISC | ● | esptool | ● | ○ |
| R₄ | Shelly Plus 2PM | Shelly | ESP32 U4WD | RISC | ● | esptool | ● | ○ |
| R₅ | Shelly Plus i4 | Shelly | ESP32 U4WD | RISC | ● | esptool | ● | ○ |
| R₆ | RR500W | LoraTap | BK7231T | ARMv7E-M | ●ᵃ | bk7231tools | ● | ● |
| R₇ | RR620W | LoraTap | BK7231D | ARMv7E-M | ●ᵃ | bk7231tools | ● | ● |
| R₈ | MSS710 | meross | RTL8710CM | ARMv8-M | ●ᵇ | – | ○ | – |
| R₉ | MSS810 | Meross | RTL8710CM | ARMv8-M | ●ᵇ | – | ○ | – |
| R₁₀ | BASICR2 | Sonoff | ESP8285N08 | RISC | ●ᵃ | esptool | ● | ○ |
| R₁₁ | MINIR2 | Sonoff | ESP8285N08 | RISC | ●ᵃ | esptool | ● | ○ |
| R₁₂ | SS-8839-03 | eMylo | BL2028N | ARM9E | ●ᵃ | bk7231tools | ● | ● |
| R₁₃ | EWB1CH-D1 | Newgoal | BL602L20 | RISC-V | ●ᵃ | – | ○ | – |
| R₁₄ | QS-WIFI-S06-16A | Maxcio | BK7231N | ARMv7E-M | ●ᵇ | bk7231tools | ● | ● |
| R₁₅ | MS-105 | MoesGo | BK7231N | ARMv7E-M | ●ᵇ | bk7231tools | ● | ● |
| R₁₆ | MINI Smart Mesh | SIUES | TG7220B | ARMv6-M | ●ᵃ | – | ○ | – |

**Legend:**
- UART: ● accessible, ●ᵃ accessible after teardown, ●ᵇ accessible after desoldering
- FW Dump / FW Enc.: ● yes, ○ no, – not applicable

---

### Table 2: Overview of Companion Apps

Overview of the six companion apps analyzed, their Android application IDs, and the smart relays they support.

| A# | Companion App | Android Application ID | Supported Relays |
|----|---------------|------------------------|------------------|
| A₁ | eWeLink – Smart Home | com.coolkit | R₁₀, R₁₁, R₁₃ |
| A₂ | Maxcio | com.maxcio.smart | R₁₄ |
| A₃ | meross | com.meross.meross | R₈, R₉ |
| A₄ | Shelly Smart Control | cloud.shelly.smartcontrol | R₁, R₂, R₃, R₄, R₅ |
| A₅ | Smart Life – Smart Living | com.tuya.smartlife | R₆, R₇, R₁₂, R₁₄, R₁₅, R₁₆ |
| A₆ | Tuya Smart | com.tuya.smart | R₆, R₇, R₁₂, R₁₄, R₁₅, R₁₆ |
