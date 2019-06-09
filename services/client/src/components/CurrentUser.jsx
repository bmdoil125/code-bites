import React, { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom'

// This is a class based component with its own internal state
class CurrentUser extends Component {
    constructor(props) {
        super(props);
        this.state = {
        email: '',
        id: '',
        username: '',
        active: '',
        admin: ''
        };
    };

    componentDidMount() {
        if (this.props.isAuthenticated) {
            this.getCurrentUser();
        }       
    };

    getCurrentUser(event) {
        const options = {
            url: `${process.env.BASE_URL}/login/me`,
            method: 'get',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${window.localStorage.token}`
            }
        }
        return axios(options)
        .then((res) => { 
            this.setState({
                email: res.data.data.email,
                id: res.data.data.id,
                username: res.data.data.username,
                active: String(res.data.data.active),
                admin: String(res.data.data.admin),
            }) 
        })
        .catch((err) => { console.log(err); });
    };
    render() {
        //Hide links if user is not logged in
        if (!this.props.isAuthenticated) {
            return (
                <p>You must be logged in to view this page. Login <Link to="/login">here.</Link></p>
            )
        };
        return (
            <div>
                <ul>
                    <li><strong>User ID:</strong> {this.state.id}</li>
                    <li><strong>Username:</strong> {this.state.username}</li>
                    <li><strong>Email:</strong> {this.state.email}</li>
                    <li><strong>Active:</strong> {this.state.active}</li>
                    <li><strong>Admin:</strong> {this.state.admin} </li>
                </ul>              
            </div>
        )
    };
};

export default CurrentUser;