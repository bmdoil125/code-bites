import React from 'react';

// functional component
// props - read only from state -> props
// https://lucybain.com/blog/2016/react-state-vs-pros/

const UsersList = (props) => {
    return (
            props.users.map((user) => {
                return (
                    <tr key={user.id}>
                        <th>{user.id}</th>
                        <th>{user.username}</th>
                        <th>{user.email}</th>
                    </tr>
                )
            })
    )
};

export default UsersList