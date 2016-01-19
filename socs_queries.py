import pandas as pd

"""
Author: John Levander

Description:
    The purpose of this program is to extract data from a dataframe using a simulator count output specification as the
    query specification.  This script is in it's early stages of development.  As it sits right now, the program will
    load a dataset of simulator output and filter out all rows that are about LATENT or INFECTIOUS MALES.
Log:
    01/15/2016: Simple example to create dataframe queries given categorical variables.  Next step is to support
                integer variables and age ranges.
    01/19/2016: Started to implement age ranges.  Passing this off to Nick Millett for now.
"""


# Sample Simulator Count Output Specifications
all_sick_scos = {}
all_sick_scos["simulator_count_variables"] = {}
all_sick_scos["simulator_count_variables"]['infection_state'] = ["LATENT", "INFECTIOUS"]
all_sick_scos["output_options"] = {}
all_sick_scos["output_options"]['axes'] = {'simulator_time'}


all_sick_by_sex = {}
all_sick_by_sex["simulator_count_variables"] = {}
all_sick_by_sex["simulator_count_variables"]['infection_state'] = ["LATENT", "INFECTIOUS"]
all_sick_by_sex["simulator_count_variables"]['sex'] = ["M"]

all_sick_by_sex_by_age_range = {}
#this is the where clause
all_sick_by_sex_by_age_range["simulator_count_variables"] = {}
all_sick_by_sex_by_age_range["simulator_count_variables"]['infection_state'] = ["LATENT", "INFECTIOUS"]
all_sick_by_sex_by_age_range["simulator_count_variables"]['sex'] = ["M", "F"]
all_sick_by_sex_by_age_range["simulator_count_variables"]['age_range'] = {}
all_sick_by_sex_by_age_range["simulator_count_variables"]['age_range']['driving_age'] = [16,999]
all_sick_by_sex_by_age_range["simulator_count_variables"]['age_range']['voting_age'] = [18,999]
all_sick_by_sex_by_age_range["simulator_count_variables"]['age_range']['retirement_age'] = [65,999]
#this is the select clause
all_sick_by_sex_by_age_range["output_options"] = {}
all_sick_by_sex_by_age_range["output_options"]['axes'] = {'simulator_time', 'age_range'}

all_sick_by_sex_by_age = {}
#this is the where clause
all_sick_by_sex_by_age["simulator_count_variables"] = {}
all_sick_by_sex_by_age["simulator_count_variables"]['infection_state'] = ["LATENT", "INFECTIOUS"]
all_sick_by_sex_by_age["simulator_count_variables"]['sex'] = ["M", "F"]
all_sick_by_sex_by_age["simulator_count_variables"]['integer_age'] = {"min_age" : 30, "max_age" : 40}
#this is the select clause
all_sick_by_sex_by_age["output_options"] = {}
all_sick_by_sex_by_age["output_options"]['axes'] = {'simulator_time', 'integer_age'}

"""
TODO: Add support for these in next version.
all_sick_by_sex_by_age = {}
all_sick_by_sex_by_age["simulator_count_variables"] = {}
all_sick_by_sex_by_age["simulator_count_variables"]['infection_states'] = ["LATENT", "INFECTIOUS"]
all_sick_by_sex_by_age["simulator_count_variables"]['sex'] = ["M", "F"]
all_sick_by_sex_by_age["simulator_count_variables"]['integer_age'] = True



all_sick_by_sex_by_age_state = {}
all_sick_by_sex_by_age_state["simulator_count_variables"] = {}
all_sick_by_sex_by_age_state["simulator_count_variables"]['infection_state'] = ["LATENT", "INFECTIOUS"]
all_sick_by_sex_by_age_state["simulator_count_variables"]['sex'] = ["M", "F"]
all_sick_by_sex_by_age_state["simulator_count_variables"]['integer_age'] = "all"
all_sick_by_sex_by_age_state["simulator_count_variables"]['location_admin1'] = "all"
"""


def add_age_range_column(scos, df):

    def filter_out_unrequested_age_ranges(df, age_range):
    #build the query
    #remove everything below minnist min, and above maxxest max
        query = "(integer_age >= "+age_range[0] +") & (integer_age <= 25)"
        df = df.query(query)
        return df


    def make_age_range_row(row):
        return pd.cut([row['integer_age']], bins=bins, labels=bin_labels)[0]

    df = filter_out_unrequested_age_ranges(df)
    #nick create the bins given all_sick_by_sex_by_age_range["simulator_count_variables"]['age_range']
    #here is some help:
    age_ranges = scos["simulator_count_variables"]['age_range']
    for age_range in age_ranges:
        print (age_range + " bin is " + str(age_ranges[age_range][0]) + " to " + str(age_ranges[age_range][1]))

    #result of nicks awesome code is bins and labels
    bins = [0,2,65,100]
    bin_labels = ['infant', 'unwanted_1', 'retirement']

    df['age_range'] = df.apply(make_age_range_row, axis=1)

    return df

"""
This function creates queries in the form of: 'b == ["a", "b", "c"]'
The query selects all rows in the dataframe where column b is equal to the value a b or c.
"""
def create_category_query(df, col_name, vals_to_keep):
    query = df.columns[df.columns.get_loc(col_name)] + ' == ['
    for val in vals_to_keep:
        query += "'" + val + "',"
    query = query[:-1]
    query += "]"
    return query

"""
Here we enforce the WHERE clause.  We filter out rows that we do not want, want based on the simulator_count_variables.
For example if the user
only wanted to see the rows that contain data for MALES, it would be specified in the simulator_count_variables, and we
would filter the FEMALES out in this function.
"""
def filter_df(df, scos):
    #TODO: deal with age_range categories and integer categories
    for simulator_count_variable in scos["simulator_count_variables"]:
        if simulator_count_variable != "age_range":
            query = create_category_query(df, simulator_count_variable, scos['simulator_count_variables'][simulator_count_variable])
            df = df.query(query)
    return df




if __name__ == '__main__':
    scos = all_sick_by_sex_by_age_range

    #load the simulator output into a dataframe
    line_listing = pd.read_csv('http://research.rods.pitt.edu/line_listing.csv')


    #Filter out rows from the dataframe that we don't want
    df = filter_df(line_listing, scos)

    df = add_age_range_column(scos, df)

    #TODO: Add aggregation options next, once data is filtered
    print (df)
