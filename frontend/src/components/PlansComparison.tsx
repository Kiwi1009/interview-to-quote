import { Plan } from '../api/plans'
import './PlansComparison.css'

interface PlansComparisonProps {
  caseId: number
  plans: Plan[]
  onGenerate: () => void
}

export default function PlansComparison({ plans, onGenerate }: PlansComparisonProps) {
  const calculateTotal = (plan: Plan) => {
    const subtotalLow = plan.quote_items.reduce((sum, item) => sum + (item.subtotal_low || 0), 0)
    const subtotalHigh = plan.quote_items.reduce((sum, item) => sum + (item.subtotal_high || 0), 0)
    const contingency = subtotalLow * 0.1
    return {
      subtotalLow,
      subtotalHigh,
      contingency,
      totalLow: subtotalLow + contingency,
      totalHigh: subtotalHigh + contingency,
    }
  }

  if (plans.length === 0) {
    return (
      <div className="plans-comparison">
        <h3>報價方案</h3>
        <p>尚未產生報價方案，請點擊「產生方案」按鈕</p>
        <button onClick={onGenerate} className="btn btn-primary">
          產生方案
        </button>
      </div>
    )
  }

  return (
    <div className="plans-comparison">
      <div className="plans-header">
        <h3>報價方案比較</h3>
        <button onClick={onGenerate} className="btn btn-secondary">
          重新產生
        </button>
      </div>

      <div className="plans-grid">
        {plans.map((plan) => {
          const totals = calculateTotal(plan)
          return (
            <div key={plan.id} className="plan-card">
              <div className="plan-header">
                <h4>{plan.plan_code} - {plan.name}</h4>
              </div>

              <div className="plan-items">
                <table>
                  <thead>
                    <tr>
                      <th>項目</th>
                      <th>數量</th>
                      <th>單價</th>
                      <th>小計</th>
                    </tr>
                  </thead>
                  <tbody>
                    {plan.quote_items.map((item) => (
                      <tr key={item.id}>
                        <td>
                          <div className="item-name">{item.item_name}</div>
                          {item.spec && (
                            <div className="item-spec">{item.spec}</div>
                          )}
                        </td>
                        <td>{item.qty} {item.unit}</td>
                        <td>
                          ${item.unit_price_low.toLocaleString()} - ${item.unit_price_high.toLocaleString()}
                        </td>
                        <td>
                          ${(item.subtotal_low || 0).toLocaleString()} - ${(item.subtotal_high || 0).toLocaleString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="plan-totals">
                <div className="total-row">
                  <span>小計</span>
                  <span>${totals.subtotalLow.toLocaleString()} - ${totals.subtotalHigh.toLocaleString()}</span>
                </div>
                <div className="total-row">
                  <span>預備費（10%）</span>
                  <span>${totals.contingency.toLocaleString()}</span>
                </div>
                <div className="total-row total-final">
                  <span>合計</span>
                  <span>${totals.totalLow.toLocaleString()} - ${totals.totalHigh.toLocaleString()}</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

