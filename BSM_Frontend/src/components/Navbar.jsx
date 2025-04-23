import React from 'react'
import ThemeToggle from './ThemeToggle'

export default function Navbar({ theme, setTheme }) {
  return (
    <nav className="fixed top-0 w-full z-50 bg-white dark:bg-gray-800 shadow-md">
      <div className="container mx-auto flex items-center justify-between p-6">
        <span className="text-xl font-bold text-brand">BS-ML</span>
        <div className="flex items-center space-x-6">
          {['Home','About','Info','Pricing','Contact'].map(sec => (
            <a
              key={sec}
              href={`#${sec.toLowerCase()}`}
              className="hover:text-brand"
            >
              {sec}
            </a>
          ))}
          <ThemeToggle theme={theme} setTheme={setTheme} />
        </div>
      </div>
    </nav>
  )
}