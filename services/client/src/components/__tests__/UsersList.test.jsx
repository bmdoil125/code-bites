import React from 'react';
import { shallow } from 'enzyme'
import renderer from 'react-test-renderer';
import UsersList from '../UsersList'

const users = [
    {
        'active': true,
        'email': 'brent@brentdoil.com',
        'id': 1,
        'username': 'brent'
    },
    {
        'active': true,
        'email': 'testy@testing.com',
        'id': 2,
        'username': 'testing1'
    }
];

// https://stackoverflow.com/questions/38710309/when-should-you-use-render-and-shallow-in-enzyme-react-tests/38747914#38747914
test('UsersList renders', () => {
    const wrapper = shallow(<UsersList users={users}/>);    //create UsersList component
    const element = wrapper.find('h4')                      // get output of UsersList
    expect(element.length).toBe(2)                  
    expect(element.get(0).props.children).toBe('brent');    
})
// snapshot is saved to __snapshots__
// on subsequent runs new output will be compared to saved output
test('UsersList renders a snapshot', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON();
    expect(tree).toMatchSnapshot();
})