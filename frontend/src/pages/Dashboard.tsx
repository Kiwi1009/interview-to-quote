import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { casesApi, Case } from '../api/cases'
import './Dashboard.css'

export default function Dashboard() {
  const { data: cases, isLoading } = useQuery({
    queryKey: ['cases'],
    queryFn: async () => {
      const response = await casesApi.list()
      return response.data
    },
  })

  const statusLabels: Record<string, string> = {
    draft: '草稿',
    extracting: '提取中',
    reviewing: '審核中',
    quoted: '已報價',
    archived: '已歸檔',
  }

  const statusColors: Record<string, string> = {
    draft: '#95a5a6',
    extracting: '#3498db',
    reviewing: '#f39c12',
    quoted: '#27ae60',
    archived: '#7f8c8d',
  }

  if (isLoading) {
    return <div className="loading">載入中...</div>
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>案件列表</h2>
        <Link to="/cases/new" className="btn btn-primary">
          建立新案件
        </Link>
      </div>
      <div className="cases-grid">
        {cases && cases.length > 0 ? (
          cases.map((caseItem) => (
            <Link
              key={caseItem.id}
              to={`/cases/${caseItem.id}`}
              className="case-card"
            >
              <h3>{caseItem.title}</h3>
              <div className="case-meta">
                {caseItem.industry && (
                  <span className="industry">{caseItem.industry}</span>
                )}
                <span
                  className="status"
                  style={{ backgroundColor: statusColors[caseItem.status] }}
                >
                  {statusLabels[caseItem.status]}
                </span>
              </div>
              <div className="case-date">
                建立時間：{new Date(caseItem.created_at).toLocaleDateString('zh-TW')}
              </div>
            </Link>
          ))
        ) : (
          <div className="empty-state">
            <p>尚無案件，請建立新案件</p>
          </div>
        )}
      </div>
    </div>
  )
}

