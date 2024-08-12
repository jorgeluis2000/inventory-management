import { Badge, Button, Card, FloatingLabel, HR, Label, Modal, TextInput } from "flowbite-react";
import { useEffect, useState } from "react";
import { useGetFetch, usePostFetch, usePutFetch } from "@/utils/hooks/fetch-data";
import { PATH_DEFAULT, SERVER_LOCAL } from "@/utils/constants/server";
import './App.css'
import { ProductContent, ResponseAddProduct, ResponseDefault, ResponseList } from "@/utils/domain/types/responses.type";
import { toast } from "react-toastify";
import { BodyAddProduct, BodyUpdateCount } from "@/utils/domain/types/body.type";
import { useGetLocalStorage } from "@/utils/hooks/local-storage";
import { HiClock } from "react-icons/hi";
import { format } from "@formkit/tempo";

interface Props {
  children?: React.ReactNode
}

function App(_props: Props) {
  const [products, setProducts] = useState<ProductContent[]>([])
  const [nextPage, setNextPage] = useState<string | null | undefined>(null)
  const [openModalAddProduct, setOpenModalAddProduct] = useState(false);

  const [newName, setNewName] = useState("")
  const [newSerial, setNewSerial] = useState("")
  const [newPrice, setNewPrice] = useState("")
  const [updateProduct, setUpdateProduct] = useState({ id: "", name: "", serial: "", price: "", count: "" })

  const [openModalUpdateProduct, setOpenModalUpdateProduct] = useState(false)

  const exec_data = async () => {
    const data = await useGetFetch<ResponseList<ProductContent>>(SERVER_LOCAL, { path: `${PATH_DEFAULT}/products/`, tokenAuth: useGetLocalStorage('token') ?? "" }) as ResponseList<ProductContent>
    if (data.results) {
      setNextPage(data.next)
      setProducts(data.results)
    }
  }

  useEffect(() => {
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
      <Modal show={openModalUpdateProduct} onClose={() => setOpenModalUpdateProduct(false)}>
        <Modal.Header>Editar Producto</Modal.Header>
        <Modal.Body>
          <div className="space-y-6">
            <FloatingLabel variant="outlined" label="Nombre" defaultValue={updateProduct.name} onChange={(event) => setUpdateProduct((before => ({ ...before, name: event.target.value })))} />
            <FloatingLabel variant="outlined" type="text" defaultValue={updateProduct.serial} label="Serial" onChange={(event) => setUpdateProduct((before => ({ ...before, serial: event.target.value })))} />
            <FloatingLabel variant="outlined" type="number" defaultValue={Number(updateProduct.price).toFixed(2)} label="Precio" onChange={(event) => setUpdateProduct((before => ({ ...before, price: event.target.value })))} />
            <FloatingLabel variant="outlined" type="number" defaultValue={Number(updateProduct.count)} label="Cantidad" onChange={(event) => setUpdateProduct((before => ({ ...before, count: event.target.value })))} />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button color="gray" onClick={() => setOpenModalUpdateProduct(false)}>
            Cancelar
          </Button>

          <Button color="primary" onClick={async () => {
            const response = await usePutFetch<ResponseAddProduct, BodyAddProduct>(SERVER_LOCAL, {
              path: `/api/v1/products/${updateProduct.id}/`, data: {
                name: updateProduct.name,
                serial: updateProduct.serial,
                price: updateProduct.price
              },
              tokenAuth: useGetLocalStorage('token') ?? ""
            }) as ResponseAddProduct
            toast(response.detail ?? "Se ha actualizado el producto.", { type: 'info' })

            const responseUpdate = await usePostFetch<ResponseDefault, BodyUpdateCount>(SERVER_LOCAL, {
              path: `/api/v1/products/${updateProduct.id.toString()}/increase_inventory/`, data: {
                count: Number(updateProduct.count)
              },
              tokenAuth: useGetLocalStorage('token') ?? ""
            }) as ResponseAddProduct
            toast(responseUpdate.detail ?? "Se ha actualizado la cantidad del producto.", { type: 'info' })

            setOpenModalUpdateProduct(false)
            await exec_data()
          }}>Actualizar producto</Button>
        </Modal.Footer>
      </Modal>
      <Modal show={openModalAddProduct} onClose={() => setOpenModalAddProduct(false)}>
        <Modal.Header>Producto</Modal.Header>
        <Modal.Body>
          <div className="space-y-6">
            <FloatingLabel variant="outlined" label="Nombre" onChange={(event) => setNewName(event.target.value)} />
            <FloatingLabel variant="outlined" type="text" label="Serial" onChange={(event) => setNewSerial(event.target.value)} />
            <FloatingLabel variant="outlined" type="number" label="Precio" onChange={(event) => setNewPrice(event.target.value)} />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button color="gray" onClick={() => setOpenModalUpdateProduct(false)}>
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
            await exec_data()
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
              <div className="flex justify-start items-center gap-2 h-auto">
                <Button color="success" onClick={() => {
                  setUpdateProduct({
                    id: item.id.toString(),
                    count: item.count.toString(),
                    name: item.name,
                    price: item.price,
                    serial: item.serial
                  })
                  setOpenModalUpdateProduct(true)
                }}>
                  Actualizar producto
                </Button>
              </div>
              <div className="flex justify-end font-medium">
                <div className="max-w-xs">
                  <Badge color="gray" icon={HiClock}>
                    {format(item.created_at, "full")}
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
