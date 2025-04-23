import React, { useState } from 'react'

export default function PriceForm() {
  const [symbol, setSymbol] = useState('AAPL')
  const [strike, setStrike] = useState(150)
  const [expiration, setExpiration] = useState('2025-05-16')
  const [optionType, setOptionType] = useState(1)
  const [price, setPrice] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol, strike, expiration, option_type: optionType })
      })
      const data = await res.json()
      setPrice(parseFloat(data.predicted_price).toFixed(4))
    } catch {
      setPrice('Error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section id="pricing" className="py-20 px-4">
      <div className="container mx-auto max-w-lg bg-gray-100 dark:bg-gray-900 rounded-3xl shadow-xl p-8">
        <h2 className="text-2xl font-bold mb-6 text-center">Get Your Price</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Symbol</label>
            <input
              className="mt-1 block w-full p-2 border rounded-lg bg-white dark:bg-gray-700"
              value={symbol}
              onChange={e => setSymbol(e.target.value.toUpperCase())}
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Strike</label>
            <input
              type="number"
              className="mt-1 block w-full p-2 border rounded-lg bg-white dark:bg-gray-700"
              value={strike}
              onChange={e => setStrike(Number(e.target.value))}
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Expiration</label>
            <input
              type="date"
              className="mt-1 block w-full p-2 border rounded-lg bg-white dark:bg-gray-700"
              value={expiration}
              onChange={e => setExpiration(e.target.value)}
            />
          </div>
          <div>
            <span className="block text-sm font-medium">Type</span>
            <select
              className="mt-1 block w-full p-2 border rounded-lg bg-white dark:bg-gray-700"
              value={optionType}
              onChange={e => setOptionType(Number(e.target.value))}
            >
              <option value={1}>Call</option>
              <option value={0}>Put</option>
            </select>
          </div>
          <button
            type="submit"
            className="w-full py-2 bg-brand text-white rounded-full font-semibold disabled:opacity-50"
            disabled={loading}
          >
            {loading ? 'Pricing...' : 'Calculate'}
          </button>
        </form>
        {price !== null && (
          <div className="mt-6 text-center text-xl">
            Predicted Price: <span className="font-bold text-brand">{price}</span>
          </div>
        )}
      </div>
    </section>
  )
}