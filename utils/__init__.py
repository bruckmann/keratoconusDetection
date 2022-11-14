
def format_file_name(person_name: str):
    return person_name.replace(" ", "-") + "-" + str(uuid.uuid4())
