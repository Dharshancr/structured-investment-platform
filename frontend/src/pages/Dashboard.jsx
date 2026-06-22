import { useEffect, useState } from "react";
import api from "../api/client";

export default function Dashboard() {
  const [holdings, setHoldings] = useState([]);
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    Promise.all([api.get("/holdings"), api.get("/transactions")]).then(([holdingsResponse, transactionsResponse]) => {
      setHoldings(holdingsResponse.data);
      setTransactions(transactionsResponse.data);
    });
  }, []);

  const totalValue = holdings.reduce((sum, holding) => sum + Number(holding.current_value), 0);

  return (
    <div className="space-y-6">
      <section className="grid gap-4 md:grid-cols-3">
        <Metric label="Portfolio value" value={`$${totalValue.toLocaleString()}`} />
        <Metric label="Holdings" value={holdings.length} />
        <Metric label="Transactions" value={transactions.length} />
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="text-base font-semibold text-ink">Portfolio holdings</h2>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-slate-500">
              <tr>
                <th className="py-2">Product</th>
                <th className="py-2">Quantity</th>
                <th className="py-2">Average price</th>
                <th className="py-2">Current value</th>
              </tr>
            </thead>
            <tbody>
              {holdings.map((holding) => (
                <tr key={holding.id} className="border-t border-slate-100">
                  <td className="py-3">{holding.product.name}</td>
                  <td className="py-3">{holding.quantity}</td>
                  <td className="py-3">${holding.average_price}</td>
                  <td className="py-3">${holding.current_value}</td>
                </tr>
              ))}
              {holdings.length === 0 && (
                <tr>
                  <td colSpan="4" className="py-8 text-center text-slate-500">No holdings yet.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-ink">{value}</p>
    </div>
  );
}

