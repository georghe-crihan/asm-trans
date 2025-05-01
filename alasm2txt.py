#!/usr/bin/env python3

from sys import argv

tokens = [
    "INCLUDE",  # 80
    "INCBIN",  # 81
    "MACRO",  # 82
    "LOCAL",  # 83
    "RLCA",  # 84
    "RRCA",  # 85
    "HALT",  # 86
    "CALL",  # 87 ,
    "PUSH",  # 88 ,
    "RETN",  # 89
    "RETI",  # 8A
    "DJNZ",  # 8B ,
    "OUTI",  # 8C
    "OUTD",  # 8D
    "LDIR",  # 8E
    "CPIR",  # 8F
    "INIR",  # 90
    "OTIR",  # 91
    "LDDR",  # 92
    "CPDR",  # 93
    "INDR",  # 94
    "OTDR",  # 95
    "DD",  # 96
    "DEFB",  # 97
    "DEFW",  # 98
    "DEFS",  # 99 ?
    "DISP",  # 9A
    "ENDM",  # 9B
    "EDUP",  # 9C
    "ENDL",  # 9D
    "MAIN",  # 9E
    "ELSE",  # 9F
    "DISPLAY",  # A0
    "EXA",  # A1
    "DB",  # A2
    "DW",  # A3
    "DS",  # A4
    "NOP",  # A5
    "INC",  # A6 ,
    "DEC",  # A7 ,
    "RLA",  # A8
    "RRA",  # A9
    "DAA",  # AA
    "CPL",  # AB
    "SCF",  # AC
    "CCF",  # AD
    "ADD",  # AE ,
    "ADC",  # AF ,
    "SUB",  # B0 ,
    "SBC",  # B1 ,
    "AND",  # B2 ,
    "XOR",  # B3 ,
    "RET",  # B4 ,
    "POP",  # B5 ,
    "RST",  # B6 ,
    "EXX",  # B7
    "RLC",  # B8 ,
    "RRC",  # B9 ,
    "SLA",  # BA ,
    "SRA",  # BB ,
    "SLI",  # BC ,
    "SRL",  # BD ,
    "BIT",  # BE ,
    "RES",  # BF ,
    "SET",  # C0 ,
    "OUT",  # C1 ,
    "NEG",  # C2
    "RRD",  # C3
    "RLD",  # C4
    "LDI",  # C5
    "CPI",  # C6
    "INI",  # C7
    "LDD",  # C8
    "CPD",  # C9
    "IND",  # CA
    "ORG",  # CB
    "EQU",  # CC
    "ENT",  # CD
    "INF",  # CE
    "DUP",  # CF
    "IFN",  # D0
    "REPEAT",  # D1
    "UNTIL0",  # D2
    "IF0",  # D3
    "LD",  # D4 ,
    "JR",  # D5 ,
    "JP",  # D6 ,
    "OR",  # D7 ,
    "CP",  # D8 ,
    "EX",  # D9 ,
    "DI",  # DA
    "EI",  # DB
    "IN",  # DC ,
    "RL",  # DD ,
    "RR",  # DE ,
    "IM",  # DF
    "ENDIF",  # E0
    "EXD",  # E1
    "JNZ",  # E2
    "JZ",  # E3
    "JNC",  # E4
    "JC",  # E5
    "RUN"  # E6
]

tokens1 = [
    "(BC)",  # 9F
    "(DE)",  # A0
    "(HL)",  # A1
    "(SP)",  # A2
    "(IX)",  # A3
    "(IY)"  # A4
]

tokens2 = [
    "(C)",  # D0
    "(IX",  # D1
    "(IY",  # D2
    "AF'"  # D3
]

tokens3 = [
    "BC",  # E0
    "DE",  # E1
    "HL",  # E2
    "AF",  # E3
    "IX",  # E4
    "IY",  # E5
    "SP",  # E6
    "NZ",  # E7
    "NC",  # E8
    "PO",  # E9
    "PE",  # EA
    "HX",  # EB
    "LX",  # EC
    "HY",  # ED
    "LY",  # EE
    "B",  # EF
    "C",  # F0
    "D",  # F1
    "E",  # F2
    "H",  # F3
    "L",  # F4
    "A",  # F5
    "P",  # F6
    "M",  # F7
    "Z",  # F8
    "R",  # F9
    "I"  # FA
]


def check_signature(f):
    if f[47] == 0xd9:
        loc = 64
    elif f[47 + 17] == 0xd9:  # Hobeta
        loc = 64 + 17
    else:
        return
    return loc


def convert(inbuf, f, insertNumbers=False):
    i = 0
    buflen = len(inbuf)
    currentline = 1

    while buflen > 0:
        comment = False
        quot = False
        rustxt = False
        colon = 0
        k = inbuf[i]
        i += 1
        buflen -= 1

        currentline += 1
        if insertNumbers:
            strerr = "%d:\t" % (currentline,)
            f.append(bytes(strerr, encoding='utf-8'))

        for j in range(1, k):
            if buflen <= 0:
                break
            ch = inbuf[i]
            i += 1
            buflen -= 1

            if ch < 0x80 or comment or quot or rustxt or ch == 0xFF:
                if ch < 0x10:
                    f.append(b' ' * ch)
                elif ch == 0xFF:
                    f.append(b' ')
                elif ch == 0x10:
                    rustxt = True
                else:
                    f.append(b"%c" % ch)
                if chr(ch) == ";":
                    comment = True
                if chr(ch) == "\"":
                    quot = not quot
            else:  # Parse tokens
                colon += 1
                if colon == 1:
                    f.append(b'\t')
                    if 0x80 <= ch <= 0xE6:
                        f.append(bytes(tokens[ch - 0x80], encoding='utf8'))
                        f.append(b'\t')
                    else:
                        strerr = "<col: Unknown token: #%02hX>" % (ch,)
                        f.append(bytes(strerr, encoding='utf8'))
                else:
                    if 0x9F <= ch <= 0xA4:
                        f.append(bytes(tokens1[ch - 0x9F], encoding='utf8'))
                    elif 0xD0 <= ch <= 0xD3:
                        f.append(bytes(tokens2[ch - 0xD0], encoding='utf8'))
                    elif 0xE0 <= ch <= 0xFA:
                        f.append(bytes(tokens3[ch - 0xE0], encoding='utf8'))
                    else:
                        strerr = "<tok: Unknown token: #%02hX>" % (ch,)
                        f.append(bytes(strerr, encoding='utf8'))

        if quot:
            f.append(b'"')

        f.append(b"\n")


def main():
    b = []
    f = open(argv[1], "rb")
    buf = f.read()
    f.close()

    i = check_signature(buf)
    if i is not None:
        with open(argv[2], "wb") as f:
            convert(buf[i:], b)
            f.write(b''.join(b))


main()
