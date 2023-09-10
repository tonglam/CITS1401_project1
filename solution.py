def read_file(csvfile):
    try:
        with open(csvfile, 'r') as f:
            # read file by lines
            data = f.readlines()
            return data
    except IOError:
        return None


def save_file_data(read_data):
    data_list = []
    # get csv header
    header = read_data[0].strip().split(',')
    # save to a dictionary list
    for i in range(1, len(read_data)):
        data = read_data[i].strip().split(',')
        # save to a dictionary
        data_dict = dict(zip(header, data))
        data_list.append(data_dict)
    return data_list


def filter_country_data(country, data_list):
    # filter by country
    return [x for x in data_list if x['Country'].upper() == country.upper()]


def max_min(country_data_list):
    # filter by year range, founded in the year range of 1981 to 2000 (inclusive)
    max_min_data_list = [x for x in country_data_list if 1981 < int(x["Founded"]) <= 2000]
    if len(max_min_data_list) == 0:
        return ["", ""]
    elif len(max_min_data_list) == 1:
        return [max_min_data_list[0]["Name"], max_min_data_list[0]["Name"]]
    # find max and min number
    max_number = max(max_min_data_list, key=lambda x: int(x["Number of employees"]))["Number of employees"]
    min_number = min(max_min_data_list, key=lambda x: int(x["Number of employees"]))["Number of employees"]
    # find max and min name list
    max_name_list = [x["Name"] for x in max_min_data_list if x["Number of employees"] == max_number]
    min_name_list = [x["Name"] for x in max_min_data_list if x["Number of employees"] == min_number]
    # sort the list by name
    max_name_list.sort()
    min_name_list.sort()
    return [max_name_list[0], min_name_list[0]]


def standard_deviation(country_data_list, data_list):
    # get the salary lists
    country_salary_list = [int(x["Median Salary"]) for x in country_data_list]
    all_salary_list = [int(x["Median Salary"]) for x in data_list]
    # calculate the standard deviation, round to 4 decimal places
    # standard deviation must contain at least two values
    country_sd = round(calculate_sd(country_salary_list), 4) if len(country_salary_list) > 1 else 0
    all_sd = round(calculate_sd(all_salary_list), 4) if len(all_salary_list) > 1 else 0
    return [country_sd, all_sd]


def calculate_sd(data_list):
    # calculate length
    length = len(data_list)
    # calculate mean
    mean = sum(data_list) / length
    # calculate standard deviation
    diff_sq_sum = sum([(x - mean) ** 2 for x in data_list])
    return (diff_sq_sum / (length - 1)) ** 0.5


def profit_ratio(country_data_list):
    # get profits list
    profits_list = [int(x["Profits in 2021(Million)"]) - int(x["Profits in 2020(Million)"]) for x in country_data_list]
    if len(profits_list) == 0:
        return 0
    # calculate the ratio
    positive = sum([profit for profit in profits_list if profit > 0])
    negative = abs(sum([profit for profit in profits_list if profit < 0]))
    # round to 4 decimal places
    return round(positive / negative, 4) if negative != 0 else 0


def correlation_coefficient(country_data_list):
    # only use the organisations which show an increase in profits from 2020 to 2021
    country_valid_data_list = [x for x in country_data_list if
                               int(x["Profits in 2021(Million)"]) - int(x["Profits in 2020(Million)"]) > 0]
    if len(country_valid_data_list) == 0 or len(country_valid_data_list) == 1:
        return 0
    # get the profits in 2021 list
    profits_2021_list = [int(x["Profits in 2021(Million)"]) for x in country_valid_data_list]
    # get the median salaries list
    median_salary_list = [int(x["Median Salary"]) for x in country_valid_data_list]
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


def main(csvfile, country):
    # check input params
    if len(csvfile) == 0 or len(country) == 0:
        return ["", ""], [0, 0], 0, 0
    # read file
    read_data = read_file(csvfile)
    if read_data is None or len(read_data) == 0:
        return ["", ""], [0, 0], 0, 0
    # store data to a list and filter by country
    data_list = save_file_data(read_data)
    if len(data_list) == 0:
        return ["", ""], [0, 0], 0, 0
    # data filter by country
    country_data_list = filter_country_data(country, data_list)
    # maximum and minimum
    max_min_list = max_min(country_data_list)
    # standard deviation
    stdv = standard_deviation(country_data_list, data_list)
    # ratio
    ratio = profit_ratio(country_data_list)
    # correlation
    correlation = correlation_coefficient(country_data_list)
    return max_min_list, stdv, ratio, correlation


if __name__ == '__main__':
    print(main("./Organisations.csv", "Japan"))
