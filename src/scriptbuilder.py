from .common import formatHex

class LabelOffset:
    _label = None
    _offset = None

class ScriptBuilder:
    _file_str = None
    _byte_buf = None
    _show_offsets = False
    _byte_start = True
    _byte_offset = 0
    _offsets = []
    _offset_index = 1

    def __init__(self):
        self._file_str = ''
        self._byte_buf = ''
        self._offsets = []
        self._offset_index = 1

        
    def write(self, str = '', args = '', end = '\n'):
        self._file_str = self._file_str + str + end

    def __check_labels__(self, offset):
        for _offset in self._offsets:
            if _offset._offset == offset:
                self._file_str = self._file_str + '[LABEL] ' + _offset._label + '\n'
                
        
    def __flush_bytes__(self):
        if len(self._byte_buf) > 0:
            if self._byte_start and self._show_offsets:
                self._file_str = self._file_str + hex(self._byte_offset) + ': '
            self._file_str = self._file_str + '[BYTES] ' + self._byte_buf + '\n'
            self._byte_buf = ''
        self._byte_start = True

    def write_offset(self, offset, str, label_offset, end = '\n'):
        self.__flush_bytes__()
        target_offset = int.from_bytes(label_offset, byteorder='little')

        jump_offset = LabelOffset()
        jump_offset._offset = offset + target_offset
        jump_offset._label = f"Label{self._offset_index}"

        self._offset_index = self._offset_index + 1

        self._offsets.append(jump_offset)

        if self._show_offsets:
            self._file_str = self._file_str + hex(offset) + ': '

        self._file_str = self._file_str + str + ' ' + jump_offset._label + end

        pass
    
    def write_command(self, offset, str = '', args = None, end = '\n'):
        self.__flush_bytes__()
        self.__check_labels__(offset)
        
        if self._show_offsets:
            self._file_str = self._file_str + hex(offset) + ': '

        self._file_str = self._file_str + str 

        if args != None:
            self._file_str = self._file_str + ' ' + formatHex(args) 

        self._file_str = self._file_str + end 

    def write_byte(self, offset, bytes, args = None, end = ' '):
        if self._byte_start:
            self._byte_offset = offset

        self.__check_labels__(offset)
        
        self._byte_buf = self._byte_buf + formatHex(bytes)

        if args != None:
            self._byte_buf = self._byte_buf + ' ' + formatHex(args) 

        self._byte_buf = self._byte_buf + end 

        self._byte_start = False

    def __str__(self):
        self.__flush_bytes__()
        return self._file_str

    def value(self):
        self.__flush_bytes__()
        return self._file_str     
