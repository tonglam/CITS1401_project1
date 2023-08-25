def read_file(csvfile):
    try:
        with open(csvfile, 'r') as f:
            # read file by lines
            data = f.readlines()
            return data
    except IOError:
        print("read csvfile:%s error" % csvfile)
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
    if len(data_list) == 0:
        return None
    # filter by country
    return [x for x in data_list if x['Country'].upper() == country.upper()]


def max_min(data_list):
    # set default values by values from the first line
    max_min_list = [data_list[0]["Name"], data_list[0]["Name"]]
    max_employees, min_employees = int(data_list[0]["Number of employees"]), int(data_list[0]["Number of employees"])
    # loop to find max and min
    for i in range(len(data_list)):
        line_dict = data_list[i]
        number = int(line_dict["Number of employees"])
        if number > max_employees:
            max_employees = number
            # update the max organization name
            max_min_list[0] = line_dict["Name"]
        elif number < min_employees:
            min_employees = number
            # update the min organization name
            max_min_list[1] = line_dict["Name"]
    return max_min_list


def standard_deviation(country_data_list, data_list):
    # get the salary lists
    country_salary_list = [int(x["Median Salary"]) for x in country_data_list]
    all_salary_list = [int(x["Median Salary"]) for x in data_list]
    # calculate the standard deviation
    country_sd = calculate_sd(country_salary_list)
    all_sd = calculate_sd(all_salary_list)
    return [country_sd, all_sd]


def calculate_sd(data_list):
    # calculate length
    length = len(data_list)
    # standard deviation must contain at least two values
    if length == 1:
        return None
    # calculate mean
    mean = sum(data_list) / length
    # calculate standard deviation
    diff_sq_sum = sum([(x - mean) ** 2 for x in data_list])
    return (diff_sq_sum / (length - 1)) ** 0.5


def profit_ratio(data_list):
    # get profits list
    profits_list = [int(x["Profits in 2021(Million)"]) - int(x["Profits in 2020(Million)"]) for x in data_list]
    # calculate the ratio
    positive = sum([profit for profit in profits_list if profit > 0])
    negative = abs(sum([profit for profit in profits_list if profit < 0]))
    return positive / negative


def correlation_coefficient(country_data_list):
    # get the profits in 2021 list
    profits_2021_list = [int(x["Profits in 2021(Million)"]) for x in country_data_list]
    # get the median salaries list
    median_salary_list = [int(x["Median Salary"]) for x in country_data_list]
    # calculate the means
    profits_mean = sum(profits_2021_list) / len(profits_2021_list)
    median_salary_mean = sum(median_salary_list) / len(median_salary_list)
    # calculate the correlation coefficient, profits_2021_list and median_salary_list have the same length with country_data_list
    molecule = sum([(profits_2021_list[i] - profits_mean) * (median_salary_list[i] - median_salary_mean) for i in range(len(country_data_list))])
    denominator = (sum([(x - profits_mean) ** 2 for x in profits_2021_list]) * sum([(y - median_salary_mean) ** 2 for y in median_salary_list])) ** 0.5
    return molecule / denominator


def main(csvfile, country):
    # read file
    read_data = read_file(csvfile)
    if read_data is None:
        print("read csvfile:%s error: file is empty" % csvfile)
        return None
    # store data to a list and filter by country
    data_list = save_file_data(read_data)
    if len(data_list) == 0:
        print("read csvfile:%s error: file is empty" % csvfile)
        return None
    # data filter by country
    country_data_list = filter_country_data(country, data_list)
    if len(country_data_list) == 0:
        print("read csvfile:%s error: country:%s data is empty" % (csvfile,country))
        return None
    # maximum and minimum
    max_min_list = max_min(country_data_list)
    # standard deviation
    stdv = standard_deviation(country_data_list, data_list)
    # ratio
    ratio = profit_ratio(country_data_list)
    # correlation
    correlation = correlation_coefficient(country_data_list)
    return max_min_list, stdv, ratio, correlation

