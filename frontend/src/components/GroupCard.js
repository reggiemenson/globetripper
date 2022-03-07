import React from 'react'
import Auth from '../lib/Auth'

const GroupCard = ({ group, goToGroupProfile, sendRequest }) => (
  <div id="group-card" className="column is-one-fifth-desktop is-one-quarter-tablet is-half-mobile">
    <div className="card">

      
      <div className="card-content">
        <div className="media">
          <div className="media-content">
            <figure className="image is-48x48">
              <img className="is-rounded" src={group.image} alt="group profile image" />
            </figure>
          </div>

          {group.owner.id === Auth.getUserId() ? <div className="media-right">
            <i className="fas fa-crown is-size-5" />
          </div> : <></>
          }

        </div>
        <div className="media">
          <div className="media-content">
            <p className="subtitle is-5">{group.name}</p>
            <p className="text">{group.description}</p>
          </div>
        </div>

        <div className="media">
          {group.members.map((member, i) => {
            return <figure className="image is-48x48 member-image" key={i}>
              <img className="is-rounded" src={member.image} alt="member profile image" />
            </figure>
          })}
        </div>
      </div>

      <footer className="card-footer">
        <a 
          className="card-footer-item is-size-5"
          onClick={(e) => goToGroupProfile(e)}
          id={group.id}  
        >
          <i 
            className="fas fa-info-circle"
            onClick={(e) => goToGroupProfile(e)}
            id={group.id}  
          />
        </a>

        {!group.requests
          .reduce((list, member) => {
            list.push(member.id)
            return list
          }, [])
          .includes(Auth.getUserId()) &&
          !group.members
            .reduce((list, member) => {
              list.push(member.id)
              return list
            }, [])
            .includes(Auth.getUserId()) ? <a 
            className="card-footer-item"
            onClick={(e) => sendRequest(e)}
            id={group.id}   
          >
            <i 
              className="fas fa-paper-plane is-size-5"
              id={group.id}   
            />
          </a> : <></>
        }

        {group.requests
          .reduce((list, member) => {
            list.push(member.id)
            return list
          }, [])
          .includes(Auth.getUserId()) ? <a 
            className="card-footer-item pending"
          >
            <i 
              className="fas fa-clock is-size-5 pending" 
              id={group.id}
            />
          </a> : <></>
        }
        
      </footer>
    </div>
  </div>
)

export default GroupCard