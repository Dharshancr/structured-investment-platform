import { Plus, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import api from "../api/client";

const initialForm = {
  name: "",
  issuer: "",
  underlying_asset: "",
  product_type: "Autocallable",
  currency: "USD",
  coupon_rate: "0.08",
  barrier_level: "0.70",
  strike_price: "100.00",
  issue_date: "2026-01-01",
  maturity_date: "2029-01-01",
  risk_rating: "Medium",
  description: "",
};

export default function Products() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [error, setError] = useState("");

  async function loadProducts() {
    const response = await api.get("/products");
    setProducts(response.data);
  }

  useEffect(() => {
    loadProducts();
  }, []);

  async function createProduct(event) {
    event.preventDefault();
    setError("");
    try {
      await api.post("/products", form);
      setForm(initialForm);
      await loadProducts();
    } catch {
      setError("Only admin users can create products.");
    }
  }

  async function deleteProduct(id) {
    await api.delete(`/products/${id}`);
    await loadProducts();
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[360px_1fr]">
      <form onSubmit={createProduct} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="text-base font-semibold text-ink">New product</h2>
        <div className="mt-4 space-y-3">
          {Object.keys(initialForm).map((key) => (
            <input
              key={key}
              placeholder={key.replaceAll("_", " ")}
              value={form[key]}
              onChange={(event) => setForm({ ...form, [key]: event.target.value })}
              required={!["description", "barrier_level"].includes(key)}
            />
          ))}
          {error && <p className="text-sm text-coral">{error}</p>}
          <button className="flex w-full items-center justify-center gap-2 bg-mint px-4 py-2 text-white hover:bg-mint/90">
            <Plus size={16} />
            Create product
          </button>
        </div>
      </form>

      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="text-base font-semibold text-ink">Product catalog</h2>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-slate-500">
              <tr>
                <th className="py-2">Name</th>
                <th className="py-2">Issuer</th>
                <th className="py-2">Underlying</th>
                <th className="py-2">Coupon</th>
                <th className="py-2">Risk</th>
                <th className="py-2"></th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product.id} className="border-t border-slate-100">
                  <td className="py-3 font-medium">{product.name}</td>
                  <td className="py-3">{product.issuer}</td>
                  <td className="py-3">{product.underlying_asset}</td>
                  <td className="py-3">{Number(product.coupon_rate) * 100}%</td>
                  <td className="py-3">{product.risk_rating}</td>
                  <td className="py-3 text-right">
                    <button onClick={() => deleteProduct(product.id)} className="p-2 text-coral hover:bg-red-50" title="Delete product">
                      <Trash2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

