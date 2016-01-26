import xml.etree.ElementTree as ET
import math

APOLLO_TYPES_NAMESPACE = 'http://types.apollo.pitt.edu/v4_0/'
XSI_TYPE = '{http://www.w3.org/2001/XMLSchema-instance}type'

def process_other_variables(query, base):
    variable = base.find('{' + APOLLO_TYPES_NAMESPACE + '}variable')
    categories = base.findall('{' + APOLLO_TYPES_NAMESPACE + '}categories')
    range_type = ''
    if variable.text == 'ageRange':
        range_type = 'age_range'
    elif variable.text == 'householdMedianIncome':
        range_type = 'household_median_income'

    query["simulator_count_variables"][range_type] = {}
    query["output_options"]['axes'].append(range_type)

    for category in categories:
        type = category.get(XSI_TYPE)
        if type == 'apollo:MeasuredQuantityRangeCategoryDefinition':
            unit_of_measure = category.find('{' + APOLLO_TYPES_NAMESPACE + '}unitOfMeasure')

            lower_bound = category.find('{' + APOLLO_TYPES_NAMESPACE + '}lowerBound')
            query_lb = process_boundary(lower_bound)

            upper_bound = category.find('{' + APOLLO_TYPES_NAMESPACE + '}upperBound')
            query_ub = process_boundary(upper_bound)

            bound_text = str(query_lb) + ' - ' + str(query_ub)
            query["simulator_count_variables"][range_type][bound_text] = {}
            query["simulator_count_variables"][range_type][bound_text]['range_units'] = unit_of_measure.text
            query["simulator_count_variables"][range_type][bound_text]['range'] = [query_lb, query_ub]



def process_boundary(boundary_element):
    finite_boundry = boundary_element.find('{' + APOLLO_TYPES_NAMESPACE + '}finiteBoundary')
    infinite_boundry = boundary_element.find('{' + APOLLO_TYPES_NAMESPACE + '}infiniteBoundary')
    if finite_boundry is not None:
        lb = int(finite_boundry.text)
    elif infinite_boundry is not None:
        inf_type = infinite_boundry.text
        if inf_type == 'negativeInfinity':
            lb = -float("inf")
        elif inf_type == 'positiveInfinity':
            lb = float("inf")
    return lb

if __name__ == '__main__':

    tree = ET.parse('/Users/nem41/Documents/code_projects/apollo_projects/example-scos-messages/S_E_I_R_new_I_by_household_income.xml')
    root = tree.getroot()

    for count_specification in root.findall('{' + APOLLO_TYPES_NAMESPACE + '}SimulatorCountOutputSpecification'):

        query = {}
        query["simulator_count_variables"] = {}
        query["output_options"] = {}
        query["output_options"]['axes'] = []

        for element in count_specification:

            namespace = ''
            field = ''
            if '}' in element.tag:
                field = element.tag.split('}', 1)[1]  # strip all namespaces
                namespace = (element.tag.split('}', 1)[0])[1:]  # strip all namespaces

            if namespace != APOLLO_TYPES_NAMESPACE:
                print "Error: unsupported Apollo type namespace was used in the XML"

            if field == 'speciesToCount':
                query["simulator_count_variables"]['species'] = {element.text}
                query["output_options"]['axes'].append('species')
            elif field == 'temporalGranularity':
                if element.text != 'entireSimulation':
                    if element.text != 'eachSimulationTimestep':
                        # need to do further aggregation
                        print 'Error: currently the only supported temporalGranularity is eachSimulationTimestep'
                    query["output_options"]['axes'].append('simulator_time')
            elif field == 'spatialGranularity':
                if element.text != 'none':
                    if element.text == 'admin0':
                        query["simulator_count_variables"]['location_admin0'] = True
                        query["output_options"]['axes'].append('location_admin0')
                    elif element.text == 'admin1':
                        query["simulator_count_variables"]['location_admin1'] = True
                        query["output_options"]['axes'].append('location_admin0')
                        query["output_options"]['axes'].append('location_admin1')
                    elif element.text == 'admin2':
                        query["simulator_count_variables"]['location_admin2'] = True
                        query["output_options"]['axes'].append('location_admin0')
                        query["output_options"]['axes'].append('location_admin1')
                        query["output_options"]['axes'].append('location_admin2')
                    elif element.text == 'admin3':
                        query["simulator_count_variables"]['location_admin3'] = True
                        query["output_options"]['axes'].append('location_admin0')
                        query["output_options"]['axes'].append('location_admin1')
                        query["output_options"]['axes'].append('location_admin2')
                        query["output_options"]['axes'].append('location_admin3')
                    elif element.text == 'admin4':
                        query["simulator_count_variables"]['location_admin4'] = True
                        query["output_options"]['axes'].append('location_admin0')
                        query["output_options"]['axes'].append('location_admin1')
                        query["output_options"]['axes'].append('location_admin2')
                        query["output_options"]['axes'].append('location_admin3')
                        query["output_options"]['axes'].append('location_admin4')
                    elif element.text == 'admin5':
                        query["simulator_count_variables"]['location_admin5'] = True
                        query["output_options"]['axes'].append('location_admin0')
                        query["output_options"]['axes'].append('location_admin1')
                        query["output_options"]['axes'].append('location_admin2')
                        query["output_options"]['axes'].append('location_admin3')
                        query["output_options"]['axes'].append('location_admin4')
                        query["output_options"]['axes'].append('location_admin5')
                    elif element.text == 'latLong':
                        print "Error: latLong coordinates are not currently supported"
            elif field == 'infectionState':
                if 'infection_state' in query["simulator_count_variables"]:
                 query["simulator_count_variables"]['infection_state'].add(element.text)
                else:
                    query["simulator_count_variables"]['infection_state'] = {element.text}
            elif field == 'diseaseOutcome':
                if 'disease_state' in query["simulator_count_variables"]:
                 query["simulator_count_variables"]['disease_state'].add(element.text)
                else:
                    query["simulator_count_variables"]['disease_state'] = {element.text}
            elif field == 'otherVariables':
                process_other_variables(query, element)


        print query
