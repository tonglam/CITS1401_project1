import logging as log

import numpy as np

import solution as solution

csvfile = "./Organisations.csv"


def read_file(csvfile):
    try:
        with open(csvfile, 'r') as f:
            # read file by lines
            data = f.readlines()
            return data
    except IOError:
        log.error("read csvfile:%s error" % csvfile)
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


def check_max_min(max_min_list, country_data_list):
    solution_max_name = max_min_list[0]
    solution_min_name = max_min_list[1]
    expect_max = max([int(x["Number of employees"]) for x in country_data_list])
    expect_min = min([int(x["Number of employees"]) for x in country_data_list])
    # check num
    for x in country_data_list:
        name = x["Name"].lower()
        assert int(x["Number of employees"]) <= expect_max, (
                "max name is wrong, expected:[%s], solution:[%s]" % (name, solution_max_name))
        assert int(x["Number of employees"]) >= expect_min, (
                "min name is wrong, expected:[%s], solution:[%s]" % (name, solution_min_name))
    # check order
    solution_max_list = [x for x in country_data_list if int(x["Number of employees"]) == expect_max]
    if len(solution_max_list) > 1:
        solution_max_list.sort()
        assert solution_max_list[0]["Name"] == solution_max_name, (
                "max name is wrong, not in the order, expected:[%s], solution:[%s]" % (
            solution_max_list[0]["Name"], solution_max_name))
    solution_min_list = [x for x in country_data_list if int(x["Number of employees"]) == expect_min]
    if len(solution_min_list) > 1:
        solution_min_list.sort()
        assert solution_min_list[0]["Name"] == solution_min_name, (
                "min name is wrong, not in the order, expected:[%s], solution:[%s]" % (
            solution_min_list[0]["Name"], solution_min_name))


def check_stdv(country, stdv, country_data_list, data_list):
    expect_sd_country = round(np.std([int(x["Median Salary"]) for x in country_data_list], ddof=1), 4)
    expect_sd_all = round(np.std([int(x["Median Salary"]) for x in data_list], ddof=1), 4)
    solution_sd_country = stdv[0]
    solution_sd_all = stdv[1]
    # check
    assert expect_sd_country == solution_sd_country, (
        "country:%s standard deviation is wrong, expected:[%d], solution:[%d]" % country, expect_sd_country,
        solution_sd_country)
    assert expect_sd_all == solution_sd_all, (
        "country:%s standard deviation is wrong, expected:[%d], solution:[%d]" % country, expect_sd_all,
        solution_sd_all)


def check_ratio(country_data_list, ratio):
    # get profits list
    profits_list = [int(x["Profits in 2021(Million)"]) - int(x["Profits in 2020(Million)"]) for x in country_data_list]
    # calculate the ratio
    positive = sum([profit for profit in profits_list if profit > 0])
    negative = abs(sum([profit for profit in profits_list if profit < 0]))
    # check
    expected_ratio = round(positive / negative, 4) if negative != 0 else 0
    assert expected_ratio == ratio, ("ratio is wrong, expected:[%d], solution:[%d]" % (expected_ratio, ratio))


def check_correlation(country, solution_corr, country_data_list):
    # only use the organisations which show an increase in profits from 2020 to 2021
    country_valid_data_list = [x for x in country_data_list if
                               int(x["Profits in 2021(Million)"]) - int(x["Profits in 2020(Million)"]) > 0]
    # get the profits in 2021 list
    profits_2021_list = [int(x["Profits in 2021(Million)"]) for x in country_valid_data_list]
    # get the median salaries list
    median_salary_list = [int(x["Median Salary"]) for x in country_valid_data_list]
    # pf.corr
    np_corr = float(np.corrcoef(median_salary_list, profits_2021_list)[0, 1])
    expected_corr = round(np_corr, 4)
    # check
    assert expected_corr == solution_corr, ("country:%s correlation is wrong, expected:[%d], solution:[%d]" % (
        country, expected_corr, solution_corr))


def test_case(csvfile, country, country_data_list, data_list):
    max_min_list, stdv, ratio, correlation = solution.main(csvfile, country)
    # check max and min
    check_max_min(max_min_list, country_data_list)
    # check standard deviation
    check_stdv(country, stdv, country_data_list, data_list)
    # check ratio
    check_ratio(country_data_list, ratio)
    # check correlation
    check_correlation(country, correlation, country_data_list)
    # result
    print("Congratulations! All test cases passed! Well done!")


def test_one_case():
    csvfile = "./Organisations.csv"
    country = "Belgium"
    # read file, get all countries
    read_data = read_file(csvfile)
    # get data list
    data_list = save_file_data(read_data)
    # get country list
    country_data_list = filter_country_data(country, data_list)
    # test
    test_case(csvfile, country, country_data_list, data_list)


def test_all_case():
    csvfile = "./Organisations.csv"
    # read file, get all countries
    read_data = read_file(csvfile)
    # get data list
    data_list = save_file_data(read_data)
    country_list = list(set([read_data[i].strip().split(',')[3] for i in range(len(read_data)) if i > 0]))
    for country in country_list:
        log.error(("start testing country: %s" % country))
        # get country list
        country_data_list = filter_country_data(country, data_list)
        test_case(csvfile, country, country_data_list, data_list)


if __name__ == '__main__':
    test_one_case()
    # test_all_case()
