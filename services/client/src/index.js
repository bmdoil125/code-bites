import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios'
import UsersList from './components/UsersList'
import AddUser from './components/AddUser'

/* 
Class based component. Runs when instance is created.
super() calls constructor of Component
*/
class App extends Component {
    constructor() {
        super();
        // adds state property to class, state begins as empty array
        this.state = {
            users: [],
            username: 'test',
            email: 'test',
        };
        // https://reactjs.org/docs/handling-events.html
        this.addUser = this.addUser.bind(this); // binds the context of 'this' 
        this.handleChange = this.handleChange.bind(this)
    };
    // Avoids race condition, fire after DOM rendered
    componentDidMount() {
        this.getUsers();
    };

    handleChange(event) {
        const obj = {};
        obj[event.target.name] = event.target.value;
        this.setState(obj)
    }
    addUser(event) {
        event.preventDefault();
        // bundle up the data
        const data = {
            username: this.state.username,
            email: this.state.email
        };
        // ajax request to backend
        axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data)
        .then((res) => { 
            this.getUsers(); //update users list
            this.setState( {username: '', email: '' }) }) //reset form state
        .catch((err) => { console.log(err); });
    };

    render() {
        return (
            <section className="section">
                <div className="container">
                    <div className="column is-half">
                        <br/>
                        <h1 className="title is-1 is-1">All Users</h1>
                        <hr/><br/>
                        <AddUser 
                            username={this.state.username}
                            email={this.state.email}
                            addUser={this.addUser}
                            handleChange={this.handleChange}
                            />
                        <br/><br/>
                        <UsersList users={this.state.users}/> 
                    </div>
                </div>
            </section>
        )
    };

    getUsers() {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
        .then((res) => { this.setState({ users: res.data.data.users }); })
        .catch((err) => { console.log(err); });
    };


};

// Mount App to DOM of HTML element root
ReactDOM.render(<App />, document.getElementById('root'));


