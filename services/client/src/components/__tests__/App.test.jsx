import React from 'react';
import { shallow } from 'enzyme';

import App from '../../App';

test('App renders propery', () => {
    const wrapper = shallow(<App/>);
});