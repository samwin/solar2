import React from 'react'
import Navbar from '../components/landing_comp/navbar'
import Chatbox from '../components/landing_comp/chatbot'

function Chatbotpage() {
  const [flag, setflag] = React.useState(false)

  const handelClick = () => {
    setflag(!flag)
  }
  return (
    <>
    <Navbar flag={flag} handelClick={handelClick}/>
    <Chatbox flag={flag}/>
    </>
  )
}

export default Chatbotpage