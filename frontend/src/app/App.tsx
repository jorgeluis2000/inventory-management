import { Badge, Button, Card, FloatingLabel, HR, Label, Modal, TextInput } from "flowbite-react";
import { useEffect, useState } from "react";
import { useGetFetch, usePostFetch } from "@/utils/hooks/fetch-data";
import { PATH_DEFAULT, SERVER_LOCAL } from "@/utils/constants/server";
import './App.css'
import { ProductContent, ResponseAddProduct, ResponseList } from "@/utils/domain/types/responses.type";
import { toast } from "react-toastify";
import { BodyAddProduct } from "@/utils/domain/types/body.type";
import { useGetLocalStorage } from "@/utils/hooks/local-storage";
import { useLocation } from "wouter";
import { HiClock } from "react-icons/hi";
import { format } from "@formkit/tempo";

function App() {
  const [products, setProducts] = useState<ProductContent[]>([])
  const [nextPage, setNextPage] = useState<string | null | undefined>(null)
  const [openModalAddProduct, setOpenModalAddProduct] = useState(false);

  const [newName, setNewName] = useState("")
  const [newSerial, setNewSerial] = useState("")
  const [newPrice, setNewPrice] = useState("")

  const [location, setLocation] = useLocation();

  useEffect(() => {
    const exec_data = async () => {
      const data = await useGetFetch<ResponseList<ProductContent>>(SERVER_LOCAL, { path: `${PATH_DEFAULT}/products/`, tokenAuth: useGetLocalStorage('token') ?? "" }) as ResponseList<ProductContent>
      if (data.results) {
        setNextPage(data.next)
        setProducts(data.results)
      }
    }
    exec_data()
  }, [])
  return (
    <>
      <Card className='w-full max-w-screen-2xl mt-10'>
        <h5 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
          Inventarios
        </h5>
        <div className="flex flex-col md:flex-row">
          <Button color="primary" onClick={() => setOpenModalAddProduct(true)}>
            Agregar producto
          </Button>
        </div>
      </Card>
      <Modal show={openModalAddProduct} onClose={() => setOpenModalAddProduct(false)}>
        <Modal.Header>Inicia Sección Ahora</Modal.Header>
        <Modal.Body>
          <div className="space-y-6">
            <FloatingLabel variant="outlined" label="Nombre" onChange={(event) => setNewName(event.target.value)} />
            <FloatingLabel variant="outlined" type="text" label="Serial" onChange={(event) => setNewSerial(event.target.value)} />
            <FloatingLabel variant="outlined" type="number" label="Precio" onChange={(event) => setNewPrice(event.target.value)} />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button color="gray" onClick={() => setOpenModalAddProduct(false)}>
            Cancelar
          </Button>
          <Button color="primary" onClick={async () => {
            const response = await usePostFetch<ResponseAddProduct, BodyAddProduct>(SERVER_LOCAL, {
              path: '/api/v1/products/', data: {
                name: newName,
                serial: newSerial,
                price: newPrice
              },
              tokenAuth: useGetLocalStorage('token') ?? ""
            }) as ResponseAddProduct
            toast(response.detail ?? "Se ha agregado un nuevo producto.", { type: 'info' })
            setOpenModalAddProduct(false)
            setLocation(location, { replace: true })
          }}>Agregar producto</Button>
        </Modal.Footer>
      </Modal>
      <Card className='w-full gap-2 max-w-screen-2xl'>
        {
          products?.map((item) => (
            <div className="w-full space-y-4" key={item.id}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full" >
                <div className="flex max-w-md flex-col gap-4">
                  <Label htmlFor={`name-product-${item.id}`}>Nombre producto</Label>
                  <TextInput type="text" id={`name-product-${item.id}`} value={`${item.name}`} placeholder={item.name} disabled readOnly />
                  <Label htmlFor={`serial-product-${item.id}`}>Serial producto</Label>
                  <TextInput type="text" id={`serial-product-${item.id}`} value={`${item.serial}`} placeholder={item.serial} disabled readOnly />
                </div>

                <div className="flex max-w-md flex-col gap-4">
                  <Label htmlFor={`name-count-${item.id}`}>Cantidad del producto</Label>
                  <TextInput type="text" id={`name-count-${item.id}`} value={`${item.count}`} placeholder={`${item.count}`} disabled readOnly />
                  <Label htmlFor={`serial-price-${item.id}`}>Precio del producto</Label>
                  <TextInput type="text" id={`serial-price-${item.id}`} value={`$ ${Number(item.price).toFixed(2)}`} placeholder={`$ ${Number(item.price).toFixed(2)}`} disabled readOnly />
                </div>

              </div>
              <div className="flex justify-end font-medium">
                <div className="max-w-xs">
                  <Badge color="gray" icon={HiClock}>
                    {format(item.updated_at, "long")}
                  </Badge>
                </div>
              </div>
              <HR />
            </div>
          ))
        }
        {
          nextPage ?
            <Button color="primary" onClick={async () => {
              if (nextPage) {
                const data = await useGetFetch<ResponseList<ProductContent>>(nextPage, { tokenAuth: useGetLocalStorage('token') ?? "" }) as ResponseList<ProductContent>
                if (data?.results) {
                  setNextPage(data.next)
                  const results = data.results
                  setProducts((currentList) => ([...currentList, ...results]))
                }
              }
            }}>
              Ver más
            </Button>
            :
            <></>
        }

      </Card>
    </>
  )
}

export default App
