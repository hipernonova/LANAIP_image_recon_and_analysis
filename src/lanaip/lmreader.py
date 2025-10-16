#!/usr/bin/env python3
"""
lmreader.py

Reads Albira/Albira-like LM files (header + list-mode events).
- Header size: 176 bytes (alignment 4)
- Event formats:
  - Version 5 and earlier: 40-byte block (pair + event1(8) + event2(8) + time(8) + amount(4) + padding)
  - Version 6: 32-byte block (time(8), e1(4), e2(4), amount(4), x1,y1,x2,y2,pair,gate all ushorts)

Usage:
    python lmreader.py file.lm            # auto-detect version
    python lmreader.py file.lm -print     # print first N events (default -n 20)
    python lmreader.py file.lm --v1       # force v1 parsing
    python lmreader.py file.lm --v2       # force v2 parsing
"""

import struct
import argparse
import sys

single_flag = 0x100

header_size = 176  # bytes

# ------------------------
# Header parser
# ------------------------
class lm_header:
    """Representation of the 176-byte header you provided."""
    def __init__(self, raw: bytes):
        if len(raw) < header_size:
            raise ValueError(f"Header too short ({len(raw)} bytes), expected {header_size}")

        # Offsets follow the table you supplied (all little-endian)
        # Note: using latin1 decode keeps bytes 0..255 without errors
        self.identifier = raw[0:16].decode("utf8", errors="ignore").rstrip("\x00")
        self.rawCounts = struct.unpack("<d", raw[16:24])[0]
        self.acqTime = struct.unpack("<d", raw[24:32])[0]
        self.activity = struct.unpack("<d", raw[32:40])[0]
        self.isotope = raw[40:56].decode("utf8", errors="ignore").rstrip("\x00")
        self.detectorSizeX = struct.unpack("<d", raw[56:64])[0]
        self.detectorSizeY = struct.unpack("<d", raw[64:72])[0]
        self.startTime = struct.unpack("<d", raw[72:80])[0]
        self.measurementTime = struct.unpack("<d", raw[80:88])[0]
        self.moduleNumber = struct.unpack("<i", raw[88:92])[0]
        self.ringNumber = struct.unpack("<i", raw[92:96])[0]
        self.ringDistance = struct.unpack("<d", raw[96:104])[0]
        self.detectorDistance = struct.unpack("<d", raw[104:112])[0]
        self.isotopeHalfLife = struct.unpack("<d", raw[112:120])[0]
        # reserved: 32 bytes (120..151)
        self.reserved = raw[120:152]
        # version: 2 bytes (152..153)
        self.version_bytes = raw[152:154]
        # reserved 2 bytes (154..155)
        self.reserved2 = raw[154:156]
        # gatePeriod double (156..163)
        self.gatePeriod = struct.unpack("<d", raw[156:164])[0]
        # reserved 12 bytes at the end (164..175) -> ignored
        self.reserved3 = raw[164:176]

    def is_v2(self):
        """Follow the original C++ detection: v2 only when version[0] == 6."""
        return self.version_bytes[0] > 5# 6

    def version_major(self):
        return self.version_bytes[0]

    def pretty_print(self):
        print("\n===== LM Header =====")
        print(f"Identifier     : {self.identifier}")
        print(f"RawCounts      : {self.rawCounts}")
        print(f"AcqTime (s)    : {self.acqTime}")
        print(f"Activity       : {self.activity}")
        print(f"Isotope        : {self.isotope}")
        print(f"DetectorSizeX  : {self.detectorSizeX}, DetectorSizeY: {self.detectorSizeY}")
        print(f"StartTime      : {self.startTime}")
        print(f"MeasurementTime: {self.measurementTime}")
        print(f"ModuleNumber   : {self.moduleNumber}, RingNumber: {self.ringNumber}")
        print(f"RingDistance   : {self.ringDistance}, DetectorDistance: {self.detectorDistance}")
        print(f"IsotopeHalfLife: {self.isotopeHalfLife}")
        print(f"Version bytes  : ({self.version_bytes[0]}, {self.version_bytes[1]})")
        print(f"GatePeriod     : {self.gatePeriod}")
        print("======================\n")


# ------------------------
# Event parsers
# ------------------------
# v1 (version 5 and previous): 40 bytes with compiler padding so double aligned at offset 24
fmt_v1 = "<H2xHHfHHf4xdf4x"   # totalsize = 40
size_v1 = struct.calcsize(fmt_v1)

