def splitter_of_strings (string):
    string = string.split(" ")
    string = "-".join(string)
    string = string.split(":")
    string = "-".join(string)
    string = string.split(".")
    string = "-".join(string)
    return string