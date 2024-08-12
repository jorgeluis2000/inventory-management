import { StrictMode } from 'react'
import { Flowbite, Footer } from "flowbite-react";
import { createRoot } from 'react-dom/client'
import { customTheme } from './utils/constants/theme.ts';
import { Route, Switch } from 'wouter'
import { ToastContainer } from 'react-toastify'
import App from './app/App.tsx'
import 'react-toastify/dist/ReactToastify.css'
import './index.css'
import { CustomNavbar } from '@/utils/components/ui/CustomNavbar.tsx';
import InvoicesPage from './app/Invoices.tsx';


function Router() {

  return (
    <div className='dark:bg-gray-800'>
      <div className='min-h-screen'>
        <CustomNavbar />
        <div className='flex flex-col gap-4 justify-center items-center w-full overflow-x-hidden'>
          <Switch>
            <Route path="/" >{<App />}</Route>
            <Route path="/factura">{<InvoicesPage />}</Route>
            <Route>404: No such page!</Route>
          </Switch>
        </div>
      </div>
      <Footer className='mt-10'  container >
        <Footer.Copyright href="https://github.com/jorgeluis2000" by="Jorge Luis Güiza" year={2024} />
      </Footer>
    </div>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ToastContainer
      position="top-right"
      autoClose={5000}
      hideProgressBar={false}
      newestOnTop={false}
      closeOnClick
      rtl={false}
      pauseOnFocusLoss
      draggable
      pauseOnHover
      theme="colored"
    />
    <Flowbite theme={{ theme: customTheme }}>
      <Router />
    </Flowbite>
  </StrictMode>,
)
