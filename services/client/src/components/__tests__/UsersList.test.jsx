import React from 'react';
import { shallow } from 'enzyme'
import renderer from 'react-test-renderer';
import UsersList from '../UsersList'

const users = [
    {
        'active': true,
        'email': 'brent@brentdoil.com',
        'id': 1,
        'username': 'brent',
        'admin': false
    },
    {
        'active': false,
        'email': 'testy@testing.com',
        'id': 2,
        'username': 'testing1',
        'admin': true
    }
];

// https://stackoverflow.com/questions/38710309/when-should-you-use-render-and-shallow-in-enzyme-react-tests/38747914#38747914
test('UsersList renders', () => {
    const wrapper = shallow(<UsersList users={users}/>);    //create UsersList component
    const row = wrapper.find('tr')                      // get output of UsersList
    expect(row.length).toBe(4)
    expect(wrapper.find('h1').get(0).props.children).toBe('All Users');
    const header = wrapper.find('thead > tr > th')
    expect(header.length).toBe(5);
    expect(header.get(0).props.children).toBe('ID');
    expect(header.get(1).props.children).toBe('USERNAME');
    expect(header.get(2).props.children).toBe('EMAIL');
    expect(header.get(3).props.children).toBe('ACTIVE');
    expect(header.get(4).props.children).toBe('ADMIN');
    expect(header.length).toBe(5)
    const td = wrapper.find('tbody > tr > td')
    // First entry
    expect(td.get(0).props.children).toBe(1);
    expect(td.get(1).props.children).toBe('brent');   
    expect(td.get(2).props.children).toBe('brent@brentdoil.com');
    expect(td.get(3).props.children).toBe('true');
    expect(td.get(4).props.children).toBe('false');
    // Second entry
    expect(td.get(5).props.children).toBe(2);
    expect(td.get(6).props.children).toBe('testing1');   
    expect(td.get(7).props.children).toBe('testy@testing.com');
    expect(td.get(8).props.children).toBe('false');
    expect(td.get(9).props.children).toBe('true');

})
// snapshot is saved to __snapshots__
// on subsequent runs new output will be compared to saved output
test('UsersList renders a snapshot', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON();
    expect(tree).toMatchSnapshot();
})