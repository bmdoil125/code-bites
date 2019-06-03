import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios'
import UsersList from './components/UsersList'
/* 
Class based component. Runs when instance is created.
super() calls constructor of Component
*/
class App extends Component {
    constructor() {
        super();
        // adds state property to class, state begins as empty array
        this.state = {
            users: []
        };
    };
    // Avoids race condition, fire after DOM rendered
    componentDidMount() {
        this.getUsers();
    };

    render() {
        return (
            <section className="section">
                <div className="container">
                    <div className="column is-one-third">
                        <br/>
                        <h1 className="title is-1 is-1">All Users</h1>
                        <hr/><br/>
                        <UsersList users={this.state.users}/>
                    </div>
                </div>
            </section>
        )
    }

    getUsers() {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
        .then((res) => { this.setState({ users: res.data.data.users }); })
        .catch((err) => { console.log(err); });
    }
};

// Mount App to DOM of HTML element root
ReactDOM.render(<App />, document.getElementById('root'));


