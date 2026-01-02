import { Document } from '../api/documents'
import { documentsApi } from '../api/documents'
import './DocumentsPanel.css'

interface DocumentsPanelProps {
  caseId: number
  documents: Document[]
  onGenerate: () => void
}

export default function DocumentsPanel({ documents, onGenerate }: DocumentsPanelProps) {
  const handleDownload = async (docId: number, filename: string) => {
    try {
      const response = await documentsApi.download(docId)
      const blob = new Blob([response.data])
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Download failed:', error)
      alert('下載失敗')
    }
  }

  const getDocTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      spec: '需求規格書',
      report: '需求報告表',
      quote: '報價單',
    }
    return labels[type] || type
  }

  const getFormatLabel = (format: string) => {
    return format.toUpperCase()
  }

  return (
    <div className="documents-panel">
      <div className="documents-header">
        <h3>文件下載</h3>
        <button onClick={onGenerate} className="btn btn-primary">
          產生文件
        </button>
      </div>

      {documents.length > 0 ? (
        <div className="documents-list">
          <table>
            <thead>
              <tr>
                <th>文件類型</th>
                <th>格式</th>
                <th>產生時間</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              {documents.map((doc) => (
                <tr key={doc.id}>
                  <td>{getDocTypeLabel(doc.doc_type)}</td>
                  <td>{getFormatLabel(doc.format)}</td>
                  <td>{new Date(doc.created_at).toLocaleString('zh-TW')}</td>
                  <td>
                    <button
                      onClick={() => handleDownload(doc.id, `${doc.doc_type}_${doc.id}.${doc.format}`)}
                      className="btn-download"
                    >
                      下載
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="empty-state">
          <p>尚未產生任何文件</p>
          <p className="hint">請先完成需求提取和方案產生，然後點擊「產生文件」按鈕</p>
        </div>
      )}
    </div>
  )
}

