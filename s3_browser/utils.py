import shutil


def print_grid(data):
    """
    Print a list of strings in a grid according to the terminal size
    """
    largest = 0
    for e in data:
        largest = max(len(e), largest)

    # Add spacing
    largest += 1

    w = shutil.get_terminal_size().columns
    num_cols = int(w / largest)

    # Give up if we can't fit the data into columns anyway
    if num_cols <= 1:
        for e in data:
            print(e)

        return

    # Pad the strings to all be the same length, and divide into columns
    padded = [e.ljust(largest) for e in data]
    col_size = int(len(data) / num_cols)
    groups = [col_size] * num_cols

    # Account for remainder: first x columns need to be longer
    for i in range(len(data) % num_cols):
        groups[i] += 1

    output = [''] * groups[0]
    i = 0
    for g in groups:
        for j in range(g):
            output[j] += padded[i]
            i += 1

    for line in output:
        print(line)


def print_dict(data, indent_level=0):
    """Pretty-print a dict full of key-value metadata pairs"""
    indent = '  ' * indent_level

    def _format_key(k):
        return '{}{}{: <40}{}'.format(
            indent, '\x1b[36m', k + ':', '\x1b[0m'
        )

    for k, v in sorted(data.items()):
        if not isinstance(v, dict):
            print('{}{}'.format(_format_key(k), v))
        else:
            print(_format_key(k))
            print_dict(v, indent_level=indent_level + 1)


def strip_s3_metadata(data):
    """Strip s3 metadata down to the useful stuff"""
    metadata = data.get('Metadata', {})
    http_head = data.get('ResponseMetadata', {}).get('HTTPHeaders', {})

    return {
        'Content-Length': http_head.get('content-length'),
        'Content-Type': http_head.get('content-type'),
        'Last-Modified': http_head.get('last-modified'),
        'Metadata': metadata
    }
