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


function Router() {

  return (
    <>
      <div className='min-h-screen dark:bg-gray-800'>
        <CustomNavbar />
        <div className='flex flex-col space-y-5 justify-center items-center w-full overflow-x-hidden'>
          <Switch>
            <Route path={"/"}>{<App />}</Route>
          </Switch>
        </div>
      </div>
      <Footer className='mt-10'  container >
        <Footer.Copyright href="https://github.com/jorgeluis2000" by="Jorge Luis Güiza" year={2024} />
      </Footer>
    </>
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
