
def chunks(iterable, chunk_size):
    chunk = []
    try:
        while True:
            for _ in range(chunk_size):
                chunk.append(next(iterable))
            yield chunk
            chunk = []

    except StopIteration:
        if chunk:
            yield chunk