# v2 (version 6): 32 bytes: time,d1,d2,amount,x1,y1,x2,y2,pair,gate
fmt_2 = "<dfffHHHHHH"        # totalsize = 32
size_v2 = struct.calcsize(fmt_2)


def parse_event_v1(raw: bytes):
    """Parse a 40-byte v1 coincidence block (returns dict)."""
    if len(raw) != size_v1:
        raise ValueError(f"v1 event must be {size_v1} bytes (got {len(raw)})")
    # Unpack: pair, (pad), e1.x,e1.y,e1.e, e2.x,e2.y,e2.e, pad, time (d), amount (f), pad
    unpacked = struct.unpack(fmt_v1, raw)
    # Mapping from format:
    # unpacked = (pair, e1_x, e1_y, e1_e, e2_x, e2_y, e2_e, time, amount)
    pair = unpacked[0]
    e1_x = unpacked[1]
    e1_y = unpacked[2]
    e1_e = unpacked[3]
    e2_x = unpacked[4]
    e2_y = unpacked[5]
    e2_e = unpacked[6]
    time = unpacked[7]
    amount = unpacked[8]
    return {
        "pair": pair, "time": time, "amount": amount,
        "x1": e1_x, "y1": e1_y, "e1": e1_e,
        "x2": e2_x, "y2": e2_y, "e2": e2_e,
        "gate": 0
    }


def parse_event_v2(raw: bytes):
    """Parse a 32-byte v2 coincidence block (returns dict)."""
    if len(raw) != size_v2:
        raise ValueError(f"v2 event must be {size_v2} bytes (got {len(raw)})")
    unpacked = struct.unpack(fmt_2, raw)
    # unpacked = (time, e1, e2, amount, x1, y1, x2, y2, pair, gate)
    time = unpacked[0]
    e1 = unpacked[1]
    e2 = unpacked[2]
    amount = unpacked[3]
    x1 = unpacked[4]
    y1 = unpacked[5]
    x2 = unpacked[6]
    y2 = unpacked[7]
    pair = unpacked[8]
    gate = unpacked[9]
    return {
        "pair": pair, "time": time, "amount": amount,
        "x1": x1, "y1": y1, "e1": e1,
        "x2": x2, "y2": y2, "e2": e2,
        "gate": gate
    }


