import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Loading from '@/src/components/loading/loading';
import Auth from '@/src/views/auth';
import Node from '@/src/views/node';
import Preview from '@/src/views/preview';


export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Auth />} />
        <Route path="/node/:node_id" element={<Node />} />
        <Route path="/preview/:node_id" element={<Preview />} />
      </Routes>
    </Router>
  );
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Loading />
    <App />
  </StrictMode>
);
