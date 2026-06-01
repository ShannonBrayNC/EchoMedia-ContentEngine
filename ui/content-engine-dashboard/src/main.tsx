import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { EmasAdStudio } from './EmasAdStudio';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
    <main className="app-shell emas-shell" aria-label="EchoMedia Ad Studio">
      <EmasAdStudio />
    </main>
  </React.StrictMode>
);
