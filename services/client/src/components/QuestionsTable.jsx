import React, { Component } from "react";

import ReactTable from 'react-table';
import 'react-table/react-table.css';
import axios from "axios";
import UsersTable from "./UsersTable";
import Questions from "./Questions";

class QuestionsTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            questions: [],
            num_questions: 0,
        }
    }
    componentDidMount(){
        this.getQuestions()
    }

    getQuestions() {
        const options = {
            url: `${process.env.BASE_URL}/questions`,
            method: 'get',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${window.localStorage.token}`
            }
        }
        return axios(options)
        .then((res) => {
            this.setState({
                questions: res.data.data.questions,
                num_questions: res.data.data.num_questions
            })
        })
        .catch((err) => { console.log(err); });
    }

    render() {
        const questions = this.state.questions;
        return (
            <div>
                <button className="button is-primary">Number of Questions: {this.state.num_questions}</button>
                <ReactTable
                data={questions}
                columns={[
                    {
                        Header: "ID",
                        id: "id",
                        accessor: q => q.id
                    },
                    {
                        Header: "AUTHOR ID",
                        id: "author_id",
                        accessor: q => q.author_id
                    },
                    {
                        Header: "BODY",
                        accessor: "body"
                    },
                    {
                        Header: "TEST CODE",
                        accessor: "test_code"
                    },
                    {
                        Header: "SOLUTION",
                        accessor: "test_solution"
                    },
                    {
                        Header: "DIFFICULTY",
                        accessor: "difficulty"
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

export default QuestionsTable