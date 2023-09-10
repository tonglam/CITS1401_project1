import os
import time

import numpy as np

import solution as solution

default_csvfile = "./Organisations.csv"


def read_file(csvfile):
    try:
        with open(csvfile, 'r') as f:
            # read file by lines
            data = f.readlines()
            return data
    except IOError:
        print("read csvfile:%s error\n" % csvfile)
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
    country_data_list = [x for x in country_data_list if 1981 < int(x["Founded"]) <= 2000]
    # empty list
    if not any(max_min_list):
        assert not any(country_data_list) is True, "max_min_list and country_data_list must be empty at the same time"
        print("max name:[''], min name:['']\n")
        return
    else:
        # not empty list, at least two elements
        assert len(max_min_list) >= 2, "max_min_list:%s must contains at least two elements" % max_min_list
    solution_max_name = max_min_list[0]
    solution_min_name = max_min_list[1]
    expect_max = max([int(x["Number of employees"]) for x in country_data_list])
    expect_min = min([int(x["Number of employees"]) for x in country_data_list])
    # check num
    for x in country_data_list:
        name = x["Name"].lower()
        assert int(x["Number of employees"]) <= expect_max, (
                "max name is wrong, expected:[%s], solution:[%s]\n" % (name, solution_max_name))
        assert int(x["Number of employees"]) >= expect_min, (
                "min name is wrong, expected:[%s], solution:[%s]\n" % (name, solution_min_name))
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
    print("max name:[%s], min name:[%s]\n" % (solution_max_name, solution_min_name))


def check_stdv(country, stdv, country_data_list, data_list):
    assert len(stdv) == 2, "standard deviation must contains two elements"
    expect_sd_country = round(np.std([int(x["Median Salary"]) for x in country_data_list], ddof=1), 4) if len(
        country_data_list) > 1 else 0
    expect_sd_all = round(np.std([int(x["Median Salary"]) for x in data_list], ddof=1), 4) if len(data_list) > 1 else 0
    solution_sd_country = stdv[0]
    solution_sd_all = stdv[1]
    # check
    assert expect_sd_country == solution_sd_country, (
        "country:%s standard deviation is wrong, expected:[%s], solution:[%s]" % country, expect_sd_country,
        solution_sd_country)
    assert expect_sd_all == solution_sd_all, (
        "country:%s standard deviation is wrong, expected:[%s], solution:[%s]" % country, expect_sd_all,
        solution_sd_all)
    print("country standard deviation:[%s], all standard deviation:[%s]\n" % (solution_sd_country, solution_sd_all))


def check_ratio(country_data_list, solution_ratio):
    if len(country_data_list) == 0:
        solution_ratio = 0
    # get profits list
    profits_list = [int(x["Profits in 2021(Million)"]) - int(x["Profits in 2020(Million)"]) for x in country_data_list]
    if len(profits_list) == 0:
        solution_ratio = 0
    # calculate the ratio
    positive = sum([profit for profit in profits_list if profit > 0])
    negative = abs(sum([profit for profit in profits_list if profit < 0]))
    # check
    expected_ratio = round(positive / negative, 4) if negative != 0 else 0
    assert expected_ratio == solution_ratio, (
            "ratio is wrong, expected:[%s], solution:[%s]" % (expected_ratio, solution_ratio))
    print("ratio:[%s]\n" % solution_ratio)


