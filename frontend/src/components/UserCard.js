import React from 'react'
import Auth from '../lib/Auth'
import { Link } from 'react-router-dom'

const UserCard = ({ user, toggleSearch }) => (

  <Link to={`/reroute/${user.id}/`} id = "user-card" onClick={toggleSearch} className = "column is-one-quarter-desktop is-one-quarter-tablet is-half-mobile" >
    <div className="card">

      <div className="card-content">
        <div className="media">
          <div className="media-content">
            <figure className="image is-48x48">
              <img className="is-rounded" src={user.image} alt="profile image" />
            </figure>
          </div>

          {user.id === Auth.getUserId() ? <div className="media-right">
            <i className="fas fa-crown is-size-5" />
          </div> : <></>
          }

        </div>
        <div className="media">
          <div className="media-content">
            <p className="subtitle is-5">{user.username}</p>
            <p className="text">{user.first_name} {user.last_name}</p>
          </div>
        </div>
      </div>
    </div>
  </Link >
)

export default UserCard