
def file_filter(file, words: list[str]) -> str:
    if words == []:
        raise ValueError('Empty list')
    words = [word.lower() for word in words]
    if isinstance(file, str):
        with open(file, 'r+') as data:
            for line in data:
                line_list = str.lower(line).split()
                for word in words:
                    if word in line_list:
                        yield line
                        break
    else:
        file.seek(0)
        for line in file:
            line_list = str.lower(line).split()
            for word in words:
                if word in line_list:
                    yield line
                    break
