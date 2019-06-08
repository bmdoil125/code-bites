import React from 'react';
import { shallow, mount } from 'enzyme';
import { MemoryRouter as Router } from 'react-router-dom';
import AceEditor from 'react-ace';
jest.mock('react-ace');
import App from '../../App';

beforeAll(() => {
    global.localStorage = {
      getItem: () => 'test'
    };
  });

test('App renders propery', () => {
    const wrapper = shallow(<App/>);
});

test('componentWillMount called', () => {
    const onWillMount = jest.fn();
    App.prototype.componentWillMount = onWillMount;
    const wrapper = mount(<Router><App/></Router>);
    expect(onWillMount).toHaveBeenCalledTimes(1)
    });