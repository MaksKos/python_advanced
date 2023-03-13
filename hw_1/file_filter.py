from io import StringIO


def file_filter(file: StringIO, words: list[str]) -> str:
    if words == []:
        raise ValueError('Empty list')
    if file.tell() > 0:
        file.seek(0)

    words = [word.lower() for word in words]
    line = file.readline()
    while line:
        line_list = str.lower(line).split()
        for word in words:
            if word in line_list:
                yield line
                break
        line = file.readline()
