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
  const [selectedCompany, setSelectedCompany] = useState()
  const [stockData, setStockData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [summary, setSummary]=useState();
  const [company2, setCompany2]=useState(null);

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
    setCompany2("")
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

  const emptyChartData = {
  labels: [],
  datasets: [
    {
      label: 'Closing Price',
      data: [],
      borderColor: 'rgba(200,200,200,0.5)',
      backgroundColor: 'rgba(200,200,200,0.1)',
      tension: 0.1,
    },
  ],
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
    maintainAspectRatio: false,
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
//fetch summary of company
  // useEffect(()=>{
  //   try{
  //     const response= await
  //   }catch(e){
  //     console.log("error during fetch summary-", e);
  //   }
  // },[chartData])
  const fetchSummary= async(symbol)=>{
    setLoading(true)
    setError(null)
    try{
      const res= await fetch(`${API_BASE}/summary/${symbol}`)
      const data= await res.json()
      console.log("res of summary- ", data);
      setSummary(data?.summary);
    }catch(e){
      console.log("error in fetch summary -", e);
    }
  }

const fieldMap = [
  {key: "date", label: 'Date'},
  {key: "open", label: 'Open Price'},
  {key: "close", label: 'Close Price'},
  {key: "high", label: 'High'},
  {key: "low", label: 'Low'},
  {key: "daily_return", label: 'Daily Return'},
  {key: "ma_7", label: '7 Day MA'},
  {key: "week52_high", label: '52W High'},
  {key: "week52_low", label: '52W Low'},
];

//compare between 2 company fetch
useEffect(()=>{
  if(!selectedCompany || !company2) return;

  const fetchCompare = async () => {
    try {
      const res = await fetch(
        `${API_BASE}/compare/?symbol1=${selectedCompany}&symbol2=${company2}`
      );
      const data = await res.json();
      console.log("compare result:", data);
    } catch (e) {
      console.log("error in fetch compare - ", e);
    }
  };

  fetchCompare();

},[company2])

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
              onClick={() => (
                fetchStockData(company.symbol),
                fetchSummary(company.symbol)
              )}
            >
              {company.symbol}
            </li>
          ))}
        </ul>
      </div>
      <div className="main-content">
        {/* <h1>Stock Data Intelligence</h1> */}
        {loading && <div className="loading">Loading...</div>}
        <div className='upper-content'>
          <div className="chart-container">
            {chartData && (
                <Line data={chartData} options={chartOptions} />
            )}
          </div>
          <div className='summary-content'>
            <h1>summary</h1>
            {summary && 
              <div className='summary-data'>
                <h4>52 Week High :<span style={{color:"black"}}>{summary.week52_high.toFixed(2)}</span></h4>
                <h4>52 Week Low :<span style={{color:"black"}}>{summary.week52_low.toFixed(2)}</span></h4>
                <h4>7 Day Moving Average:<span style={{color:"black"}}>{summary.ma_7.toFixed(2)}</span></h4>
              </div>
            }
          </div>
          <div className='compare-content'>
            <h1>Compare</h1>
            {stockData &&
              <div className='compare-set'>
                <p>Compare {selectedCompany} with:</p>
                <select value={company2} onChange={(e)=>setCompany2(e.target.value)}>
                  <option value="">Select company</option>
                  {companies
                    .filter(company => company.symbol !== selectedCompany)
                    .map(company => (
                      <option key={company.symbol} value={company.symbol}>
                        {company.symbol}
                      </option>
                    ))}
                </select>
              </div>
            }
            <div className='compare-data'>
              <p>Winner is Tcs</p>
            </div>
          </div>
        </div>

        <div className="">
          <h1>Stock Details</h1>

          {/* {chartData&& */}
            <table className="detail-table">
              <thead>
                <tr >
                  {fieldMap.map(({key,label})=>(
                      <th key={key}>{label}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {chartData && stockData.map((row) => (
                  <tr key={row.id}>
                    {fieldMap.map(({ key }) => (
                      <td key={key}>
                        {row[key]}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          {/* } */}
        </div>
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
