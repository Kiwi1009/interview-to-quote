import { useState } from 'react'
import { Requirements } from '../api/extraction'
import { extractionApi } from '../api/extraction'
import './RequirementsEditor.css'

interface RequirementsEditorProps {
  caseId: number
  requirements: Requirements | undefined
  onExtract: () => void
  onUpdate: () => void
}

export default function RequirementsEditor({
  caseId,
  requirements,
  onExtract,
  onUpdate,
}: RequirementsEditorProps) {
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState<Record<string, any>>({})

  const handleExtract = () => {
    onExtract()
  }

  const handleSave = async () => {
    try {
      await extractionApi.updateRequirements(caseId, formData)
      setEditing(false)
      onUpdate()
    } catch (error) {
      console.error('Update failed:', error)
      alert('更新失敗')
    }
  }

  const handleEdit = () => {
    setFormData(requirements?.jsonb_data || {})
    setEditing(true)
  }

  if (!requirements) {
    return (
      <div className="requirements-editor">
        <h3>需求提取</h3>
        <p>請先上傳逐字稿，然後點擊「開始提取」按鈕</p>
        <button onClick={handleExtract} className="btn btn-primary">
          開始提取
        </button>
      </div>
    )
  }

  const reqData = requirements.jsonb_data

  return (
    <div className="requirements-editor">
      <div className="editor-header">
        <h3>提取的需求</h3>
        <div className="editor-actions">
          {!editing ? (
            <button onClick={handleEdit} className="btn btn-secondary">
              編輯
            </button>
          ) : (
            <>
              <button onClick={handleSave} className="btn btn-primary">
                儲存
              </button>
              <button onClick={() => setEditing(false)} className="btn btn-secondary">
                取消
              </button>
            </>
          )}
        </div>
      </div>

      <div className="requirements-content">
        {reqData.customer_pain_points && (
          <section>
            <h4>客戶痛點</h4>
            <ul>
              {reqData.customer_pain_points.map((point: string, idx: number) => (
                <li key={idx}>{point}</li>
              ))}
            </ul>
          </section>
        )}

        {reqData.workpiece && (
          <section>
            <h4>工件資訊</h4>
            <div className="field-grid">
              {Object.entries(reqData.workpiece).map(([key, value]) => (
                <div key={key} className="field">
                  <label>{key}</label>
                  <span>{String(value || 'N/A')}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {reqData.process && (
          <section>
            <h4>製程資訊</h4>
            <div className="field-grid">
              {Object.entries(reqData.process).map(([key, value]) => (
                <div key={key} className="field">
                  <label>{key}</label>
                  <span>{String(value || 'N/A')}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {reqData.open_questions && reqData.open_questions.length > 0 && (
          <section>
            <h4>開放問題</h4>
            <ul>
              {reqData.open_questions.map((q: string, idx: number) => (
                <li key={idx}>{q}</li>
              ))}
            </ul>
          </section>
        )}

        {requirements.evidence && requirements.evidence.length > 0 && (
          <section>
            <h4>證據片段</h4>
            <div className="evidence-list">
              {requirements.evidence.map((ev, idx) => (
                <div key={idx} className="evidence-item">
                  <div className="evidence-field">{ev.field_path}</div>
                  <div className="evidence-snippet">{ev.snippet}</div>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  )
}

