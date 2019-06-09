import React, { Component } from "react";

import ReactTable from 'react-table';
import 'react-table/react-table.css';
import axios from "axios";
import CurrentUser from "./CurrentUser";


class UsersTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            users: [],
            num_users: 0,
        }

    }
    componentDidMount(){
        this.getUsers()
    }
    getUsers() {
        const options = {
            url: `${process.env.REACT_APP_SERVER_SERVICE_URL}/users`,
            method: 'get',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${window.localStorage.token}`
            }
        }
        return axios(options)
        .then((res) => {
            this.setState({
                users: res.data.data.users,
                num_users: res.data.data.num_users
            })
        })
        .catch((err) => { console.log(err); });
    }

    render() {
        const users = this.state.users;
        return (
            <div>
                <button className="button is-primary">Number of Users: {this.state.num_users}</button>
                <ReactTable
                data={users}
                columns={[
                    {
                        Header: "ID",
                        id: "id",
                            accessor: d => d.id
                    },
                    {
                        Header: "USERNAME",
                        accessor: "username"
                    },
                    {
                        Header: "EMAIL",
                        accessor: "email"
                    },
                    {
                        Header: "RESOURCE ENDPOINT",
                        accessor: "self"
                    }
                ]}
                defaultPageSize={5}
                className="-striped -highlight"
                />
            </div>
        )
    }
}

export default UsersTable