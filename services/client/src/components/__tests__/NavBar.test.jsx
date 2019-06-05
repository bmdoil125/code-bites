import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';
// https://reacttraining.com/react-router/core/api/MemoryRouter
import { MemoryRouter as Router } from 'react-router-dom'

import NavBar from '../NavBar';

const title = "Code Bites";

test('Navbar renders', () => {
    const wrapper = shallow(<NavBar title={title}/>);
    const element = wrapper.find('strong');
    expect(element.length).toBe(1);
    expect(element.get(0).props.children).toBe(title);
})
// Renders a navbar with title inside a Router object
test('Navbar snapshot renders', () => {
    const tree = renderer.create(
        <Router location="/"><NavBar title={title}/></Router>
    ).toJSON();
    expect(tree).toMatchSnapshot();
})