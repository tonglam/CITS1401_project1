import numpy as np
import pandas as pd

import solution as solution

csvfile = "./Organisations.csv"


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


def check_max_min(country, max_min_list):
    pass


def check_stdv(country, stdv, country_data_list, data_list):
    np_sd_country = round(np.std([int(x["Median Salary"]) for x in country_data_list], ddof=1), 2)
    np_sd_all = round(np.std([int(x["Median Salary"]) for x in data_list], ddof=1), 2)
    solution_sd_country = round(stdv[0], 2)
    solution_sd_all = round(stdv[1], 2)
    if np_sd_country != solution_sd_country or np_sd_all != solution_sd_all:
        raise Exception("country:%s standard deviation is wrong, np:[%d, %d], solution:[%d, %d]"
                        % (country, np_sd_country, np_sd_all, solution_sd_country, solution_sd_all))


def check_ratio(country, ratio):
    pass


def check_correlation(country, solution_corr, country_data_list):
    # get the profits in 2021 list
    profits_2021_list = [int(x["Profits in 2021(Million)"]) for x in country_data_list]
    # get the median salaries list
    median_salary_list = [int(x["Median Salary"]) for x in country_data_list]
    # pf.corr
    df = pd.DataFrame({'profits_2021_list': profits_2021_list, 'median_salary_list': median_salary_list})
    corr = round(df['profits_2021_list'].corr(df['median_salary_list']), 2)
    solution_corr = round(solution_corr, 2)
    if corr != solution_corr:
        raise Exception("country:%s correlation is wrong, pd:[%d], solution:[%d]" % (country, corr, solution_corr))


def main():
    # read file, get all countries
    read_data = read_file(csvfile)
    # get data list
    data_list = save_file_data(read_data)
    country_list = list(set([read_data[i].strip().split(',')[3] for i in range(len(read_data)) if i > 0]))
    country_list = ["Hong Kong"]
    for country in country_list:
        print("start testing, country: %s" % country)
        # get country list
        country_data_list = filter_country_data(country, data_list)
        max_min_list, stdv, ratio, correlation = solution.main(csvfile, country)
        # check max and min
        check_max_min(country, max_min_list)
        # check standard deviation
        check_stdv(country, stdv, country_data_list, data_list)
        # check ratio
        check_ratio(country, ratio)
        # check correlation
        check_correlation(country, correlation, country_data_list)
        print("pass testing, country: %s" % country)


if __name__ == "__main__":
    main()
