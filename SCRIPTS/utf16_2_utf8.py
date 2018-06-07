

# with open("../PUBMED_DATA/pubmedNdrugs_2.txt", 'rb') as source_file:
#   with open("../PUBMED_DATA/pubmedNdrugs_2.1.txt", 'w+b') as dest_file:
#     contents = source_file.read()
#     dest_file.write(contents.decode('utf-16').encode('utf-8'))

    # Open both input and output streams.
input = open("../PUBMED_DATA/pubmedNdrugs_2.txt", "rt", encoding="utf-16")
output = open("../PUBMED_DATA/pubmedNdrugs_2.1.txt", "wt", encoding="utf-8")

# Stream chunks of unicode data.
with input, output:
    while True:
        # Read a chunk of data.
        chunk = input.read(4096)
        if not chunk:
            break
        # Remove vertical tabs.
        chunk = chunk.replace("\u000B", "")
        # Write the chunk of data.
        output.write(chunk)
