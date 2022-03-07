import React from 'react'
import { Link } from 'react-router-dom'

const GroupMembers = ({ group, handleMemberApprove, handleMemberRemove }) => (  
  <section className="section" id="member-management">
    <div className="container">
      {/* {console.log(group)} */}

      <div className="title is-size-3">Member Management</div>


      <section className="chapter">
        <div className="subtitle">Current Members</div>

        {group.members && group.members
          .filter(member => member.id !== group.owner.id)
          .map((member, i) => {
            return <div className="level" key={i}>
              <Link to={`/profile/${member.id}/`} className="level-left">
                <div className="level-item">
                  <figure className="image is-48x48 member-image" key={i}>
                    <img className="is-rounded" src={member.image} alt="member profile image" />
                  </figure>
                </div>
                <div className="level-item is-size-5 username">
                  <span className="username">{member.username}</span> ({member.first_name} {member.last_name})
                </div>
              </Link>
              <div className="level-right">
                <button className="button level-item is-danger" id={member.id} data-name={member.username} onClick={(e) => handleMemberRemove(e)}>
                  Remove
                </button>
              </div>
            </div>
          })}

        {group.members && group.members
          .filter(member => member.id !== group.owner.id)
          .length === 0 ? 
          <div className="info">No other group members</div> : <></>
        }

      </section>


      <section className="chapter">
        <div className="subtitle">Requests</div>

        {group.requests && group.requests
          .filter(member => member.id !== group.owner.id)
          .map((member, i) => {
            return <div className="level" key={i}>
              <Link to={`/profile/${member.id}/`} className="level-left">
                <div className="level-item">
                  <figure className="image is-48x48 member-image" key={i}>
                    <img className="is-rounded" src={member.image} alt="member profile image" />
                  </figure>
                </div>
                <div className="level-item is-size-5 username">
                  <span className="username">{member.username} </span> ({member.first_name} {member.last_name})
                </div>
              </Link>
              <div className="level-right">
                <button className="button level-item is-link" id={member.id} data-name={member.username} onClick={(e) => handleMemberApprove(e)}>
                  Approve
                </button>
              </div>
            </div>
          })}

        {group.requests && group.requests
          .filter(member => member.id !== group.owner.id)
          .length === 0 ? 
          <div className="info">No requests</div> : <></>
        }

      </section>

    </div>
  </section>
)

export default GroupMembers