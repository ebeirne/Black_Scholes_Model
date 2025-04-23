import React, { useEffect, useState } from 'react'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import About from './components/About'
import Info from './components/Info'
import PriceForm from './components/PriceForm'
import Footer from './components/Footer'

export default function App() {
  const [theme, setTheme] = useState('light')
  useEffect(() => {
    const root = document.documentElement
    root.classList.remove(theme === 'light' ? 'dark' : 'light')
    root.classList.add(theme)
  }, [theme])

  return (
    <div className="bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-200">
      <Navbar theme={theme} setTheme={setTheme} />
      <Hero />
      <About />
      <Info />
      <PriceForm />
      <Footer />
    </div>
  )
}