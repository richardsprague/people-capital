import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Chart = () => {
  // Hypothetical data for illustration purposes
  // Shows significant SOXX outperformance over S&P 500
  const data = [
    { date: 'Jan 2020', SOXX: 100, SP500: 100 },
    { date: 'Jul 2020', SOXX: 130, SP500: 105 },
    { date: 'Jan 2021', SOXX: 180, SP500: 120 },
    { date: 'Jul 2021', SOXX: 200, SP500: 135 },
    { date: 'Jan 2022', SOXX: 190, SP500: 130 },
    { date: 'Jul 2022', SOXX: 170, SP500: 115 },
    { date: 'Jan 2023', SOXX: 210, SP500: 125 },
    { date: 'Jul 2023', SOXX: 260, SP500: 140 },
    { date: 'Jan 2024', SOXX: 310, SP500: 155 },
    { date: 'Jul 2024', SOXX: 340, SP500: 160 },
    { date: 'Jan 2025', SOXX: 380, SP500: 175 },
  ];

  return (
    <div className="w-full h-full flex flex-col bg-white p-4 rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4 text-center">SOXX vs S&P 500 Total Returns (2020-2025)</h2>
      <p className="text-sm text-gray-600 mb-6 text-center">Indexed to 100 at January 2020</p>
      <div className="flex-grow">
        <ResponsiveContainer width="100%" height="100%" minHeight={300}>
          <LineChart
            data={data}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis domain={[0, 400]} />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="SOXX" 
              stroke="#2563eb" 
              strokeWidth={3} 
              dot={{ r: 4 }} 
              activeDot={{ r: 6 }}
              name="SOXX (Semiconductor ETF)" 
            />
            <Line 
              type="monotone" 
              dataKey="SP500" 
              stroke="#64748b" 
              strokeWidth={3} 
              dot={{ r: 4 }} 
              activeDot={{ r: 6 }}
              name="S&P 500" 
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 text-sm text-gray-600">
        <p>Chart shows the remarkable outperformance of semiconductor stocks compared to the broader market, reflecting the sector's critical role in AI infrastructure development.</p>
      </div>
    </div>
  );
};

export default Chart;