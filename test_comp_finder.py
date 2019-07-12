import comp_finder

def test_find_comps():
    
    # only info found in find_comps function

    comp_info = comp_finder.find_comps(
        'New York', '1600 Pennsylvania Avenue, Washington DC', ['date', 'venue', 'website_link'])

    # only info found in Competition class methods

    comp_specific_info = comp_finder.find_comps(
        'New York', '1600 Pennsylvania Avenue, Washington DC', ['venue_address', 'driving_distance', 'reached_competitor_limit']
    )

    print(comp_info)
    print([['name', 'date', 'venue', 'website_link'],
           [['Hudson Valley Summer 2019', 'Jul 13 2019', 'Arlington High School', 'https://www.worldcubeassociation.org/competitions/HudsonValleySummer2019']]])

    print(comp_specific_info)
    print([['name', 'venue_address', 'driving_distance', 'reached_competitor_limit'],
          [['Hudson Valley Summer 2019', '1157 State Rte 55, Lagrangeville, NY 12540', '1h 45min', 'True']]])
    

if __name__ == '__main__':
    test_find_comps()
