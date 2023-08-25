import solution as solution

csvfile = "./Organisations.csv"


def main():
    # read file, get all countries
    read_data = solution.read_file(csvfile)
    country_list = list(set([read_data[i].strip().split(',')[3] for i in range(len(read_data)) if i > 0]))
    for country in country_list:
        solution.main(csvfile, country)


if __name__ == "__main__":
    main()
