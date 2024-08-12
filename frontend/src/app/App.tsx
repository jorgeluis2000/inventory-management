import { Card } from "flowbite-react";
import { useEffect, useState } from "react";
import { useGetFetch } from "@/utils/hooks/fetch-data";
import { PATH_CREDENTIALS, PATH_DEFAULT, SERVER_LOCAL } from "@/utils/constants/server";
import { DataResponse } from "@/utils/domain/types/fetch.type";
import './App.css'

function App() {
  const myToken = "0c2c4af5fd69299f8ac91f225c1d74aae8305d83"
  const [listUser, setListUser] = useState<DataResponse>()
  useEffect(() => {
    const exec_data = async() => {
      const data = await useGetFetch<DataResponse>(SERVER_LOCAL, { path: `${PATH_DEFAULT}${PATH_CREDENTIALS}`, tokenAuth: myToken })
      setListUser(data)
    }
    exec_data()
  }, [])
  return (
    <Card className='w-full'>
      <h5 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
        Message {JSON.stringify(listUser, null, 2)}
      </h5>

    </Card>
  )
}

export default App
