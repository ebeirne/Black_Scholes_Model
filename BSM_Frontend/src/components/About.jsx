import React from 'react'

export default function About() {
  return (
    <section id="about" className="py-20 px-4">
      <div className="container mx-auto max-w-3xl text-center">
        <h2 className="text-3xl font-bold mb-6">Why Choose ML Pricing?</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-8">
          Combining statistical rigor of Black-Scholes with the adaptability of machine learning, our model learns market patterns for more accurate pricing across strikes and maturities.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { title: 'Data-Driven', desc: 'Learns from real-market option chains.' },
            { title: 'Fast', desc: 'Predicts prices in milliseconds.' },
            { title: 'Adaptive', desc: 'Updates daily with fresh data.' }
          ].map(item => (
            <div key={item.title} className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow">
              <h3 className="font-semibold text-xl mb-2 text-brand">{item.title}</h3>
              <p className="text-gray-600 dark:text-gray-400">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}