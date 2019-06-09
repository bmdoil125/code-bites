import React from 'react';
import { shallow, mount } from 'enzyme';
import renderer from 'react-test-renderer';

import AceEditor from 'react-ace';
jest.mock('react-ace')

import Questions from '../Questions';


test('Questions renders properly', () => {
    const wrapper = shallow(<Questions/>);
    const element = wrapper.find('h5');
    expect(element.length).toBe(1)
});


test('Questions renders snapshot', () => {
    const tree = renderer.create(<Questions/>).toJSON();
    expect(tree).toMatchSnapshot();
});

test('Questions call componentWillMount', () => {
    const onWillMount = jest.fn();
    Questions.prototype.componentWillMount = onWillMount;
    const wrapper = mount(<Questions/>);
    expect(onWillMount).toHaveBeenCalledTimes(1);
});
