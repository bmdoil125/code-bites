import React from 'react';

// functional component
// props - read only from state -> props
// https://lucybain.com/blog/2016/react-state-vs-pros/

const UsersList = (props) => {
    return (
        <div>
            {
                props.users.map((user) => {
                    return (
                        <h4
                        key={user.id}
                        className="box title is-4"
                        >{ user.username }
                        </h4>
                    )
                })
            }
        </div>
    )
};

export default UsersList