def check_correlation(country, solution_corr, country_data_list):
    if len(country_data_list) == 0:
        assert solution_corr == 0, ("country:%s correlation is wrong, expected:[%s], solution:[%s]" % (
            country, 0, solution_corr))
        print("correlation:[0]\n")
        return
    # only use the organisations which show an increase in profits from 2020 to 2021
    country_valid_data_list = [x for x in country_data_list if
                               int(x["Profits in 2021(Million)"]) - int(x["Profits in 2020(Million)"]) > 0]
    if len(country_valid_data_list) == 0 or len(country_valid_data_list) == 1:
        assert solution_corr == 0, ("country:%s correlation is wrong, expected:[%s], solution:[%s]" % (
            country, 0, solution_corr))
        print("correlation:[0]\n")
        return
    # get the profits in 2021 list
    profits_2021_list = [int(x["Profits in 2021(Million)"]) for x in country_valid_data_list]
    # get the median salaries list
    median_salary_list = [int(x["Median Salary"]) for x in country_valid_data_list]
    # pf.corr
    np_corr = float(np.corrcoef(median_salary_list, profits_2021_list)[0, 1])
    expected_corr = round(np_corr, 4)
    # check
    assert expected_corr == solution_corr, ("country:%s correlation is wrong, expected:[%s], solution:[%s]" % (
        country, expected_corr, solution_corr))
    print("correlation:[%s]\n" % solution_corr)


def test_case(csvfile, country, country_data_list, data_list):
    print("\nStart testing country:[%s]\n" % country)
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
    print("Congratulations! Country:[%s] passed all the tests!! Well done!!!\n" % country)


def test_preparing(csvfile=default_csvfile, country="Belgium"):
    # read file, get all countries
    read_data = read_file(csvfile)
    # get data list
    data_list = save_file_data(read_data)
    # get country list
    country_data_list = filter_country_data(country, data_list)
    return country_data_list, data_list


# test 1: test one case
def test_one_case():
    country = "Japan"
    country_data_list, data_list = test_preparing(country=country)
    # test
    test_case(default_csvfile, country, country_data_list, data_list)
    print("finished testing one case\n")


# test 2: test all cases
def test_all_cases():
    # read file, get all countries
    read_data = read_file(default_csvfile)
    # get data list
    data_list = save_file_data(read_data)
    country_list = list(set([read_data[i].strip().split(',')[3] for i in range(len(read_data)) if i > 0]))
    for country in country_list:
        # get country list
        country_data_list = filter_country_data(country, data_list)
        test_case(default_csvfile, country, country_data_list, data_list)
    print("finished testing all cases\n")


def test_empty_file():
    # read file, get all countries
    read_data = read_file(default_csvfile)
    # empty input file with header
    empty_with_header_file = "./empty_with_header.csv"
    f_header = open(empty_with_header_file, 'w')
    f_header.write(read_data[0])
    f_header.close()
    test_case(empty_with_header_file, "", [], [])
    os.remove(empty_with_header_file)
    # empty input file without header
    empty_without_header_file = "./empty_without_header.csv"
    f_without_header = open(empty_without_header_file, 'w')
    f_without_header.write("")
    f_without_header.close()
    test_case(empty_without_header_file, "", [], [])
    os.remove(empty_without_header_file)


def exist_country_one_record_file(test_file, test_country):
    country_data_list, data_list = test_preparing(country=test_country)
    country_data_list[0]["Founded"] = "1990"
    # write to file
    f = open(test_file, 'w')
    f.write(str([str(x) + "," for x in country_data_list[0].keys()]))
    f.write("\n")
    f.write(str([str(x.values()) + "\n" for x in country_data_list]))
    f.close()


# test 3: test edge cases
def test_edge_cases():
    # # empty file
    # test_empty_file()
    # print("finished testing empty file\n")
    # # empty country
    # test_case(default_csvfile, "", [], [])
    # print("finished testing empty country\n")
    # # not exists country
    # country_data_list, data_list = test_preparing(country="TEST")
    # test_case(default_csvfile, "TEST", country_data_list, data_list)
    # print("finished testing not exists country\n")
    # existing country, one valid record
    test_file = "./exist_country_with_one_record.csv"
    test_country = "Japan"
    exist_country_one_record_file(test_file, test_country)
    try:
        with open(test_file, 'r') as f:
            country_data_list, data_list = test_preparing(csvfile=test_file, country=test_country)
            test_case(test_file, test_country, country_data_list, data_list)
    except IOError:
        time.sleep(30)
        with open(test_file, 'r') as f:
            country_data_list, data_list = test_preparing(csvfile=test_file, country=test_country)
            test_case(test_file, test_country, country_data_list, data_list)
    os.remove(test_file)

    print(1)
