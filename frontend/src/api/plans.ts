import apiClient from './client'

export interface QuoteItem {
  id: number
  category: string
  item_name: string
  spec: string | null
  qty: number
  unit: string
  unit_price_low: number
  unit_price_high: number
  subtotal_low: number | null
  subtotal_high: number | null
}

export interface Plan {
  id: number
  case_id: number
  run_id: number | null
  plan_code: 'P1' | 'P2' | 'P3'
  name: string
  assumptions_jsonb: Record<string, any> | null
  quote_items: QuoteItem[]
  created_at: string
}

export const plansApi = {
  generate: (caseId: number, runId?: number) =>
    apiClient.post<Plan[]>(`/cases/${caseId}/generate-plans`, null, { params: { run_id: runId } }),
  list: (caseId: number, runId?: number) =>
    apiClient.get<Plan[]>(`/cases/${caseId}/plans`, { params: { run_id: runId } }),
  update: (planId: number, data: Partial<Plan>) =>
    apiClient.put<Plan>(`/plans/${planId}`, data),
}

