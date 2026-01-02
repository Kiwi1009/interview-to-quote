import { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import './Layout.css'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="layout">
      <header className="header">
        <Link to="/" className="logo">
          <h1>訪談轉報價平台</h1>
        </Link>
        <nav>
          <Link to="/">案件列表</Link>
        </nav>
      </header>
      <main className="main">
        {children}
      </main>
    </div>
  )
}

