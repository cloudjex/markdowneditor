import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Loading from '@/src/components/loading/loading';
import Main from '@/src/views/main';
import Preview from '@/src/views/preview';
import Top from '@/src/views/top';
import Verify from '@/src/views/verify';


export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Top />} />
        <Route path="/main/:id" element={<Main />} />
        <Route path="/preview/:id" element={<Preview />} />
        <Route path="/verify" element={<Verify />} />
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