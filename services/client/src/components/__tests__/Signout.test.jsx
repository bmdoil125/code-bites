import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';
import { MemoryRouter as Router } from 'react-router-dom';

import Signout from '../Signout';

// Mock user to log out with
const user = jest.fn()

test('Signout renders', () => {
    const wrapper = shallow(<Signout signoutUser={ user }/>);
    const element = wrapper.find('p');
    expect(element.length).toBe(1);
    expect(element.get(0).props.children[0]).toContain('Signed Out')
});


test('Signout renders a snapshot', () => {
    const tree = renderer.create(
      <Router><Signout signoutUser={user}/></Router>
    ).toJSON();
    expect(tree).toMatchSnapshot();
  });