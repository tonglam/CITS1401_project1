def read_file(csvfile: str) -> list:
    try:
        with open(csvfile, 'r') as f:
            data = f.readlines()
            return data
    except IOError:
        print("Cannot open file:[%s]" % csvfile)
        return None


def save_file_data(read_data: list) -> list:
    data_list = []
    # get csv header
    header = read_data[0].lower().strip().split(',')
    # save to a dictionary list
    for i in range(1, len(read_data)):
        data = read_data[i].lower().strip().split(',')
        # save to a dictionary
        data_dict = dict(zip(header, data))
        data_list.append(data_dict)
    return data_list


def max_min(country: str, country_data_list: list) -> list:
    # filter by year range, founded in the year range of 1981 to 2000 (inclusive)
    max_min_data_list = [x for x in country_data_list if 1981 <= int(x["founded"]) <= 2000]
    if len(max_min_data_list) == 0:
        print("Country:[%s], no organizations founded in the year range of 1981 to 2000 (inclusive)" % country)
        return ["", ""]
    elif len(max_min_data_list) == 1:
        return [max_min_data_list[0]["name"], max_min_data_list[0]["name"]]
    # find max and min number
    max_number = max(max_min_data_list, key=lambda x: int(x["number of employees"]))["number of employees"]
    min_number = min(max_min_data_list, key=lambda x: int(x["number of employees"]))["number of employees"]
    # find max and min name list
    max_name_list = [x["name"] for x in max_min_data_list if x["number of employees"] == max_number]
    min_name_list = [x["name"] for x in max_min_data_list if x["number of employees"] == min_number]
    # sort the list by name
    max_name_list.sort()
    min_name_list.sort()
    return [max_name_list[0], min_name_list[0]]


def standard_deviation(country_data_list: list, data_list: list) -> list:
    # get the salary lists
    country_salary_list = [int(x["median salary"]) for x in country_data_list]
    all_salary_list = [int(x["median salary"]) for x in data_list]
    # calculate the standard deviation, round to 4 decimal places
    # standard deviation must contain at least two values
    country_sd = round(calculate_sd(country_salary_list), 4) if len(country_salary_list) > 1 else 0
    all_sd = round(calculate_sd(all_salary_list), 4) if len(all_salary_list) > 1 else 0
    return [country_sd, all_sd]


def calculate_sd(data_list: list) -> float:
    # calculate length
    length = len(data_list)
    # calculate mean
    mean = sum(data_list) / length
    # calculate standard deviation
    diff_sq_sum = sum([(x - mean) ** 2 for x in data_list])
    return (diff_sq_sum / (length - 1)) ** 0.5


def profit_ratio(country: str, country_data_list: list) -> float:
    # get profits list
    profits_list = [int(x["profits in 2021(million)"]) - int(x["profits in 2020(million)"]) for x in country_data_list]
    if len(profits_list) == 0:
        print("Country:[%s], no profit data from 2020-2021" % country)
        return 0
    # calculate the ratio
    positive = sum([profit for profit in profits_list if profit > 0])
    negative = abs(sum([profit for profit in profits_list if profit < 0]))
    if negative == 0:
        print("Country:[%s], all organizations have made a positive profit from 2020-2021" % country)
        return 0
    # round to 4 decimal places
    return round(positive / negative, 4)


def correlation_coefficient(country: str, country_data_list: list) -> float:
    # only use the organisations which show an increase in profits from 2020 to 2021
    country_valid_data_list = [x for x in country_data_list if
                               int(x["profits in 2021(million)"]) - int(x["profits in 2020(million)"]) > 0]
    if len(country_valid_data_list) == 0 or len(country_valid_data_list) == 1:
        print("Country:[%s], no organisations have an increase in profits from 2020 to 2021" % country)
        return 0
    # get the profits in 2021 list
    profits_2021_list = [int(x["profits in 2021(million)"]) for x in country_valid_data_list]
    # get the median salaries list
    median_salary_list = [int(x["median salary"]) for x in country_valid_data_list]
    # calculate the means
    profits_mean = sum(profits_2021_list) / len(profits_2021_list)
    median_salary_mean = sum(median_salary_list) / len(median_salary_list)
    # calculate the correlation coefficient between profits in 2021 and median salaries
    molecule = sum([(profits_2021_list[i] - profits_mean) * (median_salary_list[i] - median_salary_mean) for i
                    in range(len(country_valid_data_list))])
    denominator = ((sum([(x - profits_mean) ** 2 for x in profits_2021_list]) *
                    sum([(y - median_salary_mean) ** 2 for y in median_salary_list]))
                   ** 0.5)
    # round to 4 decimal places
    return round(molecule / denominator, 4) if denominator != 0 else 0


def main(csvfile: str, country: str) -> tuple:
    # check input params
    if len(csvfile) == 0 or len(country) == 0:
        print("Please input the valid params")
        return ["", ""], [0, 0], 0, 0
    # read file
    read_data = read_file(csvfile)
    if read_data is None or len(read_data) == 0:
        print("Input file:[] is empty or not exists" % csvfile)
        return ["", ""], [0, 0], 0, 0
    # store data to a list and filter by country
    data_list = save_file_data(read_data)
    if len(data_list) == 0:
        print("Input file:[] contains no data" % csvfile)
        return ["", ""], [0, 0], 0, 0
    # data filter by country
    country_data_list = [x for x in data_list if x['country'] == country.lower()]
    # maximum and minimum
    max_min_list = max_min(country, country_data_list)
    # standard deviation
    stdv = standard_deviation(country_data_list, data_list)
    # ratio
    ratio = profit_ratio(country, country_data_list)
    # correlation
    correlation = correlation_coefficient(country, country_data_list)
    return max_min_list, stdv, ratio, correlation
