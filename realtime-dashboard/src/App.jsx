import React, { useEffect, useState, useRef } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function App() {
  const [trades, setTrades] = useState([]);
  const [minSize, setMinSize] = useState(0);
  const [minPrice, setMinPrice] = useState(0);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8000/ws");

    ws.current.onopen = () => {
      console.log("✅ WebSocket connected");
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setTrades((prev) => [data, ...prev].slice(0, 20));
    };

    ws.current.onclose = () => {
      console.log("WebSocket disconnected");
    };

    return () => {
      ws.current.close();
    };
  }, []);

  // Filter trades
  const filteredTrades = trades.filter(
    (trade) => trade.s >= minSize && trade.p >= minPrice
  );

  const chartData = filteredTrades
  .map((trade) => ({
    price: trade.p,
    time: new Date(trade.t).toLocaleTimeString(),
    size: trade.s,
  }))
  .reverse(); // So data flows left-to-right in the chart




  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h1>Realtime AAPL Trades</h1>

      {/* Filter Inputs */}
      <div style={{ marginBottom: 20 }}>
        <label style={{ marginRight: 10 }}>
          Min Size:
          <input
            type="number"
            value={minSize}
            onChange={(e) => setMinSize(Number(e.target.value))}
            style={{ marginLeft: 5 }}
          />
        </label>

        <label style={{ marginRight: 10 }}>
          Min Price:
          <input
            type="number"
            value={minPrice}
            onChange={(e) => setMinPrice(Number(e.target.value))}
            style={{ marginLeft: 5 }}
          />
        </label>
      </div>
      <h2>Price Over Time</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis domain={['auto', 'auto']} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#8884d8"
            dot={({ payload }) =>
              payload.size >= 1000 ? { r: 6, fill: "red" } : { r: 3 }
            }
          />
        </LineChart>
      </ResponsiveContainer>

      {/* Trades Table */}
      <table border="1" cellPadding="5" cellSpacing="0">
        <thead>
          <tr>
            <th>Price</th>
            <th>Size</th>
            <th>Timestamp (UTC)</th>
          </tr>
        </thead>
        <tbody>
          {filteredTrades.map(({ p, s, t }, i) => (
            <tr key={i} style={{ fontWeight: s >= 1000 ? "bold" : "normal" }}>
              <td>${p.toFixed(2)}</td>
              <td>{s}</td>
              <td>{new Date(t).toISOString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
