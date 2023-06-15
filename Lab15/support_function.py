def read_file(name_file: str, size_buffer: int):
    file_for_only_read = open(name_file, 'r', encoding="utf8")
    return file_for_only_read.read() if size_buffer <= -1 else file_for_only_read.read()[:size_buffer]


def write_file(name_file: str, message: str, size_buffer: int):
    file_for_only_write = open(name_file, 'w', encoding="utf8")
    if size_buffer <= -1:
        file_for_only_write.write(message)
    else:
        file_for_only_write.write(message[:size_buffer])
