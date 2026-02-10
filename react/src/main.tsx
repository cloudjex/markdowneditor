import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Loading from '@/src/components/loading/loading';
import Auth from '@/src/views/auth';
import Main from '@/src/views/main';
import Preview from '@/src/views/preview';


export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Auth />} />
        <Route path="/main/:node_id" element={<Main />} />
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
