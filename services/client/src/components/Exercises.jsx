import React, { Component } from 'react';
import AceEditor from 'react-ace';
import 'brace/mode/python';
import 'brace/theme/solarized_dark';

class Exercises extends Component {
    constructor(props) {
        super(props);
        this.state = {
            exercises: [],
            editor: {
                value: '# Enter your code here.'
            },
        };
        this.onChange = this.onChange.bind(this);
        this.submitExercise = this.submitExercise.bind(this);
    };
    componentDidMount() {
        this.getExercises();
    };
    onChange(value) {
        this.setState({
            editor: {
                value: value
            }
        });
    };

    submitExercise(event) {
        event.preventDefault();
        console.log(this.state.editor.value);
    }
    render() {
        return (
            <div>
                <h1 className="title is-1">Exercises</h1>
                <hr/><br/>
                {!this.props.isAuthenticated && 
                    <div className="notification is-warning">
                        <span>Register or Login to submit a code exercise.</span>
                    </div>    
                }
                {this.state.exercises.length &&
                    <div key={this.state.exercises[0].id}>
                        <h5 className="title is-5">{this.state.exercises[0].body}</h5>
                        <AceEditor
                            mode="python"
                            theme="solarized_dark"
                            name={(this.state.exercises[0].id).toString()}
                            onLoad={this.onLoad}
                            fontSize={18}
                            height={'350px'}
                            showPrintMargin={true}
                            showGutter={true}
                            highlightActiveLine={true}
                            value={this.state.editor.value}
                            style={{
                                marginBottom: '10px'
                            }}
                            editorProps={{
                                $blockScrolling: Infinity
                            }}
                            onChange={this.onChange}
                        />
                        {this.props.isAuthenticated &&
                            <button className="button is-primary" onClick={this.submitExercise}>Run</button>
                        }

                        <br/><br/>
                    </div>
                }
            </div>
        )
    };

    getExercises() {
        const exercises = [
            {
                id: 0,
                body: 'Define a function called factorial that takes two integers as arguments and returns the factorial of that number.',
            },
            {
                id: 1,
                body: 'Define a function reverse that takes a string as an argument and returns the string in the reversed order.',
            }
        ];
        this.setState({exercises:exercises});
    }
}

export default Exercises;