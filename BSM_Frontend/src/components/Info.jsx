import React from 'react'

export default function Info() {
  return (
    <section id="info" className="py-20 px-4 bg-white dark:bg-gray-800">
      <div className="container mx-auto max-w-3xl">
        <h2 className="text-3xl font-bold mb-4 text-center">What is Black-Scholes?</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-6">
          The Black-Scholes model is a mathematical framework for pricing European-style options. It calculates the theoretical value of a call or put option based on factors such as the current price of the underlying asset, the strike price, time to expiration, volatility, and the risk-free interest rate.
        </p>
        <p className="text-gray-700 dark:text-gray-300">
          This website augments Black-Scholes with machine learning by training on real market data to capture deviations and improve pricing accuracy across various strikes and maturities.
        </p>
      </div>
    </section>
  )
}