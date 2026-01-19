import { useState, useEffect } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Line } from 'react-chartjs-2'
import './App.css'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const API_BASE = 'http://127.0.0.1:8000'

function App() {
  const [companies, setCompanies] = useState([])
  const [selectedCompany, setSelectedCompany] = useState(null)
  const [stockData, setStockData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchCompanies()
  }, [])

  const fetchCompanies = async () => {
    try {
      const response = await fetch(`${API_BASE}/companies/`)
      if (!response.ok) throw new Error('Failed to fetch companies')
      const data = await response.json()
      setCompanies(data)
    } catch (err) {
      setError(err.message)
    }
  }

  const fetchStockData = async (symbol) => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE}/data/${symbol}`)
      console.log("response of stock data")
      if (!response.ok) throw new Error('Failed to fetch stock data')
      const data = await response.json()
      console.log("data res- ",data)
      setStockData(data.stock_data)
      setSelectedCompany(symbol)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const chartData = stockData ? {
    labels: stockData.map(item => item.date),
    datasets: [
      {
        label: 'Closing Price',
        data: stockData.map(item => item.close),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1,
      },
    ],
  } : null

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: selectedCompany ? `${selectedCompany} Stock Price (Last 30 Days)` : 'Stock Price Chart',
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  }

  return (
    <div className="app">
      <div className="sidebar">
        <h2>Companies</h2>
        {error && <div className="error">Error: {error}</div>}
        <ul className="company-list">
          {companies.map((company, index) => (
            console.log(company),
            <li
              key={index}
              className={`company-item ${selectedCompany === company.symbol ? 'selected' : ''}`}
              onClick={() => fetchStockData(company.symbol)}
            >
              {company.symbol}
            </li>
          ))}
        </ul>
      </div>
      <div className="main-content">
        <h1>Stock Data Intelligence</h1>
        {loading && <div className="loading">Loading...</div>}
        {chartData && (
          <div className="chart-container">
            <Line data={chartData} options={chartOptions} />
          </div>
        )}
        {!chartData && !loading && (
          <div className="placeholder">
            <p>Select a company from the list to view its stock price chart</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
