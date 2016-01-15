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

"""
TODO: Add support for these in next version.
all_sick_by_sex_by_age = {}
all_sick_by_sex_by_age["simulator_count_variables"] = {}
all_sick_by_sex_by_age["simulator_count_variables"]['infection_states'] = ["LATENT", "INFECTIOUS"]
all_sick_by_sex_by_age["simulator_count_variables"]['sex'] = ["M", "F"]
all_sick_by_sex_by_age["simulator_count_variables"]['integer_age'] = True

all_sick_by_sex_by_age_range = {}
all_sick_by_sex_by_age_range["simulator_count_variables"] = {}
all_sick_by_sex_by_age_range["simulator_count_variables"]['infection_states'] = ["LATENT", "INFECTIOUS"]
all_sick_by_sex_by_age_range["simulator_count_variables"]['sex'] = ["M", "F"]
all_sick_by_sex_by_age_range["simulator_count_variables"]['age_range'] = [0, 5, 18, 25, 65, 100]


all_sick_by_sex_by_age_state = {}
all_sick_by_sex_by_age_state["simulator_count_variables"] = {}
all_sick_by_sex_by_age_state["simulator_count_variables"]['infection_state'] = ["LATENT", "INFECTIOUS"]
all_sick_by_sex_by_age_state["simulator_count_variables"]['sex'] = ["M", "F"]
all_sick_by_sex_by_age_state["simulator_count_variables"]['integer_age'] = "all"
all_sick_by_sex_by_age_state["simulator_count_variables"]['location_admin1'] = "all"
"""


"""
This function creates queries in the form of: df.query('b == ["a", "b", "c"]')
The query selects all rows in the dataframe where column b is equal to the value a b or c.
"""
def create_query(df, col_name, vals_to_keep):
    query = df.columns[df.columns.get_loc(col_name)] + ' == ['
    for val in vals_to_keep:
        query += "'" + val + "',"
    query = query[:-1]
    query += "]"
    return query


"""
Here we SELECT only rows that we want based on the simulator_count_variables.  For example if the user
only wanted to see the rows that contain data for MALES, it would be specified in the simulator_count_variables, and we
would filter the FEMALES out in this function.
"""
def filter_df(df, scos):
    #TODO: deal with age_range categories and integer categories
    for simulator_count_variable in scos["simulator_count_variables"]:
        query = create_query(df, simulator_count_variable, scos['simulator_count_variables'][simulator_count_variable])
        df = df.query(query)
    return df

if __name__ == '__main__':
    #load the simulator output into a dataframe
    line_listing = pd.read_csv('http://research.rods.pitt.edu/line_listing.csv')

    #Filter out rows from the dataframe that we don't want
    df = filter_df(line_listing, all_sick_by_sex)

    #TODO: Add aggregation options next, once data is filtered
    print (df)
