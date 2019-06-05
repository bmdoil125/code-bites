import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';
import UsersList from './components/UsersList';
import AddUser from './components/AddUser';
import About from './components/About';

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
            username: '',
            email: '',
            password: '',
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
            email: this.state.email,
            password: this.state.password,
        };
        // ajax request to backend
        axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data)
        .then((res) => { 
            this.getUsers(); //update users list
            this.setState( {username: '', email: '', password: '' }) }) //reset form state
        .catch((err) => { console.log(err.response); });
    };

    render() {
        return (
            <section className="section">
                <div className="container">
                    <div className="columns">
                    <div className="column is-three-quarters">
                        <br/>
                        <Switch> 
                            <Route exact path='/' render={() => (
                                <div>
                                    <h1 className="title is-1 is-1">All Users</h1>
                                    <hr/><br/>
                                    <AddUser 
                                        username={this.state.username}
                                        email={this.state.email}
                                        addUser={this.addUser}
                                        handleChange={this.handleChange}
                                    />
                                    <br/><br/>
                                    <table className="table">
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>USERNAME</th>
                                            <th>EMAIL</th>
                                        </tr>
                                    </thead>
                                    <tfoot>
                                        <tr>
                                            <th>ID</th>
                                            <th>USERNAME</th>
                                            <th>EMAIL</th> 
                                        </tr>
                                    </tfoot>
                                    <tbody>
                                    <UsersList users={this.state.users}/>
                                    </tbody>
                                    </table>
                                </div>
                            )}/>
                        <Route exact path='/about' component={About}/> 
                        </Switch>
                    </div>                         
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

export default App;