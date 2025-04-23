import React from 'react'
import { motion } from 'framer-motion'

export default function Hero() {
  return (
    <section
      id="home"
      className="h-screen flex items-center justify-center bg-gradient-to-r from-brand-light to-brand-dark"
    >
      <div className="text-center px-4">
        <motion.h1
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="text-5xl md:text-6xl font-extrabold text-white mb-4"
        >Black-Scholes ML Pricer</motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="text-lg md:text-xl text-gray-200 mb-8"
        >Real-time, data-driven option price predictions</motion.p>
        <motion.a
          href="#pricing"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 1, type: 'spring', stiffness: 120 }}
          className="inline-block px-8 py-3 bg-white text-brand font-semibold rounded-full"
        >Get Started</motion.a>
      </div>
    </section>
  )
}