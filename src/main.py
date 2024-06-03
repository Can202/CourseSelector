def main():
    csv_reader(path_file="data.csv")

def csv_reader(*, path_file = ""):
    
    file = open(path_file, "r", encoding="utf-8")
    data = file.read()
    print(data)
    file.close()


if __name__ == "__main__":
    main()