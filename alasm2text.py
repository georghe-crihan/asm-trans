#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Original author: (c) CityAceE
Source taken from:
https://zx-pk.ru/printthread.php?t=33565&pp=20

"""

import sys


def get_file_trd(filedata_trd, file_number_trd):
    begin = file_number_trd * 16
    if file_number_trd > 127 or not filedata_trd[begin]:
        return None, None, None
    else:
        file_name_trd = filedata_trd[begin + 0:begin + 8].decode().replace("\\", " ").strip()
        if (31 < filedata_trd[begin + 9] < 128) and (31 < filedata_trd[begin + 10] < 128):
            file_ext_trd = filedata_trd[begin + 8:begin + 11].decode().strip()
        else:
            file_ext_trd = chr(filedata_trd[begin + 8])
        file_body_trd = bytearray()
        for file_byte_number in range(filedata_trd[begin + 12] * 256 + filedata_trd[begin + 11]):
            file_body_trd.append(filedata_trd[(filedata_trd[begin + 15] * 16 + filedata_trd[begin + 14]) * 256 +
                                              file_byte_number])
        return file_name_trd, file_ext_trd, file_body_trd


def get_file_scl(filedata_scl, file_number_scl):
    if file_number_scl >= filedata_scl[8]:
        return None, None, None
    begin_name = file_number_scl * 14 + 9
    file_name_scl = filedata_scl[begin_name + 0:begin_name + 8].decode().strip()
    if (31 < filedata_scl[begin_name + 9] < 128) and (31 < filedata_scl[begin_name + 10] < 128):
        file_ext_scl = filedata_scl[begin_name + 8:begin_name + 11].decode().strip()
    else:
        file_ext_scl = chr(filedata_scl[begin_name + 8])
    sectors = 0
    next_file = 9
    for i in range(file_number_scl):
        sectors += filedata_scl[next_file + 13]
        next_file += 14
    file_body_scl = bytearray()
    for file_byte_number in range(filedata_scl[begin_name + 12] * 256 + filedata_scl[begin_name + 11]):
        file_body_scl.append(filedata_scl[filedata_scl[8] * 14 + 9 + sectors * 256 + file_byte_number])
    return file_name_scl, file_ext_scl, file_body_scl


def get_file_raw(filedata_raw, file_number_raw):
    if file_number_raw:
        return None, None, None
    else:
        file_name_raw = filename.split('.')
        del file_name_raw[-1]
        file_name_raw = '.'.join(file_name_raw)
        return file_name_raw, extension, filedata_raw


def get_file_hobeta(filedata_hobeta, file_number_hobeta):
    if file_number_hobeta:
        return None, None, None
    else:
        file_lenght = filedata_hobeta[11] + filedata_hobeta[12] * 256
        return filedata_hobeta[0:8].decode().strip(), chr(filedata_hobeta[8]), filedata_hobeta[17:17 + file_lenght]


def asm2text(databytes):
    asm_name = databytes[0:8].decode().replace("/", " ").strip()
    asm_code = ';Alasm filename: {0}.H\n'.format(asm_name).encode()

    mnemtkn = {
                0x80: "INCLUDE", 0x81: "INCBIN", 0x82: "MACRO", 0x83: "LOCAL", 0x84: "RLCA", 0x85: "RRCA", 0x86: "HALT",
                0x87: "CALL", 0x88: "PUSH", 0x89: "RETN", 0x8A: "RETI", 0x8B: "DJNZ", 0x8C: "OUTI", 0x8D: "OUTD",
                0x8E: "LDIR", 0x8F: "CPIR", 0x90: "INIR", 0x91: "OTIR", 0x92: "LDDR", 0x93: "CPDR", 0x94: "INDR",
                0x95: "OTDR", 0x96: "DD", 0x97: "DEFB", 0x98: "DEFW", 0x99: "DEFS", 0x9A: "DISP", 0x9B: "ENDM",
                0x9C: "EDUP", 0x9D: "ENDL", 0x9E: "MAIN", 0x9F: "ELSE", 0xA0: "DISPLAY", 0xA1: "EXA", 0xA2: "DB",
                0xA3: "DW", 0xA4: "DS", 0xA5: "NOP", 0xA6: "INC", 0xA7: "DEC", 0xA8: "RLA", 0xA9: "RRA", 0xAA: "DAA",
                0xAB: "CPL", 0xAC: "SCF", 0xAD: "CCF", 0xAE: "ADD", 0xAF: "ADC", 0xB0: "SUB", 0xB1: "SBC", 0xB2: "AND",
                0xB3: "XOR", 0xB4: "RET", 0xB5: "POP", 0xB6: "RST", 0xB7: "EXX", 0xB8: "RLC", 0xB9: "RRC", 0xBA: "SLA",
                0xBB: "SRA", 0xBC: "SLI", 0xBD: "SRL", 0xBE: "BIT", 0xBF: "RES", 0xC0: "SET", 0xC1: "OUT", 0xC2: "NEG",
                0xC3: "RRD", 0xC4: "RLD", 0xC5: "LDI", 0xC6: "CPI", 0xC7: "INI", 0xC8: "LDD", 0xC9: "CPD", 0xCA: "IND",
                0xCB: "ORG", 0xCC: "EQU", 0xCD: "ENT", 0xCE: "INF", 0xCF: "DUP", 0xD0: "IFN", 0xD1: "REPEAT",
                0xD2: "UNTIL", 0xD3: "IF", 0xD4: "LD", 0xD5: "JR", 0xD6: "JP", 0xD7: "OR", 0xD8: "CP", 0xD9: "EX",
                0xDA: "DI", 0xDB: "EI", 0xDC: "IN", 0xDD: "RL", 0xDE: "RR", 0xDF: "IM", 0xE0: "ENDIF",
                0xE1: "EXD", 0xE2: "JNZ", 0xE3: "JZ", 0xE4: "JNC", 0xE5: "JC", 0xE6: "RUN"
                }

    regstkn = {
                0x9F: "(BC)", 0xA0: "(DE)", 0xA1: "(HL)", 0xA2: "(SP)", 0xA3: "(IX)", 0xA4: "(IY)", 0xA5: " ",
                0xA6: " ", 0xA7: " ", 0xA8: " ", 0xA9: " ", 0xAA: " ", 0xAB: " ", 0xAC: " ", 0xAD: " ", 0xAE: " ",
                0xAF: " ", 0xB0: " ", 0xB1: " ", 0xB2: " ", 0xB3: " ", 0xB4: " ", 0xB5: " ", 0xB6: " ", 0xB7: " ",
                0xB8: " ", 0xB9: " ", 0xBA: " ", 0xBB: " ", 0xBC: " ", 0xBD: " ", 0xBE: " ", 0xBF: " ", 0xC0: " ",
                0xC1: " ", 0xC2: " ", 0xC3: " ", 0xC4: " ", 0xC5: " ", 0xC6: " ", 0xC7: " ", 0xC8: " ", 0xC9: " ",
                0xCA: " ", 0xCB: " ", 0xCC: " ", 0xCD: " ", 0xCE: " ", 0xCF: " ", 0xD0: "(C)", 0xD1: "(IX", 0xD2: "(IY",
                0xD3: "AF'", 0xD4: " ",0xD5: " ", 0xD6: " ",  0xD7: " ", 0xD8: " ", 0xD9: " ", 0xDA: " ", 0xDB: " ",
                0xDC: " ", 0xDD: " ", 0xDE: " ", 0xDF: " ", 0xE0: "BC", 0xE1: "DE", 0xE2: "HL", 0xE3: "AF", 0xE4: "IX",
                0xE5: "IY", 0xE6: "SP", 0xE7: "NZ", 0xE8: "NC", 0xE9: "PO", 0xEA: "PE", 0xEB: "HX", 0xEC: "LX",
                0xED: "HY", 0xEE: "LY", 0xEF: "B", 0xF0: "C", 0xF1: "D", 0xF2: "E", 0xF3: "H", 0xF4: "L", 0xF5: "A",
                0xF6: "P", 0xF7: "M", 0xF8: "Z", 0xF9: "R", 0xFA: "I"
                }

    counter = 0x40  # Начало ассемблерного текста после заголовка
    while True:
        # Обработка одной строки
        # Сброс всех переключателей
        rus = False
        comment = False
        quote = False
        mnem = False
        len_string = 0
        for current_byte in range(counter + 1, counter + databytes[counter]):
            if databytes[current_byte] != 0xff:
                # Обработка переключателей внутри строки
                if databytes[current_byte] == 0x22:
                    quote = not quote
                elif databytes[current_byte] == 0x3b:
                    comment = True
                elif databytes[current_byte] == 0x10:
                    rus = True
                # Генерация символов внутри строки согласно переключателям
                if databytes[current_byte] in range(0x01, 0x10):
                    asm_code += b' ' * databytes[current_byte]
                    len_string += databytes[current_byte]

                elif databytes[current_byte] in range(0x20, 0x80):
                    asm_code += bytes([databytes[current_byte]])
                    len_string += 1

                elif (databytes[current_byte] in range(0x9f, 0xfb)) and (not rus and not comment and not quote) \
                        and mnem:
                    for letter in regstkn[databytes[current_byte]]:
                        asm_code += letter.encode()
                        len_string += 1

                elif (databytes[current_byte] in range(0x80, 0xe1)) and (not rus and not comment and not quote) \
                        and not mnem:
                    if not len_string or (len_string and asm_code[-1] != 0x20):
                        tab_step = 8 - (len_string - (len_string // 8) * 8)
                        if not tab_step:
                            tab_step = 8
                        asm_code += b' ' * tab_step
                        len_string += tab_step

                    for letter in mnemtkn[databytes[current_byte]]:
                        asm_code += letter.encode()
                        len_string += 1

                    asm_code += b' '
                    len_string += 1
                    mnem = True

                elif (databytes[current_byte] in range(0x80, 0x100)) and (rus or comment or quote):
                    asm_code += bytes([databytes[current_byte]])
                    len_string += 1

        asm_code += b'\n'
        # Следующая строка и проверка на конец текста
        counter += databytes[counter]
        if not databytes[counter]:
            break
    return asm_name, asm_code


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        extension = filename.split('.')[-1].lower()
        if extension == 'scl' or extension == 'trd' or extension == 'h' or extension.startswith('$'):
            with open(filename, "rb") as f:
                file_bytes = bytearray(f.read())
            if extension.startswith('$'):
                extension = '$'
            convert = {'scl': get_file_scl, 'trd': get_file_trd, 'h': get_file_raw, '$': get_file_hobeta}

            for file_number in range(128):
                file_name, file_ext, file_body = convert[extension](file_bytes, file_number)
                if not file_name:
                    break
                else:
                    if 'h' == file_ext.lower() and chr(file_body[8]) == 'H' \
                            and file_body[0x28:0x30] == bytes([0xF3, 0x76, 0xC7, 0xDD, 0xFD, 0xED, 0xB0, 0xD9]):
                        alasm_name, alasm_text = asm2text(bytes(file_body))
                        with open('{0:03}_{1}.asm'.format(file_number, alasm_name), "wb") as f:
                            f.write(alasm_text)
    else:
        print('Usage: python3 alasm2text.py filename.(trd|scl|$h|H)')
