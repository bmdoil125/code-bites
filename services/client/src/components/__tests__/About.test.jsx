import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import About from '../About';

test('About renders', () => {
    const wrapper = shallow(<About/>);
    const element = wrapper.find('p');
    expect(element.length).toBe(1);
    expect(element.text()).toBe('REST API Final Project')
});

test('About snapshot renders', () => {
    const tree = renderer.create(<About/>).toJSON();
    expect(tree).toMatchSnapshot();
});