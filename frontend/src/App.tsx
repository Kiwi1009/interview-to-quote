import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import CaseDetail from './pages/CaseDetail'
import SimpleUpload from './pages/SimpleUpload'
import Layout from './components/Layout'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/simple" element={<SimpleUpload />} />
        <Route path="/" element={<Layout><Dashboard /></Layout>} />
        <Route path="/cases/:caseId" element={<Layout><CaseDetail /></Layout>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

