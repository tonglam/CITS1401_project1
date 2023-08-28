import logging as log

import numpy as np
import pandas as pd
import pytest as pytest
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
    solution_max = max([x["Number of employees"] for x in country_data_list])
    solution_min = max([x["Number of employees"] for x in country_data_list])
    # check
    for x in country_data_list:
        name = x["Name"].lower()
        assert int(x["Number of employees"]) <= solution_max, (
                "max name is wrong, detected:[%s], solution:[%s]" % (name, solution_max_name))
        assert int(x["Number of employees"]) >= solution_min, (
                "min name is wrong, detected:[%s], solution:[%s]" % (name, solution_min_name))


def check_stdv(country, stdv, country_data_list, data_list):
    np_sd_country = np.std([int(x["Median Salary"]) for x in country_data_list])
    np_sd_all = np.std([int(x["Median Salary"]) for x in data_list])
    solution_sd_country = round(stdv[0], 4)
    solution_sd_all = round(stdv[1], 4)
    pytest.approx(np_sd_country, solution_sd_country)
    pytest.approx(np_sd_all, solution_sd_all)
    # check
    assert np_sd_country == solution_sd_country, ("country:%s standard deviation is wrong, np:[%d], solution:[%d]"
                                                  % country, np_sd_country, solution_sd_country)
    assert np_sd_all == solution_sd_all, ("country:%s standard deviation is wrong, np:[%d], solution:[%d]"
                                          % country, np_sd_all, solution_sd_all)


def check_ratio(country, ratio):
    pass


def check_correlation(country, solution_corr, country_data_list):
    # get the profits in 2021 list
    profits_2021_list = [int(x["Profits in 2021(Million)"]) for x in country_data_list]
    # get the median salaries list
    median_salary_list = [int(x["Median Salary"]) for x in country_data_list]
    # pf.corr
    df = pd.DataFrame({'profits_2021_list': profits_2021_list, 'median_salary_list': median_salary_list})
    corr = round(df['profits_2021_list'].corr(df['median_salary_list']), 4)
    # check
    assert corr == solution_corr, (
            "country:%s correlation is wrong, pd:[%d], solution:[%d]" % (country, corr, solution_corr))


def test_case(country, country_data_list, data_list):
    max_min_list, stdv, ratio, correlation = solution.main(csvfile, country)
    # check max and min
    check_max_min(max_min_list, country_data_list)
    # check standard deviation
    check_stdv(country, stdv, country_data_list, data_list)
    # check ratio
    check_ratio(country, ratio)
    # check correlation
    check_correlation(country, correlation, country_data_list)


@pytest.mark.parametrize("csvfile, country", ["./Organisations.csv", "Belgium"])
def test_one_case(csvfile, country):
    # read file, get all countries
    read_data = read_file(csvfile)
    # get data list
    data_list = save_file_data(read_data)
    # get country list
    country_data_list = filter_country_data(country, data_list)
    # test
    test_case(country, country_data_list, data_list)


@pytest.mark.parametrize("csvfile", ["./Organisations.csv"])
def test_all_case(csvfile):
    # read file, get all countries
    read_data = read_file(csvfile)
    # get data list
    data_list = save_file_data(read_data)
    country_list = list(set([read_data[i].strip().split(',')[3] for i in range(len(read_data)) if i > 0]))
    for country in country_list:
        log.error(("start testing country: %s" % country))
        # get country list
        country_data_list = filter_country_data(country, data_list)
        test_case(country, country_data_list, data_list)


def test_input_case():
    pass
