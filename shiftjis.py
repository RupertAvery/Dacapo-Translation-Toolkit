text = '96 B2 82 CC 8F AD 8F 97'
byte_sequence_2 = bytes.fromhex(text)
decoded_string_2 = byte_sequence_2.decode('shift_jis')
print(decoded_string_2)
