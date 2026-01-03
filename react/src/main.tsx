import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Loading from './components/loading';
import Information from './views/information';
import Main from './views/main';
import Top from './views/top';
import Verify from './views/verify';

function NotFound() {
  return <h1>404</h1>;
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Top />} />
        <Route path="/main" element={<Main />} />
        <Route path="/information" element={<Information />} />
        <Route path="/verify" element={<Verify />} />
        <Route path="*" element={<NotFound />} />
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