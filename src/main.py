def main():
    raw_data = csv_reader(path_file="data.csv")
    data = plain_text_to_array(data=raw_data)

def csv_reader(*, path_file = ""):
    file = open(path_file, "r", encoding="utf-8")
    data = file.read()
    file.close()
    return data

def plain_text_to_array(*, data = ""):
    data_lines = data.split("\n")
    data_splitted = []
    for i in range(len(data_lines)):
        data_splitted.append(data_lines[i].split(","))
    return data_splitted


if __name__ == "__main__":
    main()