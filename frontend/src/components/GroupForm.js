import React from 'react'

const GroupForm = ({ details, errors, handleChange, handleSubmit }) => {

  return <div className=''>
    <div className='container'>
      <div className='columns'>
        <div className='column'>
          <form className='form' onSubmit={e => handleSubmit(e)}>

            <div className="field">
              <p className="control has-icons-left">
                <input
                  onChange={handleChange}
                  className="input has-text-info"
                  name="name"
                  type="text"
                  placeholder="Group name"
                  value={details.name}
                />
                <span className="icon is-small is-left">
                  <i className="fas fa-pencil-alt"></i>
                </span>
              </p>
            </div>
            <div className="field">
              <p className="control">
                <textarea
                  onChange={handleChange}
                  name="description"
                  className="textarea has-text-info"
                  type="textarea"
                  placeholder="Description"
                  value={details.description}
                />
              </p>
            </div>
            {errors && <small className='help is-danger'>
              {errors}
            </small>}
            <button className='button is-link'>
              Submit
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
}

export default GroupForm