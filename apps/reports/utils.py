def get_file_content(filename, chunck_size):
    with open(filename) as file:
        while True:
            content = file.read(chunck_size)
            if not content:
                break
            yield content