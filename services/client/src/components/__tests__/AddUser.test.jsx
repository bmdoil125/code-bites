import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import AddUser from '../AddUser';

test('AddUser renders', () => {
    const wrapper = shallow(<AddUser/>);    // create AddUser component
    const element = wrapper.find('form');   // find form in AddUser
    expect(element.find('input').length).toBe(3);   // should have 3 props, username, email, submit
    expect(element.find('input').get(0).props.name).toBe('username');
    expect(element.find('input').get(1).props.name).toBe('email');
    expect(element.find('input').get(2).props.type).toBe('submit');

});