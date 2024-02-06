import React from 'react'

function Navbar({flag,handelClick}) {

  

  return (
    <>
<div className="navbar bg-slate-700 shadow-md" style={{ zIndex: 1000 }}>
  <div className="flex-1">
    <a className="btn btn-ghost normal-case text-xl">Jinsei</a>
  </div>
  <div className="flex-none">
    <button onClick={handelClick} className='btn' >{!flag ? "Analyze":"Casual"}</button> {/*add button to logout logic*/}
  </div>
</div>
    </>
  )
}

export default Navbar