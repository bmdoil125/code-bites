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
        }

    }
    componentDidMount(){
        this.getUsers()
    }
    getUsers() {
        const options = {
            url: `${process.env.REACT_APP_USERS_SERVICE_URL}/users`,
            method: 'get',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${window.localStorage.token}`
            }
        }
        return axios(options)
        .then((res) => {
            this.setState({
                users: res.data.data.users
            })
        })
        .catch((err) => { console.log(err); });
    }

    render() {
        const users = this.state.users;
        return (
            <div>
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
                        HEADER: "Profile",
                        accessor: "self",
                        Cell: d =><a href={d.self}>Profile</a>
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