# ------------------------
# Reader (mirrors the C++ program)
# ------------------------
def read_lm_file(path, print_packets=False, max_print=None, force_v1=False, force_v2=False):
    """
    Read LM file, print (optionally) packets, and return statistics.

    Returns:
      header (lm_header), stats dict
    """
    # Stats arrays like original C++
    pairNum = [0] * 1024   # counts per pair index
    singleNum = [0] * 128  # counts per module for singles
    totalPairNum = 0
    totalSinglesNum = 0
    totalPairAmount = 0.0
    totalSinglesAmount = 0.0
    maxPairs = 0
    maxMod = 0
    initTime = None
    endTime = None

    with open(path, "rb") as f:
        raw_header = f.read(header_size)
        if len(raw_header) < header_size:
            raise IOError("File too small to contain full header")
        header = lm_header(raw_header)
        header.pretty_print()

        # determine version (same rule as your C++ code)
        if force_v1:
            lmv2 = False
        elif force_v2:
            lmv2 = True
        else:
            lmv2 = header.is_v2()

        print(f"Auto-selected lmv2={lmv2} based on header.version[0] == 6 check (header.version_bytes = {tuple(header.version_bytes)})\n")

        # Print column header if printing packets
        if print_packets:
            if lmv2:
                print("Pair\tAmount\tTime\tX1\tY1\tE1\tX2\tY2\tE2\tG")
                print("======================================================================")
            else:
                print("Pair\tAmount\tTime\tX1\tY1\tE1\tX2\tY2\tE2")
                print("======================================================================")

        total_shown = 0
        rec_no = 0

        # loop over records until EOF
        while True:
            if lmv2:
                raw = f.read(size_v2)
                if not raw or len(raw) < size_v2:
                    break
                ev = parse_event_v2(raw)
            else:
                raw = f.read(size_v1)
                if not raw or len(raw) < size_v1:
                    break
                ev = parse_event_v1(raw)

            rec_no += 1
            pair = int(ev["pair"])
            time = float(ev["time"])
            amount = float(ev["amount"])
            single = (pair & single_flag) != 0

            # Printing each packet (matches format of original)
            if print_packets:
                total_shown += 1
                if single:
                    pair_label = f"S{pair & (~single_flag):04d}"
                else:
                    pair_label = f"{pair:4d}"
                if lmv2:
                    # includes gate
                    print(f"{pair_label}\t{amount:.5f}\t{time:.6g}\t"
                          f"{ev['x1']:03d}\t{ev['y1']:03d}\t{ev['e1']:.2f}\t"
                          f"{ev['x2']:03d}\t{ev['y2']:03d}\t{ev['e2']:.2f}\t{ev['gate']}")
                else:
                    print(f"{pair_label}\t{amount:.5f}\t{time:.6g}\t"
                          f"{ev['x1']:03d}\t{ev['y1']:03d}\t{ev['e1']:.2f}\t"
                          f"{ev['x2']:03d}\t{ev['y2']:03d}\t{ev['e2']:.2f}")

                # optional page break like original C++ every 20 lines (no getch to avoid blocking)
                if max_print and total_shown >= max_print:
                    break

            # statistics
            if not single:
                # normal pair
                if pair > maxPairs:
                    maxPairs = pair
                if pair >= len(pairNum):
                    # skip out-of-bounds like original did
                    # if you need to expand dynamically, change logic here
                    # we mirror the C++ behaviour: warn and skip
                    print(f"Warning: pair index {pair} out of bounds (>= {len(pairNum)}). Skipping stats update.")
                else:
                    pairNum[pair] += 1
                    totalPairNum += 1
                    totalPairAmount += amount
            else:
                pidx = pair & (~single_flag)
                if pidx > maxMod:
                    maxMod = pidx
                if pidx >= len(singleNum):
                    print(f"Warning: single module index {pidx} out of bounds (>= {len(singleNum)}). Skipping stats update.")
                else:
                    singleNum[pidx] += 1
                    totalSinglesNum += 1
                    totalSinglesAmount += amount

            if initTime is None:
                initTime = time
                endTime = time
            else:
                endTime = time

        # finished reading
    # Prepare summary
    stats = {
        "pairNum": pairNum,
        "singleNum": singleNum,
        "totalPairNum": totalPairNum,
        "totalSinglesNum": totalSinglesNum,
        "totalPairAmount": totalPairAmount,
        "totalSinglesAmount": totalSinglesAmount,
        "maxPairs": maxPairs,
        "maxMod": maxMod,
        "initTime": initTime,
        "endTime": endTime,
        "record_count": rec_no
    }
    # Print brief summary (like original C++)
    print("\n\n Brief Data ")
    print("============\n")
    if initTime is None:
        print("No events found.")
    else:
        print(f"Total Time {float(endTime-initTime):.5f}s (from {initTime:.6f} to {endTime:.6f})")
    print(f"Modules founded from 0 to {stats['maxMod']}")
    # pairs breakdown (only non-zero)
    for i in range(stats["maxPairs"] + 1):
        if i < len(pairNum) and pairNum[i] != 0:
            print(f"Pair {i}: {pairNum[i]} coincidences")
    print("Singles founded")
    for i in range(stats["maxMod"] + 1):
        if i < len(singleNum) and singleNum[i] != 0:
            print(f"Detector {i}: {singleNum[i]} singles")
    print(f"Total Pairs Coincidences {stats['totalPairNum']}")
    print(f"Total Pairs Amount {stats['totalPairAmount']:.5f}")
    print(f"Total Singles Num {stats['totalSinglesNum']}")
    print(f"Total Singles Amount {stats['totalSinglesAmount']:.5f}")

    return header, stats

def main():
    p = argparse.ArgumentParser(description="Python LM reader (translation of your C++ lm reader).")
    p.add_argument("filename", help="LM file to read")
    p.add_argument("-print", action="store_true", help="Print packets")
    p.add_argument("--v1", action="store_true", help="Force v1 parser (40 bytes)")
    p.add_argument("--v2", action="store_true", help="Force v2 parser (32 bytes)")
    p.add_argument("-n", "--max_print", type=int, default=None, help="Stop printing after N packets (default none)")
    args = p.parse_args()

    try:
        read_lm_file(args.filename, print_packets=args.print, max_print=args.max_print,
                     force_v1=args.v1, force_v2=args.v2)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
