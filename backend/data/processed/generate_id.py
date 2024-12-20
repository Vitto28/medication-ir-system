import hashlib


# Generates an id based on the drug name
# TODO: Implement a more robust id generation algorithm (multiple files may have the same drug name, resulting in the same id)
def generate_id(data):
    m = hashlib.md5()
    # use the drug name to generate the id
    m.update(data["name"].encode())
    my_str = str(int(m.hexdigest(), 16))[0:12]
    return my_str
