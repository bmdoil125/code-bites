import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Signout extends Component {
    componentDidMount() {
        this.props.signoutUser();
    };
    render() {
        return (
            <div>
                <p>Signed Out. <Link to="/login">Login.</Link></p>
            </div>
        )
    };
};

export default Signout;