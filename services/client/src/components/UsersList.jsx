import React from 'react';

// functional component
// props - read only from state -> props
// https://lucybain.com/blog/2016/react-state-vs-pros/

const UsersList = (props) => {
  return (
    <div>
      <h1 className="title is-1">All Users</h1>
      <hr/><br/>
      <table className="table is-hoverable is-fullwidth">
          <thead>
              <tr>
              <th>ID</th>
              <th>USERNAME</th>
              <th>EMAIL</th>
              <th>ACTIVE</th>
              <th>ADMIN</th>
              </tr>
          </thead>
          <tfoot>
              <tr>
              <th>ID</th>
              <th>USERNAME</th>
              <th>EMAIL</th>
              <th>ACTIVE</th>
              <th>ADMIN</th>
              </tr>
          </tfoot>
          <tbody>
          {
              props.users.map((user) => {
                  return (
                      <tr key={user.id}>
                          <td>{user.id}</td>
                          <td>{user.username}</td>
                          <td>{user.email}</td>
                          <td>{String(user.active)}</td>
                          <td>{String(user.admin)}</td>
                      </tr>
                  )
              })
          }
          </tbody>
      </table>
    </div>
  )
};

export default UsersList