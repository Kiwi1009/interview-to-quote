import { Link } from 'react-router-dom'
import './SimpleHeader.css'

export default function SimpleHeader() {
  return (
    <header className="simple-header">
      <Link to="/simple" className="logo">
        <h1>訪談轉報價平台</h1>
      </Link>
      <nav>
        <Link to="/simple">簡易上傳</Link>
        <Link to="/">完整功能</Link>
      </nav>
    </header>
  )
}

